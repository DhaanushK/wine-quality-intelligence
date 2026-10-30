-- Project: Wine Quality Intelligence
-- Analysis: Affordable, Highly Rated Records by Country
-- Criteria: Rating >= 95, price > 0 and <= $30

USE wine_quality_intelligence;

SELECT
    country,
    COUNT(*) AS qualifying_records,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(points), 2) AS average_rating,
    MIN(price) AS lowest_price,
    MAX(price) AS highest_price
FROM wine_reviews
WHERE country IS NOT NULL
  AND price IS NOT NULL
  AND price > 0
  AND price <= 30
  AND points >= 95
GROUP BY country
ORDER BY qualifying_records DESC, average_rating DESC;
