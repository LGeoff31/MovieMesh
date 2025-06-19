-- advanced feature: find costars of an actor

WITH RECURSIVE co_stars(actor_id, depth, path) AS (
    SELECT
           :start_id, 0, CAST(:start_id AS CHAR(200))
    UNION ALL
    SELECT mc2.actor_id,
           depth + 1,
           CONCAT(path, '>', mc2.actor_id)
    FROM co_stars cs
    JOIN movie_cast mc1 ON mc1.actor_id = cs.actor_id
    JOIN movie_cast mc2 USING (movie_id)
    WHERE FIND_IN_SET(mc2.actor_id, path) = 0
      AND depth < 3
)
SELECT DISTINCT actor_id
FROM co_stars
WHERE depth > 0;