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
)

SELECT
    COUNT(*) AS regions_analysed,

    ROUND(
        (
            AVG(average_price * average_rating)
            - AVG(average_price) * AVG(average_rating)
        )
        /
        (
            STDDEV_POP(average_price)
            * STDDEV_POP(average_rating)
        ),
        4
    ) AS pearson_correlation

FROM regional_analysis;