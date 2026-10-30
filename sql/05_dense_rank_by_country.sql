-- Project: Wine Quality Intelligence
-- Analysis: Top Three Price Ranks by Country
-- Purpose:
-- Use DENSE_RANK to avoid gaps after tied prices.
USE wine_quality_intelligence;

WITH ranked_wines AS (
    SELECT
        country,
        winery,
        variety,
        points,
        price,
        DENSE_RANK() OVER (
            PARTITION BY country
            ORDER BY price DESC
        ) AS price_rank
    FROM wine_reviews
    WHERE country IS NOT NULL
      AND price IS NOT NULL
)
SELECT
    country,
    winery,
    variety,
    points,
    price,
    price_rank
FROM ranked_wines
WHERE price_rank <= 3
ORDER BY country, price_rank, price DESC;
