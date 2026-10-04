"""Reusable analytical summaries for the Jumia market-intelligence project."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

DEFAULT_DATA = Path("data/processed/jumia_phones_clean.csv")

def load_processed(path: str | Path = DEFAULT_DATA) -> pd.DataFrame:
    return pd.read_csv(path)

def smartphone_scope(df: pd.DataFrame) -> pd.DataFrame:
    if "is_smartphone_candidate" not in df.columns:
        raise KeyError("Processed dataset is missing is_smartphone_candidate.")
    return df[df["is_smartphone_candidate"].fillna(False)].copy()

def market_kpis(df: pd.DataFrame) -> dict:
    scoped = smartphone_scope(df)
    shares = scoped["brand"].value_counts(normalize=True)
    discounted = scoped["discount_pct"].gt(0)
    return {
        "raw_rows": int(len(df)),
        "smartphone_rows": int(len(scoped)),
        "excluded_non_phone_rows": int(len(df) - len(scoped)),
        "brands": int(scoped["brand"].nunique()),
        "median_price_ngn": float(scoped["price_ngn"].median()),
        "mean_price_ngn": float(scoped["price_ngn"].mean()),
        "official_listing_share": float(scoped["is_official_store"].mean()),
        "rating_coverage": float(scoped["rating"].notna().mean()),
        "discounted_listing_share": float(discounted.mean()),
        "median_discount_when_discounted": float(scoped.loc[discounted, "discount_pct"].median()),
        "duplicate_title_share": float(scoped["duplicate_title"].mean()),
        "top_brand_share": float(shares.iloc[0]),
        "top_5_brand_share": float(shares.iloc[:5].sum()),
        "listing_concentration_hhi": float((shares**2).sum()),
    }

def brand_summary(df: pd.DataFrame) -> pd.DataFrame:
    scoped = smartphone_scope(df)
    out = scoped.groupby("brand").agg(
        listings=("phone_name","size"),
        unique_titles=("phone_name","nunique"),
        median_price_ngn=("price_ngn","median"),
        q1_price_ngn=("price_ngn",lambda s:s.quantile(.25)),
        q3_price_ngn=("price_ngn",lambda s:s.quantile(.75)),
        average_discount_pct=("discount_pct","mean"),
        median_discount_pct=("discount_pct","median"),
        official_listing_share=("is_official_store","mean"),
        rating_coverage=("rating",lambda s:s.notna().mean()),
        average_rating=("rating","mean"),
        total_reviews=("review_count","sum"),
        median_reviews=("review_count","median"),
        duplicate_title_share=("duplicate_title","mean"),
    ).sort_values("listings",ascending=False)
    out["listing_share"] = out["listings"] / len(scoped)
    return out.reset_index()

def segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    scoped = smartphone_scope(df)
    order = ["Budget","Mid-range","Upper mid-range","Premium"]
    counts = scoped["price_segment"].value_counts().reindex(order).fillna(0).astype(int)
    out = counts.rename("listings").to_frame()
    out["listing_share"] = out["listings"] / len(scoped)
    return out.reset_index(names="price_segment")

def channel_summary(df: pd.DataFrame) -> pd.DataFrame:
    scoped = smartphone_scope(df)
    out = scoped.groupby("is_official_store").agg(
        listings=("phone_name","size"),
        median_price_ngn=("price_ngn","median"),
        average_discount_pct=("discount_pct","mean"),
        median_discount_pct=("discount_pct","median"),
        rating_coverage=("rating",lambda s:s.notna().mean()),
        average_rating=("rating","mean"),
        median_reviews=("review_count","median"),
        mean_reviews=("review_count","mean"),
    ).reset_index()
    out["channel"] = out["is_official_store"].map({True:"Official store",False:"Third-party"})
    out["listing_share"] = out["listings"] / len(scoped)
    return out

def engagement_summary(df: pd.DataFrame) -> dict:
    scoped = smartphone_scope(df)
    rated = scoped[scoped["rating"].notna()].copy()
    return {
        "rated_rows": int(len(rated)),
        "rating_coverage": float(len(rated)/len(scoped)),
        "discount_vs_reviews_spearman": float(rated["discount_pct"].corr(rated["review_count"],method="spearman")),
        "price_vs_reviews_spearman": float(rated["price_ngn"].corr(rated["review_count"],method="spearman")),
        "price_vs_rating_spearman": float(rated["price_ngn"].corr(rated["rating"],method="spearman")),
    }

def export_summaries(df: pd.DataFrame, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    brand_summary(df).to_csv(output_dir/"brand_summary.csv",index=False)
    segment_summary(df).to_csv(output_dir/"price_segment_summary.csv",index=False)
    channel_summary(df).to_csv(output_dir/"channel_summary.csv",index=False)
