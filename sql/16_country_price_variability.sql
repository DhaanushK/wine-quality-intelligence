USE wine_quality_intelligence;

SELECT
    country,
    COUNT(*) AS priced_records,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(STDDEV_POP(price), 2) AS price_std_deviation,
    ROUND(MIN(price), 2) AS minimum_price,
    ROUND(MAX(price), 2) AS maximum_price
FROM wine_reviews
WHERE country IS NOT NULL
  AND price IS NOT NULL
  AND price > 0
GROUP BY country
HAVING COUNT(*) >= 100
ORDER BY price_std_deviation DESC;