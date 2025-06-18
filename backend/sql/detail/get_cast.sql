SELECT p.name, mc.cast_order
FROM people p
JOIN movie_cast mc USING(person_id)
WHERE mc.movie_id = :id
ORDER BY mc.cast_order; 