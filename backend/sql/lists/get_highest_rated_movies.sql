SELECT 
    m.movie_id,
    m.title,
    m.year,
    m.poster_link,
    AVG(r.rating) AS avg_rating
FROM movies m
LEFT JOIN reviews r ON m.movie_id = r.movie_id
GROUP BY m.movie_id
ORDER BY avg_rating DESC
LIMIT 10;