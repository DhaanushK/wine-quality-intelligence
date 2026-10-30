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

benchmarks AS (
    SELECT
        AVG(average_price) AS overall_regional_price,
        AVG(average_rating) AS overall_regional_rating
    FROM regional_analysis
),

eligible_regions AS (
    SELECT
        r.*,
        b.overall_regional_price,
        b.overall_regional_rating
    FROM regional_analysis r
    CROSS JOIN benchmarks b
    WHERE r.average_price < b.overall_regional_price
      AND r.average_rating > b.overall_regional_rating
),

scored_regions AS (
    SELECT
        *,
        (
            (overall_regional_price - average_price)
            / overall_regional_price
        ) * 100 AS price_advantage,

        (
            (average_rating - overall_regional_rating)
            / overall_regional_rating
        ) * 100 AS rating_advantage
    FROM eligible_regions
)

SELECT
    country,
    province,
    region_1,
    priced_records,

    ROUND(average_price, 2) AS average_price,
    ROUND(average_rating, 2) AS average_rating,

    ROUND(price_advantage, 2) AS price_advantage_percentage,
    ROUND(rating_advantage, 2) AS rating_advantage_percentage,

    ROUND(
        (price_advantage + rating_advantage) / 2,
        2
    ) AS regional_value_score

FROM scored_regions
ORDER BY regional_value_score DESC;