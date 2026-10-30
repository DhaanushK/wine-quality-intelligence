USE wine_quality_intelligence;

WITH regional_analysis AS (
    SELECT
        country,
        province,
        region_1,
        COUNT(price) AS priced_records,
        AVG(price) AS average_price,
        AVG(points) AS average_rating,
        STDDEV_POP(points) AS rating_std_deviation
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

scored_regions AS (
    SELECT
        r.*,

        ROUND(
            (
                (
                    (b.benchmark_price - r.average_price)
                    / b.benchmark_price
                ) * 100
                +
                (
                    (r.average_rating - b.benchmark_rating)
                    / b.benchmark_rating
                ) * 100
            ) / 2,
            2
        ) AS regional_value_score

    FROM regional_analysis r
    CROSS JOIN benchmarks b

    WHERE r.average_price < b.benchmark_price
      AND r.average_rating > b.benchmark_rating
)

SELECT
    country,
    province,
    region_1,
    priced_records,

    ROUND(average_price, 2) AS average_price,
    ROUND(average_rating, 2) AS average_rating,
    ROUND(rating_std_deviation, 2) AS rating_std_deviation,
    regional_value_score,

    CASE
        WHEN rating_std_deviation <= 2.50
            THEN 'Lower rating variation'
        WHEN rating_std_deviation <= 3.00
            THEN 'Moderate rating variation'
        ELSE 'Higher rating variation'
    END AS consistency_category

FROM scored_regions

ORDER BY
    regional_value_score DESC,
    rating_std_deviation ASC;