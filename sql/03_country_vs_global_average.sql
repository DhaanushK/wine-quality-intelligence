-- Project: Wine Quality Intelligence
-- Analysis: Country Ratings vs Global Average
-- Purpose:
-- Find countries with above-average critic ratings.

USE wine_quality_intelligence;

SELECT
    country,
    COUNT(*) AS total_records,
    ROUND(AVG(points), 2) AS country_average_rating,
    ROUND(
        (SELECT AVG(points) FROM wine_reviews),
        2
    ) AS global_average_rating,
    ROUND(
        AVG(points) - (SELECT AVG(points) FROM wine_reviews),
        2
    ) AS difference_from_global
FROM wine_reviews
WHERE country IS NOT NULL
GROUP BY country
HAVING COUNT(*) >= 100
   AND AVG(points) > (
       SELECT AVG(points)
       FROM wine_reviews
   )
ORDER BY difference_from_global DESC;
