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
      AND points IS NOT NULL
    GROUP BY country
    HAVING COUNT(price) >= 100
)

SELECT
    c.country,
    c.total_reviews,
    c.priced_reviews,

    ROUND(c.average_price, 2) AS average_price,
    ROUND(c.average_rating, 2) AS average_rating,

    ROUND(b.global_avg_price, 2) AS global_average_price,
    ROUND(b.global_avg_rating, 2) AS global_average_rating,

    CASE
        WHEN c.average_price < b.global_avg_price
         AND c.average_rating > b.global_avg_rating
            THEN 'Lower Price - Higher Rating'

        WHEN c.average_price < b.global_avg_price
         AND c.average_rating <= b.global_avg_rating
            THEN 'Lower Price - Lower Rating'

        WHEN c.average_price >= b.global_avg_price
         AND c.average_rating > b.global_avg_rating
            THEN 'Higher Price - Higher Rating'

        ELSE 'Higher Price - Lower Rating'
    END AS country_positioning

FROM country_analysis c
CROSS JOIN global_benchmarks b

WHERE c.priced_reviews >= 100

ORDER BY
    country_positioning,
    c.average_rating DESC;