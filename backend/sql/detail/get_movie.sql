SELECT m.movie_id,
       m.title,
       m.year,
       mr.rating as imdb_rating,
       m.gross_usd,
       m.certificate,
       m.runtime_min,
       m.poster_link,
       m.overview
FROM movies m
LEFT JOIN movie_rating mr ON m.movie_id = mr.movie_id
WHERE m.movie_id = :id
LIMIT 1