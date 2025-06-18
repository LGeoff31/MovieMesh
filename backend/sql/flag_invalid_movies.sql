SELECT m.movie_id,
    m.title,
    COUNT(DISTINCT mc.actor_id) AS num_actors,
    COUNT(DISTINCT md.director_id) AS num_directors
FROM movies m
LEFT JOIN movie_cast mc ON mc.movie_id = m.movie_id
LEFT JOIN movie_directors md ON md.movie_id = m.movie_id
GROUP BY m.movie_id, m.title
HAVING num_actors = 0 OR num_directors = 0;
