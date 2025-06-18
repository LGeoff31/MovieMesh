SELECT movie_id,
    title,
    year,
    imdb_rating,
    certificate,
    runtime_min,
    poster_link
FROM movies
WHERE title LIKE :pat
ORDER BY year DESC
LIMIT 30;