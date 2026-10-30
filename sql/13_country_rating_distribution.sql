USE wine_quality_intelligence;

SELECT
    country,
    COUNT(*) AS total_records,

    SUM(CASE
        WHEN points BETWEEN 90 AND 94 THEN 1
        ELSE 0
    END) AS records_rated_90_94,

    SUM(CASE
        WHEN points >= 95 THEN 1
        ELSE 0
    END) AS records_rated_95_plus,

    ROUND(AVG(points), 2) AS average_rating,

    ROUND(
        100.0 * SUM(CASE
            WHEN points >= 95 THEN 1
            ELSE 0
        END) / COUNT(*),
        2
    ) AS percentage_rated_95_plus

FROM wine_reviews
WHERE country IS NOT NULL
  AND points IS NOT NULL

GROUP BY country
HAVING COUNT(*) >= 100

ORDER BY percentage_rated_95_plus DESC,
         total_records DESC;