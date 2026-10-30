USE wine_quality_intelligence;

WITH regional_analysis AS (
    SELECT
        country,
        province,
        region_1,
        COUNT(price) AS priced_records,
        AVG(price) AS average_price,
        AVG(points) AS average_rating
    FROM wine_reviews
    WHERE country IS NOT NULL
      AND province IS NOT NULL
      AND region_1 IS NOT NULL
      AND price IS NOT NULL
      AND price > 0
      AND points IS NOT NULL
    GROUP BY
        country,
        province,
        region_1
    HAVING COUNT(price) >= 100
),

weighted_stats AS (
    SELECT
        SUM(priced_records) AS total_records,

        SUM(priced_records * average_price)
            / SUM(priced_records) AS weighted_avg_price,

        SUM(priced_records * average_rating)
            / SUM(priced_records) AS weighted_avg_rating,

        SUM(priced_records * average_price * average_rating)
            / SUM(priced_records) AS weighted_avg_product,

        SUM(priced_records * POWER(average_price, 2))
            / SUM(priced_records) AS weighted_avg_price_squared,

        SUM(priced_records * POWER(average_rating, 2))
            / SUM(priced_records) AS weighted_avg_rating_squared

    FROM regional_analysis
)

SELECT
    135 AS regions_analysed,
    total_records,

    ROUND(
        (
            weighted_avg_product
            - weighted_avg_price * weighted_avg_rating
        )
        /
        SQRT(
            (weighted_avg_price_squared
             - POWER(weighted_avg_price, 2))
            *
            (weighted_avg_rating_squared
             - POWER(weighted_avg_rating, 2))
        ),
        4
    ) AS weighted_regional_correlation

FROM weighted_stats;