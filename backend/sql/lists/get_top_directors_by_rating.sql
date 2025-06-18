SELECT d.director_id,
       d.name,
       AVG(mr.rating) AS avg_rating,
       COUNT(m.movie_id) AS movie_count
FROM directors d
JOIN movie_directors md ON d.director_id = md.director_id
JOIN movies m ON md.movie_id = m.movie_id
JOIN movie_rating mr ON m.movie_id = mr.movie_id
GROUP BY d.director_id, d.name
HAVING movie_count >= 2
ORDER BY avg_rating DESC
LIMIT 10;

--

SELECT m.movie_id,
       m.title,
       m.year,
       mr.rating,
       mr.votes
FROM movies m
JOIN movie_rating mr ON m.movie_id = mr.movie_id
ORDER BY mr.votes DESC
LIMIT 20;