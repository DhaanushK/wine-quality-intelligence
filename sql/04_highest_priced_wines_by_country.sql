-- Project: Wine Quality Intelligence
-- Analysis: Highest-Priced Wine Records by Country
-- Purpose:
-- Rank wine records by price within each country.
USE wine_quality_intelligence;

WITH ranked_wines AS (
    SELECT
        country,
        winery,
        variety,
        points,
        price,
        RANK() OVER (
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
ORDER BY country, price_rank;
