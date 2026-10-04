# Data Dictionary

## Processed analytical dataset

| Column | Type | Meaning |
|---|---|---|
| `phone_name` | string | Listing title captured from Jumia |
| `brand` | string | Normalized manufacturer/brand |
| `price_ngn` | numeric | Current advertised price in Nigerian naira |
| `old_price_ngn` | numeric | Previous advertised price where available |
| `discount_pct` | numeric | Recalculated percentage discount |
| `price_segment` | category | Budget, Mid-range, Upper mid-range, or Premium |
| `rating` | numeric | Customer rating on a 0–5 scale where available |
| `review_count` | numeric | Review count recovered from the listing |
| `is_official_store` | boolean | Whether the listing carried the Jumia official-store badge |
| `product_url` | string | Product URL when a valid product link was captured |
| `duplicate_title` | boolean | Flags exact repeated listing titles for analysis |

## Important limitations

- The dataset represents **listings**, not completed sales transactions.
- Prices are advertised prices at scrape time and should not be interpreted as realized selling prices.
- Listing counts are not market share or inventory counts.
- The historical snapshot contains broken/missing URLs from the original scraper; invalid login URLs are deliberately converted to null rather than fabricated.
- Missing ratings normally mean no usable rating was exposed in the captured listing card.
