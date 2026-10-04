# Jumia Nigeria Smartphone Market Intelligence Pipeline

A reproducible analytics project for collecting, cleaning, validating, analyzing, and reporting on smartphone listings from Jumia Nigeria.

## Executive Summary

The preserved scrape contains **1,960 rows**. A conservative scope rule flags **52 obvious non-phone listings**, leaving **1,908 smartphone-candidate listings** for analysis.

> This is listing-level marketplace data, not sales data. Listing share is not unit-sales share, revenue share, inventory share, conversion, or Nigerian smartphone market share.

## Key Findings

- **Samsung:** 44.2% of in-scope listings.
- **Top five brands:** 76.9% of listings.
- **Median advertised price:** ₦290,000.
- **Largest price band:** Mid-range (₦150k–<₦300k), about 31.6%.
- **Official-store listings:** only 8.3%.
- **Listings with usable rating/review data:** 33.3%.
- **Listings with positive advertised markdowns:** 60.6%; median markdown among discounted listings is 18.1%.
- **Rows in repeated exact-title groups:** about 19.1%.

See [reports/analysis_findings.md](reports/analysis_findings.md) for interpretation and caveats.

## Architecture

```text
Jumia Nigeria
     |
     v
Python scraper
     |
     v
Raw snapshot
     |
     v
Cleaning + normalization
     |
     v
Validation + tests
     |
     v
Processed analytical dataset
     |
     +--> Python notebook analysis
     +--> SQLite + SQL queries
     +--> HTML dashboard
```

## Repository Structure

```text
src/
  scraper.py
  cleaning.py
  validate.py
  pipeline.py
  analysis.py
  build_sqlite.py
  build_dashboard.py
notebooks/
  market_analysis.ipynb
sql/
  analysis_queries.sql
dashboard/
  jumia_market_dashboard.html
reports/
  analysis_findings.md
docs/
  data_dictionary.md
  methodology.md
tests/
  test_cleaning.py
```

The original project files are retained for history, but the folders above are the canonical portfolio implementation.

## Data Quality Improvements

The refactor explicitly handles:

- numeric Naira price parsing;
- brand aliases and spelling/casing normalization;
- obvious non-phone category leakage;
- 0–5 numeric rating extraction;
- repair of the historical review-count format;
- recalculated advertised markdown percentages;
- invalid Jumia login URLs;
- exact-title duplicate flags;
- project-defined price segmentation.

### Historical review-field repair

The original scraper produced strings such as:

```text
4.1 out of 5861
```

This represents:

```text
rating = 4.1 out of 5
review_count = 861
```

The new parser correctly separates the fixed scale from the review count and includes regression tests for this case.

## Validation

| Check | Result |
|---|---|
| Processed rows | Pass |
| Numeric price coverage | 99.8% |
| Rating bounds | Pass |
| Non-negative reviews | Pass |
| Discount bounds | Pass |
| Brand coverage | 100% |
| Parser/cleaning tests | 6 passed |

## Analysis Highlights

### Brand concentration

Samsung accounts for **44.2%** of smartphone-candidate listings. Xiaomi follows at **11.9%**, Tecno at **7.7%**, Infinix at **6.6%**, and Itel at **6.5%**.

### Price positioning

| Brand | Median advertised price |
|---|---:|
| Itel | ₦128,999 |
| Tecno | ₦179,999 |
| Infinix | ₦185,000 |
| Xiaomi | ₦219,999 |
| Samsung | ₦385,000 |
| Google | ₦1,340,000 |
| Apple | ₦2,650,000 |

### Seller-channel structure

Third-party listings account for about **91.7%** of the in-scope snapshot. Rating data is present on roughly **77.2%** of official-store listings versus **29.4%** of third-party listings. This is descriptive, not causal.

## Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest -q
```

Process the historical snapshot:

```bash
PYTHONPATH=src python src/pipeline.py
```

Build SQLite database:

```bash
PYTHONPATH=src python src/build_sqlite.py
```

Run the queries in `sql/analysis_queries.sql`.

Build the dashboard:

```bash
PYTHONPATH=src python src/build_dashboard.py
```

Then open `dashboard/jumia_market_dashboard.html`.

Run a fresh scrape:

```bash
python src/scraper.py --pages 50 --delay 1
```

## Limitations

- single point-in-time snapshot;
- no units sold, revenue, conversion, inventory, or national market-share data;
- rating/review information is incomplete;
- historical product URLs were captured incorrectly;
- repeated titles can represent multiple offers, variants, or duplicate extraction and are therefore flagged rather than blindly removed.

## What This Demonstrates

This project now shows a broader analyst workflow than a standard notebook-only EDA:

1. external data acquisition;
2. raw-source preservation;
3. cleaning and normalization;
4. scope control;
5. automated validation and tests;
6. reusable KPI functions;
7. exploratory analysis;
8. SQL querying;
9. dashboard reporting;
10. documented assumptions and analytical limitations.

## Next Milestone

Repeated time-stamped snapshots would allow price-change, listing-churn, assortment, and model-lifecycle analysis.
