USE wine_quality_intelligence;

WITH global_benchmarks AS (
    SELECT
        AVG(price) AS global_avg_price,
        AVG(points) AS global_avg_rating
    FROM wine_reviews
    WHERE price IS NOT NULL
      AND price > 0
      AND points IS NOT NULL
),

country_analysis AS (
    SELECT
        country,

        COUNT(*) AS total_reviews,

        COUNT(price) AS priced_reviews,

        AVG(price) AS average_price,

        AVG(points) AS average_rating

    FROM wine_reviews

    WHERE country IS NOT NULL
      AND price IS NOT NULL
      AND price > 0
      AND points IS NOT NULL

    GROUP BY country

    HAVING COUNT(price) >= 100
)

SELECT
    c.country,
    c.priced_reviews,

    ROUND(c.average_price, 2) AS average_price,
    ROUND(c.average_rating, 2) AS average_rating,

    ROUND(
        c.average_price - b.global_avg_price, 2
    ) AS price_difference,

    ROUND(
        c.average_rating - b.global_avg_rating, 2
    ) AS rating_difference,

    ROUND(
        (
            (b.global_avg_price - c.average_price)
            / b.global_avg_price
        ) * 100, 2
    ) AS price_advantage_percentage,

    ROUND(
        c.average_rating - b.global_avg_rating, 2
    ) AS rating_advantage_points

FROM country_analysis c

CROSS JOIN global_benchmarks b

ORDER BY
    price_advantage_percentage DESC;