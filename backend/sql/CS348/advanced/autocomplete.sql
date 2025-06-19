-- advanced feature: autocomplete movie titles

SELECT m.movie_id, m.title
FROM movies m
LEFT JOIN movie_rating mr ON m.movie_id = mr.movie_id
WHERE MATCH(m.title) AGAINST (:prefix IN BOOLEAN MODE)
ORDER BY mr.rating DESC
LIMIT 10;