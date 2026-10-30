USE wine_quality_intelligence;

WITH country_price_stats AS (
    SELECT
        country,
        price,
        ROW_NUMBER() OVER (
            PARTITION BY country
            ORDER BY price
        ) AS row_num,
        COUNT(*) OVER (
            PARTITION BY country
        ) AS country_count
    FROM wine_reviews
    WHERE country IS NOT NULL
      AND price IS NOT NULL
      AND price > 0
)
SELECT
    country,
    MAX(country_count) AS priced_records,
    ROUND(AVG(
        CASE
            WHEN row_num IN (
                FLOOR((country_count + 1) / 2),
                FLOOR((country_count + 2) / 2)
            )
            THEN price
        END
    ), 2) AS median_price,
    ROUND(AVG(price), 2) AS average_price
FROM country_price_stats
GROUP BY country
HAVING MAX(country_count) >= 100
ORDER BY median_price;