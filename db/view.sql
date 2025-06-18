CREATE VIEW v_movie_card AS
SELECT m.movie_id,
    m.title,
    m.year,
    m.poster_link,
    COALESCE(s.avg_rating, 0) AS avg_rating,
    COALESCE(s.num_reviews, 0) AS num_reviews
FROM movies m
LEFT JOIN movie_rating_summary s USING (movie_id);

CREATE VIEW v_top_directors AS
SELECT d.director_id,
    d.name,
    ROUND(AVG(r.rating),2) AS avg_rating,
    COUNT() AS film_count
FROM directors d
JOIN movie_directors md USING (director_id)
JOIN reviews r USING (movie_id)
GROUP BY d.director_id, d.name
HAVING film_count >= 3
ORDER BY avg_rating DESC
LIMIT 10;