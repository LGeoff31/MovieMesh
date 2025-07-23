SELECT a.*, SUM(m.gross_usd) AS total_gross
FROM actors a
JOIN movie_cast mc ON a.actor_id = mc.actor_id
JOIN movies m ON mc.movie_id = m.movie_id
WHERE a.actor_id = :id
GROUP BY a.actor_id;