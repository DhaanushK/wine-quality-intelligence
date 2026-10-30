USE wine_quality_intelligence;

WITH global_average AS (
    SELECT
        AVG(points) AS overall_average_rating
    FROM wine_reviews
    WHERE points IS NOT NULL
),

regional_analysis AS (
    SELECT
        country,
        province,
        region_1,
        COUNT(*) AS wine_records,
        COUNT(price) AS priced_records,
        AVG(points) AS average_rating,
        AVG(price) AS average_price
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
)

SELECT
    r.country,
    r.province,
    r.region_1,
    r.priced_records,
    ROUND(r.average_rating, 2) AS average_rating,
    ROUND(g.overall_average_rating, 2) AS global_average_rating,
    ROUND(
        r.average_rating - g.overall_average_rating,
        2
    ) AS rating_difference,
    ROUND(r.average_price, 2) AS average_price

FROM regional_analysis AS r
CROSS JOIN global_average AS g

WHERE r.average_rating > g.overall_average_rating

ORDER BY rating_difference DESC
LIMIT 20;