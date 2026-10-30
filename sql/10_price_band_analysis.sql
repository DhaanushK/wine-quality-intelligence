USE wine_quality_intelligence;

SELECT
    CASE
        WHEN price <= 15 THEN '01. $0-$15'
        WHEN price <= 30 THEN '02. $15-$30'
        WHEN price <= 50 THEN '03. $30-$50'
        WHEN price <= 100 THEN '04. $50-$100'
        ELSE '05. Above $100'
    END AS price_band,
    COUNT(*) AS wine_records,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(points), 2) AS average_rating,
    MIN(points) AS lowest_rating,
    MAX(points) AS highest_rating
FROM wine_reviews
WHERE price IS NOT NULL
  AND price > 0
  AND points IS NOT NULL
GROUP BY
    CASE
        WHEN price <= 15 THEN '01. $0-$15'
        WHEN price <= 30 THEN '02. $15-$30'
        WHEN price <= 50 THEN '03. $30-$50'
        WHEN price <= 100 THEN '04. $50-$100'
        ELSE '05. Above $100'
    END
ORDER BY price_band;