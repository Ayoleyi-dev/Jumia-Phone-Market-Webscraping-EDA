# Jumia Nigeria Smartphone Market — Analysis Findings

## Scope

The preserved scrape contains 1,960 rows. A conservative scope rule flags 52 obvious tablets, accessories, headphones, or calculators, leaving **1,908 smartphone-candidate listings**.

This is listing-level marketplace data. It does not contain units sold, revenue, inventory, conversion, or national market share.

## Headline findings

1. **Listing presence is highly concentrated.** Samsung represents **44.2%** of in-scope listings. Xiaomi is second at **11.9%**, followed by Tecno (**7.7%**), Infinix (**6.6%**) and Itel (**6.5%**). The top five brands account for **76.9%** of listings.

2. **Price positions differ sharply.** The overall median advertised smartphone price is **₦290,000**. Major-brand medians range from about **₦129k for Itel** and **₦180k for Tecno** to **₦385k for Samsung**, **₦1.34m for Google**, and **₦2.65m for Apple**.

3. **The middle of the market is the largest band.** About **20.5%** of listings are Budget (<₦150k), **31.6%** Mid-range (₦150k–<₦300k), **24.8%** Upper mid-range (₦300k–<₦600k), and **22.9%** Premium (≥₦600k).

4. **Third-party sellers dominate.** Only **8.3%** of in-scope listings carry an official-store badge.

5. **Official-store listings have much better engagement-data coverage.** Ratings are available on roughly **77.2%** of official-store listings versus **29.4%** of third-party listings. This is descriptive, not causal, because brand and product mix differ between channels.

6. **Markdowns are common.** Roughly **60.6%** of in-scope listings show a positive calculated markdown. Among those discounted listings, the median markdown is **18.1%**.

7. **Duplicate-title visibility matters.** Around **19.1%** of in-scope rows belong to an exact title that appears more than once. These are retained and flagged because they can represent repeated offers or multiple sellers rather than guaranteed duplicate data.

8. **Ratings/reviews are incomplete.** Only **33.3%** of smartphone-candidate listings have usable rating/review information.

## Exploratory engagement associations

Among rows with rating/review data, Spearman correlations are modest: advertised discount vs review count is approximately **+0.12**, advertised price vs review count approximately **−0.32**, and advertised price vs rating approximately **+0.23**. These are exploratory associations only.

## Business interpretation

- Samsung is the central listing benchmark because of its unusually large footprint.
- Xiaomi, Tecno, Infinix, and Itel form a dense value/mid-market competitive set.
- Premium-brand listings are smaller by count but materially lift the upper price tail.
- Third-party seller behaviour is essential to understanding this category.
- Repeated snapshots would unlock price-change, assortment-churn, and model-lifecycle analysis.
