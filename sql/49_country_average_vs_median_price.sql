USE wine_quality_intelligence;

WITH country_prices AS (
    SELECT
        country,
        price,

        ROW_NUMBER() OVER (
            PARTITION BY country
            ORDER BY price
        ) AS price_position,

        COUNT(*) OVER (
            PARTITION BY country
        ) AS country_count

    FROM wine_reviews

    WHERE country IS NOT NULL
      AND price IS NOT NULL
      AND price > 0
),

country_summary AS (
    SELECT
        country,

        COUNT(*) AS priced_reviews,

        AVG(price) AS average_price,

        AVG(
            CASE
                WHEN price_position IN (
                    FLOOR((country_count + 1) / 2),
                    FLOOR((country_count + 2) / 2)
                )
                THEN price
            END
        ) AS median_price

    FROM country_prices

    GROUP BY country

    HAVING COUNT(*) >= 100
)

SELECT
    country,
    priced_reviews,

    ROUND(average_price, 2) AS average_price,

    ROUND(median_price, 2) AS median_price,

    ROUND(
        average_price - median_price, 2
    ) AS mean_median_difference,

    ROUND(
        average_price / median_price, 2
    ) AS mean_median_ratio

FROM country_summary

ORDER BY mean_median_difference DESC;