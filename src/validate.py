"""Data-quality checks for the processed Jumia dataset."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def validate(df: pd.DataFrame) -> list[Check]:
    checks: list[Check] = []

    checks.append(Check(
        "rows_present",
        len(df) > 0,
        f"{len(df):,} processed rows",
    ))
    checks.append(Check(
        "price_coverage",
        df["price_ngn"].notna().mean() >= 0.98,
        f"{df['price_ngn'].notna().mean():.1%} of rows have a numeric price",
    ))
    checks.append(Check(
        "valid_ratings",
        df["rating"].dropna().between(0, 5).all(),
        "All non-null ratings are between 0 and 5",
    ))
    checks.append(Check(
        "nonnegative_reviews",
        df["review_count"].dropna().ge(0).all(),
        "All non-null review counts are non-negative",
    ))
    checks.append(Check(
        "discount_bounds",
        df["discount_pct"].between(0, 100).all(),
        "All discounts are between 0% and 100%",
    ))
    checks.append(Check(
        "brand_coverage",
        df["brand"].notna().mean() >= 0.95,
        f"{df['brand'].notna().mean():.1%} of rows have a normalized brand",
    ))

    return checks


def checks_to_frame(checks: list[Check]) -> pd.DataFrame:
    return pd.DataFrame([c.__dict__ for c in checks])
