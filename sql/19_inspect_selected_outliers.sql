USE wine_quality_intelligence;

SELECT
    review_id,
    country,
    winery,
    variety,
    designation,
    points,
    price,
    description
FROM wine_reviews
WHERE
    (country = 'US'
     AND winery = 'Blair'
     AND price = 2013)

    OR

    (country = 'Germany'
     AND winery = 'Robert Weil'
     AND price = 775)

ORDER BY country, winery, price DESC;