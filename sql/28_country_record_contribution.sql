USE wine_quality_intelligence;

WITH regional_counts AS (
    SELECT
        country,
        province,
        region_1,
        COUNT(price) AS priced_records
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

country_summary AS (
    SELECT
        country,
        COUNT(*) AS qualifying_regions,
        SUM(priced_records) AS total_priced_records
    FROM regional_counts
    GROUP BY country
)

SELECT
    country,
    qualifying_regions,
    total_priced_records,

    ROUND(
        total_priced_records * 100.0
        / SUM(total_priced_records) OVER (),
        2
    ) AS record_contribution_percentage

FROM country_summary
ORDER BY record_contribution_percentage DESC;