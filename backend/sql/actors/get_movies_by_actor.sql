SELECT m.movie_id, m.title, m.year, m.poster_link
FROM movies m
JOIN movie_cast mc ON m.movie_id = mc.movie_id
WHERE mc.actor_id = :id
ORDER BY m.year DESC;