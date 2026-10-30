USE wine_quality_intelligence;

SELECT
    CASE
        WHEN points BETWEEN 80 AND 84 THEN '80-84'
        WHEN points BETWEEN 85 AND 89 THEN '85-89'
        WHEN points BETWEEN 90 AND 94 THEN '90-94'
        WHEN points BETWEEN 95 AND 100 THEN '95-100'
    END AS rating_band,

    COUNT(*) AS review_count,

    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM wine_reviews),
        2
    ) AS percentage_of_reviews,

    ROUND(AVG(points), 2) AS average_rating

FROM wine_reviews

WHERE points IS NOT NULL

GROUP BY rating_band

ORDER BY MIN(points);