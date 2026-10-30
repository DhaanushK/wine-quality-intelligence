
-- Project: Wine Quality Intelligence
-- Analysis: Affordable, Highly Rated Wine Varieties
-- Purpose:
-- Identify country-variety combinations with:
-- 1. At least 20 records with valid, positive prices
-- 2. Average rating >= 90
-- 3. Average price <= $35
USE wine_quality_intelligence;

SELECT
    country,
    variety,
    COUNT(*) AS priced_records,
    ROUND(AVG(points), 2) AS average_rating,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(points) - 90, 2) AS points_above_threshold
FROM wine_reviews
WHERE country IS NOT NULL
  AND variety IS NOT NULL
  AND price IS NOT NULL
  AND price > 0
GROUP BY country, variety
HAVING COUNT(*) >= 20
   AND AVG(points) >= 90
   AND AVG(price) <= 35
ORDER BY average_rating DESC, average_price ASC;
