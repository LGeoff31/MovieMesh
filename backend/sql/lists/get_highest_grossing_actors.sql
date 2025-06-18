SELECT a.actor_id,
       a.name,
       SUM(m.gross_usd) AS total_gross
FROM actors a
JOIN movie_cast mc ON a.actor_id = mc.actor_id
JOIN movies m ON mc.movie_id = m.movie_id
WHERE m.gross_usd IS NOT NULL
GROUP BY a.actor_id, a.name
ORDER BY total_gross DESC
LIMIT 10;