-- Project: Wine Quality Intelligence
-- Analysis: Affordable, Highly Rated Individual Records
-- Criteria:
-- Rating >= 95
-- Price > 0 and <= $30
-- Rank by rating, then lower price.
USE wine_quality_intelligence;

SELECT
    country,
    winery,
    variety,
    points,
    price,
    RANK() OVER (
        ORDER BY points DESC, price ASC
    ) AS value_rank
FROM wine_reviews
WHERE country IS NOT NULL
  AND price IS NOT NULL
  AND price > 0
  AND price <= 30
  AND points >= 95
ORDER BY points DESC, price ASC
LIMIT 20;
