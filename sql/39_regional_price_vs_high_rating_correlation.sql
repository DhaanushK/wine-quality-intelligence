USE wine_quality_intelligence;

WITH regional_analysis AS (
    SELECT
        country,
        province,
        region_1,

        COUNT(price) AS priced_records,

        AVG(price) AS average_price,

        SUM(
            CASE WHEN points >= 90 THEN 1 ELSE 0 END
        ) AS high_rating_records

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
        AVG(
            high_rating_records * 100.0 / priced_records
        ) AS benchmark_high_rating_percentage
    FROM regional_analysis
),

eligible_regions AS (
    SELECT
        r.*,

        r.high_rating_records * 100.0
            / r.priced_records AS percentage_rated_90_plus

    FROM regional_analysis r
    CROSS JOIN benchmarks b

    WHERE r.average_price < b.benchmark_price
      AND r.average_price < 100000
)

SELECT
    COUNT(*) AS regions_analysed,

    ROUND(
        (
            AVG(average_price * percentage_rated_90_plus)
            -
            AVG(average_price)
            * AVG(percentage_rated_90_plus)
        )
        /
        (
            STDDEV_POP(average_price)
            *
            STDDEV_POP(percentage_rated_90_plus)
        ),
        4
    ) AS price_high_rating_correlation

FROM eligible_regions;