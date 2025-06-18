SELECT AVG(rating) AS avg_rating, COUNT(*) AS num_reviews
FROM reviews
WHERE movie_id = :id; 