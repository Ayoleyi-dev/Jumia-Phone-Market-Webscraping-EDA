# Methodology and Analytical Boundaries

This project uses a point-in-time scrape of smartphone listings from Jumia Nigeria to study the composition of the online smartphone marketplace.

## What the data supports

The dataset can support analysis of:

- listing share by brand
- advertised price distributions
- discount patterns
- official-store versus third-party listing presence
- customer ratings and review counts where available
- repeated/duplicate listing titles
- price-segment composition

## What the data does not support

The dataset does **not** contain units sold, order value, revenue, stock levels, conversion rate, or true market share. Conclusions are therefore phrased as listing-level marketplace observations rather than claims about total Nigerian smartphone sales.

## Data quality approach

Extraction and transformation are separated. The raw snapshot is preserved unchanged. Cleaning code produces a processed analytical dataset and a validation layer checks price coverage, rating bounds, review counts, discount bounds, and brand coverage.
