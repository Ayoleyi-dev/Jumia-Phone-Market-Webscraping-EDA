"""Cleaning utilities for Jumia smartphone listing data."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd


BRAND_ALIASES = {
    "xiaomi": "Xiaomi",
    "redmi": "Xiaomi",
    "poco": "Poco",
    "tecno": "Tecno",
    "itel": "Itel",
    "infinix": "Infinix",
    "samsung": "Samsung",
    "oppo": "Oppo",
    "realme": "Realme",
    "vivo": "Vivo",
    "huawei": "Huawei",
    "apple": "Apple",
    "iphone": "Apple",
    "google": "Google",
    "honor": "Honor",
    "zte": "ZTE",
    "nokia": "Nokia",
    "motorola": "Motorola",
    "oneplus": "OnePlus",
    "oukitel": "Oukitel",
    "hmd": "HMD",
}


def parse_naira(value) -> float:
    """Convert a Naira-formatted price to a float; return NaN if invalid."""
    if pd.isna(value):
        return np.nan
    text = re.sub(r"[^\d.]", "", str(value))
    if not text:
        return np.nan
    try:
        return float(text)
    except ValueError:
        return np.nan


def parse_rating(value) -> float:
    """Extract a 0–5 rating from strings such as '4.3 out of 5'."""
    if pd.isna(value):
        return np.nan
    match = re.search(r"(\d(?:\.\d+)?)\s*out of\s*5", str(value), flags=re.I)
    if not match:
        return np.nan
    rating = float(match.group(1))
    return rating if 0 <= rating <= 5 else np.nan


def parse_review_count(value) -> float:
    """
    Extract a review count.

    Historical snapshots contain malformed values such as
    '4.1 out of 5861'. In those strings, the final integer is the
    best recoverable review-count field from the original scrape.
    """
    if pd.isna(value):
        return np.nan

    text = str(value).strip()
    if text in {"", "0", "nan", "None"}:
        return 0.0

    paren = re.search(r"\(([\d,]+)\)", text)
    if paren:
        return float(paren.group(1).replace(",", ""))

    legacy = re.search(r"out of\s*([\d,]+)\s*$", text, flags=re.I)
    if legacy:
        return float(legacy.group(1).replace(",", ""))

    if re.fullmatch(r"[\d,]+", text):
        return float(text.replace(",", ""))

    return np.nan


def normalize_brand(phone_name, existing_brand=None) -> str | None:
    """Normalize common smartphone brand variants using listing text."""
    candidates = []
    if existing_brand is not None and not pd.isna(existing_brand):
        candidates.append(str(existing_brand))
    if phone_name is not None and not pd.isna(phone_name):
        candidates.extend(str(phone_name).split()[:3])

    for candidate in candidates:
        key = re.sub(r"[^a-z0-9]", "", candidate.lower())
        if key in BRAND_ALIASES:
            return BRAND_ALIASES[key]

    if existing_brand is not None and not pd.isna(existing_brand):
        text = str(existing_brand).strip()
        return text.title() if text else None
    return None


def clean_product_link(value) -> str | None:
    """Keep only plausible product URLs; discard login and malformed links."""
    if pd.isna(value):
        return None
    link = str(value).strip()
    if not link:
        return None
    if "/customer/account/login" in link:
        return None
    if not link.startswith("http"):
        return None
    return link


def clean_listings(df: pd.DataFrame) -> pd.DataFrame:
    """Return a normalized analytical dataset from a raw Jumia snapshot."""
    out = df.copy()

    if "Price_Num" in out.columns:
        out["price_ngn"] = pd.to_numeric(out["Price_Num"], errors="coerce")
    else:
        out["price_ngn"] = out["Price"].map(parse_naira)

    if "Old_Price_Num" in out.columns:
        out["old_price_ngn"] = pd.to_numeric(out["Old_Price_Num"], errors="coerce")
    else:
        out["old_price_ngn"] = out["Old Price"].map(parse_naira)

    out["rating"] = out["Rating"].map(parse_rating)
    out["review_count"] = out["Verified Reviews"].map(parse_review_count)
    out["brand"] = [
        normalize_brand(name, brand)
        for name, brand in zip(out["Phone Name"], out.get("Brand", pd.Series(index=out.index)))
    ]
    out["is_official_store"] = (
        out["Official Store"].astype(str).str.strip().str.lower().map({"yes": True, "no": False})
    )
    out["product_url"] = out["Product Link"].map(clean_product_link)

    valid_old = out["old_price_ngn"].gt(0)
    out["discount_pct"] = np.where(
        valid_old & out["price_ngn"].notna(),
        ((out["old_price_ngn"] - out["price_ngn"]) / out["old_price_ngn"]) * 100,
        0.0,
    )
    out["discount_pct"] = pd.Series(out["discount_pct"], index=out.index).clip(lower=0).round(1)

    out["price_segment"] = pd.cut(
        out["price_ngn"],
        bins=[0, 150_000, 300_000, 600_000, np.inf],
        labels=["Budget", "Mid-range", "Upper mid-range", "Premium"],
        right=False,
    )

    out["duplicate_title"] = out["Phone Name"].duplicated(keep=False)

    keep = [
        "Phone Name",
        "brand",
        "price_ngn",
        "old_price_ngn",
        "discount_pct",
        "price_segment",
        "rating",
        "review_count",
        "is_official_store",
        "product_url",
        "duplicate_title",
    ]
    out = out[keep].rename(columns={"Phone Name": "phone_name"})

    return out


def clean_file(input_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    """Clean a CSV snapshot and save the processed analytical dataset."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    df = pd.read_csv(input_path)
    cleaned = clean_listings(df)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)
    return cleaned
