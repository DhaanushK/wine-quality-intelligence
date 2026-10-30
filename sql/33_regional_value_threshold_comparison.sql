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
        AVG(average_price) AS benchmark_price,
        AVG(average_rating) AS benchmark_rating,

        AVG(
            CASE WHEN priced_records >= 300
            THEN average_price END
        ) AS benchmark_price_300,

        AVG(
            CASE WHEN priced_records >= 300
            THEN average_rating END
        ) AS benchmark_rating_300

    FROM regional_analysis
),

scored_regions AS (
    SELECT
        r.*,

        CASE
            WHEN r.average_price < b.benchmark_price
             AND r.average_rating > b.benchmark_rating
            THEN ROUND(
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
            )
        END AS score_100,

        CASE
            WHEN r.priced_records >= 300
             AND r.average_price < b.benchmark_price_300
             AND r.average_rating > b.benchmark_rating_300
            THEN ROUND(
                (
                    (
                        (b.benchmark_price_300 - r.average_price)
                        / b.benchmark_price_300
                    ) * 100
                    +
                    (
                        (r.average_rating - b.benchmark_rating_300)
                        / b.benchmark_rating_300
                    ) * 100
                ) / 2,
                2
            )
        END AS score_300

    FROM regional_analysis r
    CROSS JOIN benchmarks b
)

SELECT
    country,
    province,
    region_1,
    priced_records,

    score_100,
    score_300,

    CASE
        WHEN score_100 IS NOT NULL
         AND score_300 IS NOT NULL
        THEN ROUND(score_300 - score_100, 2)
        ELSE NULL
    END AS score_difference,

    CASE
        WHEN score_100 IS NOT NULL
         AND score_300 IS NOT NULL
        THEN 'Qualified under both thresholds'

        WHEN score_100 IS NOT NULL
         AND score_300 IS NULL
        THEN 'Qualified only under 100 threshold'

        ELSE 'Not qualified'
    END AS qualification_status

FROM scored_regions

WHERE score_100 IS NOT NULL

ORDER BY score_100 DESC;