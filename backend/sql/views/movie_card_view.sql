CREATE VIEW v_movie_card AS
SELECT m.movie_id,
    m.title,
    m.year,
    m.poster_link,
    COALESCE(s.rating, 0) AS avg_rating,
    COALESCE(s.votes, 0) AS num_reviews
FROM movies m
LEFT JOIN movie_rating s USING (movie_id);
