SELECT 
    m.movie_id,
    m.title,
    m.year,
    m.poster_link,
    AVG(mr.rating) AS imdb_rating
FROM movies m
LEFT JOIN movie_rating mr ON m.movie_id = mr.movie_id
GROUP BY m.movie_id
ORDER BY imdb_rating DESC
LIMIT 10;