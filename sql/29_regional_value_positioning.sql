USE wine_quality_intelligence;

WITH regional_analysis AS (
    SELECT
        country,
        province,
        region_1,
        COUNT(price) AS priced_records,
        AVG(price) AS average_price,
        AVG(points) AS average_rating
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
),

benchmarks AS (
    SELECT
        AVG(average_price) AS overall_regional_price,
        AVG(average_rating) AS overall_regional_rating
    FROM regional_analysis
)

SELECT
    r.country,
    r.province,
    r.region_1,
    r.priced_records,

    ROUND(r.average_price, 2) AS average_price,
    ROUND(r.average_rating, 2) AS average_rating,

    ROUND(
        r.average_price - b.overall_regional_price,
        2
    ) AS price_difference,

    ROUND(
        r.average_rating - b.overall_regional_rating,
        2
    ) AS rating_difference

FROM regional_analysis r
CROSS JOIN benchmarks b

WHERE r.average_price < b.overall_regional_price
  AND r.average_rating > b.overall_regional_rating

ORDER BY
    r.average_rating DESC,
    r.average_price ASC;