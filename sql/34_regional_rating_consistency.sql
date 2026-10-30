USE wine_quality_intelligence;

SELECT
    country,
    province,
    region_1,

    COUNT(*) AS total_reviews,
    COUNT(price) AS priced_records,

    ROUND(AVG(points), 2) AS average_rating,
    ROUND(STDDEV_POP(points), 2) AS rating_std_deviation,

    MIN(points) AS minimum_rating,
    MAX(points) AS maximum_rating

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

HAVING COUNT(price) >= 300
   AND AVG(price) < 35.57
   AND AVG(points) > 88.02

ORDER BY rating_std_deviation ASC;