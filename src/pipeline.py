"""Run the processing and data-quality pipeline on a saved raw snapshot."""

from pathlib import Path

from cleaning import clean_file
from validate import checks_to_frame, validate

PRIMARY_RAW = Path("data/raw/jumia_phones_snapshot.csv")
LEGACY_RAW = Path("Code Alpha Jumia webscraping/Data/jumia_phones_final.csv")
PROCESSED = Path("data/processed/jumia_phones_clean.csv")
QUALITY = Path("data/processed/data_quality_report.csv")


def resolve_input() -> Path:
    """Use the refactored raw snapshot when present, otherwise the legacy dataset."""
    if PRIMARY_RAW.exists():
        return PRIMARY_RAW
    if LEGACY_RAW.exists():
        return LEGACY_RAW
    raise FileNotFoundError(
        "No input dataset found. Expected either "
        f"{PRIMARY_RAW} or {LEGACY_RAW}."
    )


def main() -> None:
    raw = resolve_input()
    cleaned = clean_file(raw, PROCESSED)
    report = checks_to_frame(validate(cleaned))
    QUALITY.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(QUALITY, index=False)

    print(f"Input: {raw}")
    print(f"Processed rows: {len(cleaned):,}")
    print(report.to_string(index=False))

    if not report["passed"].all():
        raise SystemExit("One or more data-quality checks failed.")


if __name__ == "__main__":
    main()
