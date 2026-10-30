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
        q1,
        q3,
        q3 - q1 AS iqr,
        q3 + 1.5 * (q3 - q1) AS upper_limit
    FROM country_quartiles
)

SELECT
    w.country,
    o.priced_records,
    o.q1,
    o.q3,
    ROUND(o.iqr, 2) AS iqr,
    ROUND(o.upper_limit, 2) AS upper_outlier_limit,
    COUNT(*) AS high_price_records,
    ROUND(MAX(w.price), 2) AS highest_flagged_price

FROM wine_reviews AS w

JOIN outlier_limits AS o
    ON w.country = o.country

WHERE w.price > o.upper_limit

GROUP BY
    w.country,
    o.priced_records,
    o.q1,
    o.q3,
    o.iqr,
    o.upper_limit

ORDER BY high_price_records DESC;