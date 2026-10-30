USE wine_quality_intelligence;

WITH global_average AS (
    SELECT
        AVG(points) AS global_avg_rating
    FROM wine_reviews
    WHERE points IS NOT NULL
),

country_analysis AS (
    SELECT
        country,
        COUNT(*) AS total_reviews,
        AVG(points) AS country_avg_rating
    FROM wine_reviews
    WHERE country IS NOT NULL
      AND points IS NOT NULL
    GROUP BY country
    HAVING COUNT(*) >= 100
)

SELECT
    c.country,
    c.total_reviews,

    ROUND(c.country_avg_rating, 2)
        AS country_average_rating,

    ROUND(g.global_avg_rating, 2)
        AS global_average_rating,

    ROUND(
        c.country_avg_rating - g.global_avg_rating,
        2
    ) AS rating_difference,

    CASE
        WHEN c.country_avg_rating > g.global_avg_rating
            THEN 'Above Global Average'
        WHEN c.country_avg_rating < g.global_avg_rating
            THEN 'Below Global Average'
        ELSE 'Equal to Global Average'
    END AS performance_category

FROM country_analysis c
CROSS JOIN global_average g

ORDER BY rating_difference DESC;