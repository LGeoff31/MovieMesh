SELECT a.name, mc.cast_order
FROM actors a
JOIN movie_cast mc ON a.actor_id = mc.actor_id
WHERE mc.movie_id = :id
ORDER BY mc.cast_order;
