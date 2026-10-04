# Jumia Nigeria Smartphone Market Intelligence Pipeline

A reproducible Python analytics project that collects, cleans, validates, and analyzes smartphone listings from Jumia Nigeria.

![Market analysis dashboard](Market_Analysis_Dashboard.png)

## Executive Summary

This project studies the structure of Jumia Nigeria's online smartphone marketplace using listing-level data. The current historical snapshot contains **1,960 smartphone listings** captured from the Android phones category.

The project has been refactored from a single exploratory notebook into a small analytics pipeline with separate extraction, transformation, validation, testing, and documentation layers.

> **Analytical boundary:** this dataset represents marketplace **listings**, not completed sales. Listing counts should not be interpreted as unit sales, revenue, inventory, or Nigerian smartphone market share.

## Business Questions

The analysis is designed to answer questions such as:

- Which brands account for the largest share of Jumia smartphone listings?
- How do advertised prices differ across brands and price segments?
- What discount patterns appear across manufacturers?
- How much of the marketplace is represented by official-store listings versus third-party listings?
- Do official-store listings differ in ratings or review activity?
- Which listing titles appear repeatedly and may represent duplicate or variant offers?
- How complete and reliable are key analytical fields such as price, rating, reviews, and product URLs?

## Pipeline Architecture

```text
Jumia Nigeria
     |
     v
Python scraper
     |
     v
Raw CSV snapshot
     |
     v
Cleaning + normalization
     |
     v
Data-quality checks
     |
     +------> quality report
     |
     v
Processed analytical dataset
     |
     +------> Python EDA
     |
     +------> dashboard / reporting
```

## Repository Structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── scraper.py
│   ├── cleaning.py
│   ├── validate.py
│   └── pipeline.py
├── tests/
│   └── test_cleaning.py
├── docs/
│   ├── data_dictionary.md
│   └── methodology.md
├── Code Alpha Jumia webscraping/
│   └── notebooks/
│       └── Webscraping.ipynb
├── Market_Analysis_Dashboard.png
├── requirements.txt
└── README.md
```

The original notebook and supporting files are retained for project history. The `src/` directory is now the canonical implementation.

## Data Quality Improvements

The historical project contained several issues that are now handled explicitly:

- **Price parsing:** Naira-formatted prices are converted to numeric values.
- **Brand normalization:** variants such as `XIAOMI`, `itel`, and `Oneplus` are standardized.
- **Ratings:** rating strings are converted to numeric 0–5 values.
- **Review counts:** legacy malformed review strings are parsed into a numeric review-count field.
- **Discounts:** discount percentages are recalculated from current and old prices.
- **Broken URLs:** historical links that point to Jumia's login route are treated as missing rather than presented as product links.
- **Duplicate listings:** exact repeated listing titles are flagged instead of silently removed.
- **Price segmentation:** listings are grouped into Budget, Mid-range, Upper mid-range, and Premium bands for business analysis.

### Current validation results

| Check | Result |
|---|---|
| Processed rows present | Pass |
| Numeric price coverage | **99.8%** |
| Rating bounds | Pass |
| Non-negative review counts | Pass |
| Discount range | Pass |
| Normalized brand coverage | **100%** |

## Tech Stack

- **Python**
- **Pandas / NumPy**
- **Requests**
- **BeautifulSoup**
- **Matplotlib**
- **Pytest**
- **Git / GitHub**

## Running the Project

Create a virtual environment and install the dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
python -m pytest -q
```

Process the preserved historical snapshot:

```bash
PYTHONPATH=src python src/pipeline.py
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python src/pipeline.py
```

Run a fresh scrape:

```bash
python src/scraper.py --pages 50 --delay 1
```

Fresh scraping depends on Jumia's current HTML structure and website access rules, so selectors may require maintenance over time.

## Historical Snapshot Notes

The original snapshot contains **1,960 listings**. Some fields were incompletely captured by the original scraper:

- ratings are available for only part of the dataset;
- many historical product URLs were blank;
- most captured non-blank URLs pointed to a login route instead of the product page.

The refactored pipeline does **not** fabricate missing values. It preserves the raw snapshot and makes these limitations visible in the processed data and documentation.

## What This Project Demonstrates

This repository now demonstrates a broader analyst workflow:

1. acquiring external marketplace data;
2. preserving raw source data;
3. cleaning and normalizing inconsistent fields;
4. validating data quality;
5. documenting analytical limitations;
6. structuring data for business analysis;
7. testing reusable parsing logic;
8. preparing a repeatable pipeline for future snapshots.

## Next Development Milestones

- Rebuild the exploratory analysis notebook around clear business questions.
- Add time-stamped repeated snapshots for price-change analysis.
- Create a refreshed dashboard from the processed dataset.
- Add SQL analysis queries for common marketplace KPIs.
- Expand automated tests for scraper selectors and edge cases.

## Data Source

The project uses publicly visible product-listing information from the Jumia Nigeria smartphone category for educational portfolio analysis.
