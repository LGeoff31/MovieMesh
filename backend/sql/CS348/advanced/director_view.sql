-- advanced feature: show top directors

CREATE VIEW v_top_directors AS
SELECT d.director_id,
    d.name,
    ROUND(AVG(r.rating),2) AS avg_rating,
    COUNT(DISTINCT r.movie_id) AS film_count
FROM directors d
JOIN movie_directors md USING (director_id)
JOIN reviews r USING (movie_id)
GROUP BY d.director_id, d.name
HAVING film_count >= 3
ORDER BY avg_rating DESC
LIMIT 10;

