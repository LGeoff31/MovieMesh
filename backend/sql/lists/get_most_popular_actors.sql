SELECT a.actor_id,
       a.name,
       COUNT(mc.movie_id) AS num_movies
FROM actors a
JOIN movie_cast mc ON a.actor_id = mc.actor_id
GROUP BY a.actor_id, a.name
ORDER BY num_movies DESC
LIMIT 10;