SELECT rating, COUNT(*) AS num_reviews
FROM reviews
WHERE movie_id = :id
GROUP BY rating
ORDER BY rating;