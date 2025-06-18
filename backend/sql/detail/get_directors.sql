SELECT p.name
FROM people p
JOIN movie_directors md USING(person_id)
WHERE md.movie_id = :id; 