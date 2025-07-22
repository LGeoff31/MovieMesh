SELECT m.movie_id,
       m.title,
       m.year,
       mr.rating as imdb_rating,
       m.certificate,
       m.runtime_min,
       m.poster_link
FROM movies m
LEFT JOIN movie_rating mr ON m.movie_id = mr.movie_id
WHERE mr.rating > 8
ORDER BY RAND()
LIMIT 3;