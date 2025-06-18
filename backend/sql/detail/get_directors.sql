SELECT d.name
FROM directors d
JOIN movie_directors md ON d.director_id = md.director_id
WHERE md.movie_id = :id;