-- Jumia Nigeria Smartphone Market Intelligence
-- SQLite-compatible queries. Run after: python src/build_sqlite.py

-- Brand listing share
SELECT brand, COUNT(*) AS listings,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),1) AS listing_share_pct,
       ROUND(AVG(price_ngn),0) AS average_price_ngn,
       ROUND(AVG(discount_pct),1) AS average_discount_pct
FROM jumia_listings
GROUP BY brand
ORDER BY listings DESC;

-- Price-segment mix
SELECT price_segment, COUNT(*) AS listings,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),1) AS listing_share_pct
FROM jumia_listings
WHERE price_segment IS NOT NULL
GROUP BY price_segment
ORDER BY listings DESC;

-- Official-store vs third-party
SELECT CASE WHEN is_official_store=1 THEN 'Official store' ELSE 'Third-party' END AS channel,
       COUNT(*) AS listings,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),1) AS listing_share_pct,
       ROUND(AVG(price_ngn),0) AS average_price_ngn,
       ROUND(AVG(discount_pct),1) AS average_discount_pct,
       ROUND(100.0 * AVG(CASE WHEN rating IS NOT NULL THEN 1.0 ELSE 0.0 END),1) AS rating_coverage_pct,
       ROUND(AVG(rating),2) AS average_rating,
       ROUND(AVG(review_count),1) AS average_review_count
FROM jumia_listings
GROUP BY is_official_store
ORDER BY is_official_store DESC;

-- Major-brand positioning
SELECT brand, COUNT(*) AS listings,
       ROUND(AVG(price_ngn),0) AS average_price_ngn,
       ROUND(AVG(discount_pct),1) AS average_discount_pct,
       ROUND(100.0 * AVG(is_official_store),1) AS official_listing_share_pct,
       ROUND(100.0 * AVG(CASE WHEN rating IS NOT NULL THEN 1.0 ELSE 0.0 END),1) AS rating_coverage_pct
FROM jumia_listings
GROUP BY brand
HAVING COUNT(*) >= 20
ORDER BY listings DESC;

-- Data-quality coverage
SELECT COUNT(*) AS rows_in_scope,
       SUM(CASE WHEN price_ngn IS NULL THEN 1 ELSE 0 END) AS missing_price,
       SUM(CASE WHEN rating IS NULL THEN 1 ELSE 0 END) AS missing_rating,
       SUM(CASE WHEN product_url IS NULL THEN 1 ELSE 0 END) AS missing_valid_product_url,
       SUM(CASE WHEN duplicate_title=1 THEN 1 ELSE 0 END) AS rows_with_duplicate_title
FROM jumia_listings;

-- Repeated exact titles
SELECT phone_name, brand, COUNT(*) AS listing_occurrences,
       ROUND(MIN(price_ngn),0) AS lowest_price_ngn,
       ROUND(MAX(price_ngn),0) AS highest_price_ngn
FROM jumia_listings
GROUP BY phone_name, brand
HAVING COUNT(*) > 1
ORDER BY listing_occurrences DESC, brand, phone_name
LIMIT 25;
