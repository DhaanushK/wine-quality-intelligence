USE wine_quality_intelligence;

SELECT
    CASE
        WHEN price <= 15 THEN '$0-$15'
        WHEN price <= 30 THEN '$15-$30'
        WHEN price <= 50 THEN '$30-$50'
        WHEN price <= 100 THEN '$50-$100'
        ELSE 'Above $100'
    END AS price_band,

    CASE
        WHEN points BETWEEN 80 AND 84 THEN '80-84'
        WHEN points BETWEEN 85 AND 89 THEN '85-89'
        WHEN points BETWEEN 90 AND 94 THEN '90-94'
        WHEN points BETWEEN 95 AND 100 THEN '95-100'
    END AS rating_band,

    COUNT(*) AS wine_records

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
    END,
    CASE
        WHEN points BETWEEN 80 AND 84 THEN '80-84'
        WHEN points BETWEEN 85 AND 89 THEN '85-89'
        WHEN points BETWEEN 90 AND 94 THEN '90-94'
        WHEN points BETWEEN 95 AND 100 THEN '95-100'
    END

ORDER BY price_band, rating_band;