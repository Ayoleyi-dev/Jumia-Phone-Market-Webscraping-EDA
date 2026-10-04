# Methodology and Analytical Boundaries

The project uses a point-in-time Jumia Nigeria listing snapshot to study the online smartphone marketplace.

## Scope

The source contains 1,960 rows. A conservative classification rule excludes only obvious non-phone rows such as tablets, headphones, calculators, and accessory-only listings. The current analytical population contains **1,908 smartphone-candidate rows**.

## Supported analysis

The dataset supports:

- listing share by brand;
- advertised price distributions;
- project-defined price segments;
- advertised markdown patterns;
- official-store versus third-party presence;
- rating/review coverage where available;
- duplicate-title diagnostics;
- descriptive marketplace analysis.

## Unsupported claims

The dataset does not contain units sold, revenue, stock, conversion, seller revenue, or national market share.

## Data-quality approach

Raw data is preserved separately from transformations. Cleaning, scope classification, validation, analysis, and reporting are separated into reusable modules.

The historical scraper concatenated the fixed rating scale and review count. For example, `4.1 out of 5861` is repaired as rating 4.1/5 with 861 reviews. Invalid product/login URLs are treated as missing.

Repeated exact titles are flagged rather than automatically deleted because they may represent different offers or sellers.

## Statistical interpretation

Engagement correlations are exploratory. Channel comparisons are descriptive because official-store and third-party listings differ in brand and product mix.
