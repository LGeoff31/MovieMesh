SELECT review_id,
       rating,
       comment_txt,
       created_at,
       u.username
FROM reviews 
LEFT JOIN users u ON reviews.user_id = u.user_id
WHERE movie_id = :id
ORDER BY created_at DESC; 