
-- Project: Wine Quality Intelligence
-- Analysis: Country-Level Price and Rating Comparison
-- Purpose:
-- Compare countries by average rating and listed price.
-- Include only countries with at least 100 priced records.
USE wine_quality_intelligence;

SELECT
    country,
    COUNT(*) AS total_records,
    COUNT(price) AS priced_records,
    ROUND(AVG(points), 2) AS average_rating,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(MIN(price), 2) AS minimum_price,
    ROUND(MAX(price), 2) AS maximum_price
FROM wine_reviews
WHERE country IS NOT NULL
GROUP BY country
HAVING COUNT(price) >= 100
ORDER BY average_rating DESC;
