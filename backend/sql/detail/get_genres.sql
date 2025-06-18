SELECT g.name
FROM genres g
JOIN movie_genres mg USING(genre_id)
WHERE mg.movie_id = :id; 