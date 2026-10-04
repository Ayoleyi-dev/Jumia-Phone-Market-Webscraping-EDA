"""Load the processed smartphone snapshot into SQLite."""
from pathlib import Path
import sqlite3
import pandas as pd

INPUT = Path("data/processed/jumia_phones_clean.csv")
OUTPUT = Path("data/processed/jumia_market.db")
TABLE = "jumia_listings"

def main() -> None:
    df = pd.read_csv(INPUT)
    df = df[df["is_smartphone_candidate"].fillna(False)].copy()
    for column in ["is_official_store","is_smartphone_candidate","duplicate_title"]:
        df[column] = df[column].astype(int)
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(OUTPUT) as conn:
        df.to_sql(TABLE,conn,if_exists="replace",index=False)
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_brand ON {TABLE}(brand)")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_segment ON {TABLE}(price_segment)")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_official ON {TABLE}(is_official_store)")
    print(f"Loaded {len(df):,} rows into {OUTPUT}")

if __name__ == "__main__":
    main()
