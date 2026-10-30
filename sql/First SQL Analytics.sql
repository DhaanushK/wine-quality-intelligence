USE wine_quality_intelligence;

SELECT
    country,
    COUNT(*) AS total_wine_records,
    COUNT(price) AS records_with_price,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(points), 2) AS average_rating,
    MIN(price) AS minimum_price,
    MAX(price) AS maximum_price
FROM wine_reviews
WHERE country IS NOT NULL
GROUP BY country
HAVING COUNT(price) >= 100
ORDER BY average_rating DESC;

-- find the best-rated varieties within each country
SELECT
    country,
    variety,
    COUNT(*) AS total_records,
    ROUND(AVG(points), 2) AS average_rating,
    ROUND(AVG(price), 2) AS average_price
FROM wine_reviews
WHERE country IS NOT NULL
  AND variety IS NOT NULL
GROUP BY country, variety
HAVING COUNT(*) >= 30
ORDER BY average_rating DESC, total_records DESC
LIMIT 20;

-- find country–variety combinations whose average rating is above the overall average rating.
SELECT
    country,
    variety,
    COUNT(*) AS total_records,
    ROUND(AVG(points), 2) AS average_rating,
    ROUND(AVG(price), 2) AS average_price
FROM wine_reviews
WHERE country IS NOT NULL
  AND variety IS NOT NULL
GROUP BY country, variety
HAVING COUNT(*) >= 30
   AND AVG(points) > (
       SELECT AVG(points)
       FROM wine_reviews
   )
ORDER BY average_rating DESC, total_records DESC
LIMIT 20;

-- Find the overall average rating
SELECT
    ROUND(AVG(points), 4) AS overall_average_rating
FROM wine_reviews;

-- find country–variety combinations whose average rating is above their own country's average rating.
SELECT
    cv.country,
    cv.variety,
    cv.total_records,
    ROUND(cv.average_rating, 2) AS average_rating,
    ROUND(cv.average_price, 2) AS average_price
FROM (
    SELECT
        country,
        variety,
        COUNT(*) AS total_records,
        AVG(points) AS average_rating,
        AVG(price) AS average_price
    FROM wine_reviews
    WHERE country IS NOT NULL
      AND variety IS NOT NULL
    GROUP BY country, variety
    HAVING COUNT(*) >= 30
) AS cv
WHERE cv.average_rating > (
    SELECT AVG(wr.points)
    FROM wine_reviews AS wr
    WHERE wr.country = cv.country
)
ORDER BY cv.average_rating DESC
LIMIT 20;

-- Check the country benchmark
SELECT
    country,
    COUNT(*) AS total_records,
    ROUND(AVG(points), 2) AS country_average_rating
FROM wine_reviews
WHERE country = 'Italy'
GROUP BY country;

-- Verify the filtering condition
WITH country_averages AS (
    SELECT
        country,
        AVG(points) AS country_average_rating
    FROM wine_reviews
    WHERE country IS NOT NULL
    GROUP BY country
),
variety_averages AS (
    SELECT
        country,
        variety,
        COUNT(*) AS total_records,
        AVG(points) AS variety_average_rating,
        AVG(price) AS average_price
    FROM wine_reviews
    WHERE country IS NOT NULL
      AND variety IS NOT NULL
    GROUP BY country, variety
    HAVING COUNT(*) >= 30
)
SELECT
    v.country,
    v.variety,
    v.total_records,
    ROUND(v.variety_average_rating, 2) AS variety_average_rating,
    ROUND(c.country_average_rating, 2) AS country_average_rating,
    ROUND(v.average_price, 2) AS average_price
FROM variety_averages AS v
JOIN country_averages AS c
    ON v.country = c.country
WHERE v.variety_average_rating <= c.country_average_rating
ORDER BY v.variety_average_rating DESC
LIMIT 10;

-- find affordable, highly rated wines
SELECT
    country,
    variety,
    COUNT(*) AS priced_records,
    ROUND(AVG(points), 2) AS average_rating,
    ROUND(AVG(price), 2) AS average_price
FROM wine_reviews
WHERE country IS NOT NULL
  AND variety IS NOT NULL
  AND price IS NOT NULL
  AND price > 0
GROUP BY country, variety
HAVING COUNT(*) >= 20
   AND AVG(points) >= 90
   AND AVG(price) <= 30
ORDER BY average_rating DESC, average_price ASC
LIMIT 20;

-- broaden the price threshold to $35
SELECT
    country,
    variety,
    COUNT(*) AS priced_records,
    ROUND(AVG(points), 2) AS average_rating,
    ROUND(AVG(price), 2) AS average_price
FROM wine_reviews
WHERE country IS NOT NULL
  AND variety IS NOT NULL
  AND price IS NOT NULL
  AND price > 0
GROUP BY country, variety
HAVING COUNT(*) >= 20
   AND AVG(points) >= 90
   AND AVG(price) <= 35
ORDER BY average_rating DESC, average_price ASC
LIMIT 20;

-- save this as a reusable SQL analysis
SELECT
    country,
    variety,
    COUNT(*) AS priced_records,
    ROUND(AVG(points), 2) AS average_rating,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(points) - 90, 2) AS points_above_threshold
FROM wine_reviews
WHERE country IS NOT NULL
  AND variety IS NOT NULL
  AND price IS NOT NULL
  AND price > 0
GROUP BY country, variety
HAVING COUNT(*) >= 20
   AND AVG(points) >= 90
   AND AVG(price) <= 35
ORDER BY average_rating DESC, average_price ASC;