USE wine_quality_intelligence;

SELECT
    COUNT(*) AS total_reviews,

    COUNT(DISTINCT country) AS unique_countries,

    COUNT(DISTINCT variety) AS unique_varieties,

    COUNT(DISTINCT winery) AS unique_wineries,

    COUNT(price) AS reviews_with_price,

    SUM(
        CASE WHEN price IS NULL THEN 1 ELSE 0 END
    ) AS missing_prices,

    ROUND(AVG(points), 2) AS average_rating,

    MIN(points) AS minimum_rating,

    MAX(points) AS maximum_rating,

    ROUND(AVG(price), 2) AS average_price,

    MIN(price) AS minimum_price,

    MAX(price) AS maximum_price

FROM wine_reviews;