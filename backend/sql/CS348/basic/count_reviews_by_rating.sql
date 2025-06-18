-- basic feature: show distribution of reviews by rating for a movie

SELECT rating, COUNT(*) AS num_reviews
FROM reviews
WHERE movie_id = :id
GROUP BY rating
ORDER BY rating;