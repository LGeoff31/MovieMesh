SELECT movie_id, title
FROM   movies
WHERE  MATCH(title) AGAINST (:prefix IN BOOLEAN MODE)
ORDER  BY imdb_rating DESC
LIMIT 10;