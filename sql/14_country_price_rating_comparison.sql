USE wine_quality_intelligence;

SELECT
    country,
    COUNT(*) AS priced_records,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(points), 2) AS average_rating,
    ROUND(MIN(price), 2) AS minimum_price,
    ROUND(MAX(price), 2) AS maximum_price
FROM wine_reviews
WHERE country IS NOT NULL
  AND price IS NOT NULL
  AND price > 0
  AND points IS NOT NULL
GROUP BY country
HAVING COUNT(*) >= 100
ORDER BY average_rating DESC, priced_records DESC;