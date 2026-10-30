USE wine_quality_intelligence;

WITH regional_analysis AS (
    SELECT
        country,
        province,
        region_1,

        COUNT(*) AS total_reviews,

        AVG(price) AS average_price,
        AVG(points) AS average_rating,

        SUM(CASE
            WHEN points BETWEEN 80 AND 84 THEN 1
            ELSE 0
        END) AS ratings_80_84,

        SUM(CASE
            WHEN points BETWEEN 85 AND 89 THEN 1
            ELSE 0
        END) AS ratings_85_89,

        SUM(CASE
            WHEN points BETWEEN 90 AND 94 THEN 1
            ELSE 0
        END) AS ratings_90_94,

        SUM(CASE
            WHEN points BETWEEN 95 AND 100 THEN 1
            ELSE 0
        END) AS ratings_95_100

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
),

benchmarks AS (
    SELECT
        AVG(average_price) AS benchmark_price,
        AVG(average_rating) AS benchmark_rating
    FROM regional_analysis
),

eligible_regions AS (
    SELECT r.*
    FROM regional_analysis r
    CROSS JOIN benchmarks b
    WHERE r.average_price < b.benchmark_price
      AND r.average_rating > b.benchmark_rating
)

SELECT
    country,
    province,
    region_1,
    total_reviews,

    ROUND(average_price, 2) AS average_price,
    ROUND(average_rating, 2) AS average_rating,

    ratings_80_84,
    ratings_85_89,
    ratings_90_94,
    ratings_95_100,

    ROUND(
        (
            ratings_90_94 + ratings_95_100
        ) * 100.0 / total_reviews,
        2
    ) AS percentage_rated_90_plus

FROM eligible_regions

ORDER BY percentage_rated_90_plus DESC;