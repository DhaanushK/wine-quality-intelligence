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
        MAX(country_count) AS priced_records,
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
    HAVING MAX(country_count) >= 100
),

outlier_limits AS (
    SELECT
        country,
        priced_records,
        q3 + 1.5 * (q3 - q1) AS upper_limit
    FROM country_quartiles
)

SELECT
    w.country,
    COUNT(*) AS priced_records,

    SUM(CASE
        WHEN w.price > o.upper_limit THEN 1
        ELSE 0
    END) AS flagged_records,

    ROUND(
        100.0 * SUM(CASE
            WHEN w.price > o.upper_limit THEN 1
            ELSE 0
        END) / COUNT(*),
        2
    ) AS flagged_percentage,

    ROUND(AVG(w.price), 2) AS average_price,
    MAX(w.price) AS maximum_price

FROM wine_reviews AS w

JOIN outlier_limits AS o
    ON w.country = o.country

WHERE w.price IS NOT NULL
  AND w.price > 0

GROUP BY w.country
ORDER BY flagged_percentage DESC;