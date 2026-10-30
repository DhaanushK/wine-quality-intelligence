USE wine_quality_intelligence;

WITH ranked_prices AS (
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
),

country_quartiles AS (
    SELECT
        country,
        MAX(CASE
            WHEN row_num = CEIL(country_count * 0.25)
            THEN price
        END) AS q1,
        MAX(CASE
            WHEN row_num = CEIL(country_count * 0.75)
            THEN price
        END) AS q3
    FROM ranked_prices
    GROUP BY country
    HAVING COUNT(*) >= 100
),

outlier_limits AS (
    SELECT
        country,
        q1,
        q3,
        q3 + 1.5 * (q3 - q1) AS upper_limit
    FROM country_quartiles
)

SELECT
    w.country,
    w.winery,
    w.variety,
    w.points,
    w.price,
    o.upper_limit
FROM wine_reviews AS w
JOIN outlier_limits AS o
    ON w.country = o.country
WHERE w.price > o.upper_limit
ORDER BY w.price DESC
LIMIT 30;