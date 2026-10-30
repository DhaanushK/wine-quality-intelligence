USE wine_quality_intelligence;

SELECT
    country,
    province,
    region_1,
    COUNT(price) AS priced_records,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(points), 2) AS average_rating
FROM wine_reviews
WHERE country IS NOT NULL
  AND province IS NOT NULL
  AND region_1 IS NOT NULL
  AND price IS NOT NULL
  AND price > 0
  AND points IS NOT NULL
GROUP BY
    country,
    province,
    region_1
HAVING COUNT(price) >= 100
ORDER BY priced_records DESC
LIMIT 20;