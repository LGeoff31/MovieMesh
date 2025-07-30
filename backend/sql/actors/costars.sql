


WITH RECURSIVE co_stars(actor_id, name, depth, path) AS (
    SELECT a.actor_id, a.name, 0 AS depth, CAST(a.actor_id AS CHAR(200)) AS path
    FROM actors a
    WHERE a.actor_id = :id
  UNION ALL
    SELECT a2.actor_id,
           a2.name,
           cs.depth + 1,
           CONCAT(cs.path, '>', a2.actor_id)
    FROM co_stars cs
    JOIN movie_cast mc1 ON mc1.actor_id = cs.actor_id
    JOIN movie_cast mc2 ON mc2.movie_id = mc1.movie_id
    JOIN actors a2 ON a2.actor_id = mc2.actor_id
    WHERE FIND_IN_SET(a2.actor_id, cs.path) = 0
      AND cs.depth < 3
)
SELECT DISTINCT actor_id, name
FROM co_stars
WHERE depth = 1;


