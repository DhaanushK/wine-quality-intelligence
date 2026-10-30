USE wine_quality_intelligence;

SELECT
    CASE
        WHEN price <= 15 THEN '$0-$15'
        WHEN price <= 30 THEN '$15-$30'
        WHEN price <= 50 THEN '$30-$50'
        WHEN price <= 100 THEN '$50-$100'
        ELSE 'Above $100'
    END AS price_band,

    COUNT(*) AS total_records,

    SUM(CASE
        WHEN points BETWEEN 95 AND 100 THEN 1
        ELSE 0
    END) AS records_rated_95_plus,

    ROUND(
        100.0 * SUM(CASE
            WHEN points BETWEEN 95 AND 100 THEN 1
            ELSE 0
        END) / COUNT(*),
        2
    ) AS percentage_rated_95_plus

FROM wine_reviews
WHERE price IS NOT NULL
  AND price > 0
  AND points BETWEEN 80 AND 100

GROUP BY
    CASE
        WHEN price <= 15 THEN '$0-$15'
        WHEN price <= 30 THEN '$15-$30'
        WHEN price <= 50 THEN '$30-$50'
        WHEN price <= 100 THEN '$50-$100'
        ELSE 'Above $100'
    END

ORDER BY MIN(price);