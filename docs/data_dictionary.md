# Data Dictionary

| Column | Meaning |
|---|---|
| `phone_name` | Listing title captured from Jumia |
| `brand` | Normalized manufacturer/brand |
| `price_ngn` | Current advertised price in Nigerian naira |
| `old_price_ngn` | Previous/reference advertised price where available |
| `discount_pct` | Recalculated advertised markdown percentage |
| `price_segment` | Budget, Mid-range, Upper mid-range, or Premium |
| `rating` | Customer rating on a 0–5 scale where available |
| `review_count` | Recovered review count |
| `is_official_store` | Whether the listing carried the official-store badge |
| `product_url` | Valid product URL where available |
| `is_smartphone_candidate` | Conservative scope flag for obvious non-phone leakage |
| `duplicate_title` | Whether the exact listing title occurs more than once |

## Price bands

- Budget: below ₦150,000
- Mid-range: ₦150,000 to below ₦300,000
- Upper mid-range: ₦300,000 to below ₦600,000
- Premium: ₦600,000 and above

These are project-defined analytical bands, not an asserted industry standard.

## Review-count repair

Historical values such as `4.1 out of 5861` mean `4.1 out of 5` plus 861 reviews. The cleaning layer removes the fixed scale and parses the remaining digits as the review count.

## Limitations

The data represents listings, not completed sales. Listing counts are not market share, inventory, or units sold. Invalid historical login URLs are converted to missing values rather than fabricated.
