-- Project: Wine Quality Intelligence
-- Analysis: Highest-Rated Wine Records by Country
-- Purpose:
-- Rank wines by critic rating within each country.
-- When ratings tie, higher-priced records appear first.

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
            ORDER BY points DESC, price DESC
        ) AS rating_rank
    FROM wine_reviews
    WHERE country IS NOT NULL
)
SELECT
    country,
    winery,
    variety,
    points,
    price,
    rating_rank
FROM ranked_wines
WHERE rating_rank <= 3
ORDER BY country, rating_rank;
