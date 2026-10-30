USE wine_quality_intelligence;

SELECT
    country,

    COUNT(*) AS total_reviews,

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
    END) AS ratings_95_100,

    ROUND(AVG(points), 2) AS average_rating,

    ROUND(
        SUM(CASE WHEN points >= 90 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS percentage_rated_90_plus

FROM wine_reviews

WHERE country IS NOT NULL
  AND points IS NOT NULL

GROUP BY country

HAVING COUNT(*) >= 100

ORDER BY percentage_rated_90_plus DESC;