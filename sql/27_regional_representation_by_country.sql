USE wine_quality_intelligence;

WITH regional_counts AS (
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
)

SELECT
    country,
    COUNT(*) AS qualifying_regions,
    SUM(priced_records) AS total_priced_records,
    ROUND(AVG(average_price), 2) AS average_of_regional_prices,
    ROUND(AVG(average_rating), 2) AS average_of_regional_ratings
FROM regional_counts
GROUP BY country
ORDER BY qualifying_regions DESC;