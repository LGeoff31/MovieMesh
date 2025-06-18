SELECT review_id,
       rating,
       comment_txt,
       created_at
FROM reviews
WHERE movie_id = :id
ORDER BY created_at DESC; 