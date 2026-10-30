USE wine_quality_intelligence;

WITH country_prices AS (
    SELECT
        country,
        price,
        points,

        ROW_NUMBER() OVER (
            PARTITION BY country
            ORDER BY price
        ) AS price_position,

        COUNT(*) OVER (
            PARTITION BY country
        ) AS country_count

    FROM wine_reviews

    WHERE country IS NOT NULL
      AND price IS NOT NULL
      AND price > 0
      AND points IS NOT NULL
),

country_summary AS (
    SELECT
        country,

        COUNT(*) AS priced_reviews,

        AVG(price) AS average_price,

        AVG(points) AS average_rating,

        AVG(
            CASE
                WHEN price_position IN (
                    FLOOR((country_count + 1) / 2),
                    FLOOR((country_count + 2) / 2)
                )
                THEN price
            END
        ) AS median_price,

        SUM(
            CASE WHEN points >= 90 THEN 1 ELSE 0 END
        ) AS high_rating_reviews,

        STDDEV_POP(price) AS price_stddev

    FROM country_prices

    GROUP BY country

    HAVING COUNT(*) >= 100
),

global_benchmarks AS (
    SELECT
        AVG(price) AS global_avg_price,
        AVG(points) AS global_avg_rating
    FROM wine_reviews
    WHERE price IS NOT NULL
      AND price > 0
      AND points IS NOT NULL
)

SELECT
    c.country,

    c.priced_reviews,

    ROUND(c.average_price, 2) AS average_price,

    ROUND(c.median_price, 2) AS median_price,

    ROUND(c.average_rating, 2) AS average_rating,

    ROUND(
        c.high_rating_reviews * 100.0
        / c.priced_reviews,
        2
    ) AS percentage_rated_90_plus,

    ROUND(c.price_stddev, 2) AS price_stddev,

    ROUND(
        (
            b.global_avg_price - c.average_price
        ) / b.global_avg_price * 100,
        2
    ) AS price_advantage_percentage,

    ROUND(
        c.average_rating - b.global_avg_rating,
        2
    ) AS rating_advantage_points

FROM country_summary c

CROSS JOIN global_benchmarks b

ORDER BY c.average_rating DESC;