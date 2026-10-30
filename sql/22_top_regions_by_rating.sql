USE wine_quality_intelligence;

SELECT
    country,
    province,
    region_1,
    COUNT(*) AS wine_records,
    COUNT(price) AS priced_records,
    ROUND(AVG(points), 2) AS average_rating,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(MIN(price), 2) AS minimum_price,
    ROUND(MAX(price), 2) AS maximum_price

FROM wine_reviews

WHERE country IS NOT NULL
  AND province IS NOT NULL
  AND region_1 IS NOT NULL
  AND points IS NOT NULL

GROUP BY
    country,
    province,
    region_1

HAVING COUNT(price) >= 100

ORDER BY average_rating DESC,
         priced_records DESC

LIMIT 20;