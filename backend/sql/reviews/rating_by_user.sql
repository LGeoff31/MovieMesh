SELECT AVG(rating) AS avg_rating
FROM reviews
WHERE movie_id = :movie_id AND user_id = :user_id
GROUP BY movie_id;