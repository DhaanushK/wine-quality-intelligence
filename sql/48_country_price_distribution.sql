USE wine_quality_intelligence;

SELECT
    country,

    COUNT(price) AS priced_reviews,

    ROUND(AVG(price), 2) AS average_price,

    ROUND(
        MIN(price), 2
    ) AS minimum_price,

    ROUND(
        MAX(price), 2
    ) AS maximum_price,

    ROUND(
        STDDEV_POP(price), 2
    ) AS price_standard_deviation,

    ROUND(
        AVG(price) - MIN(price), 2
    ) AS average_minus_minimum

FROM wine_reviews

WHERE country IS NOT NULL
  AND price IS NOT NULL
  AND price > 0

GROUP BY country

HAVING COUNT(price) >= 100

ORDER BY average_price DESC;