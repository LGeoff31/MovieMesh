SELECT actor_id, name
FROM actors
WHERE name LIKE :q
LIMIT 10;