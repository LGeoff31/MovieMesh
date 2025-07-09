SELECT r.review_id,
       r.rating,
       r.comment_txt,
       r.created_at,
       m.title,
       m.movie_id,
       u.username
FROM reviews r
JOIN users u ON r.user_id = u.user_id
JOIN movies m ON r.movie_id = m.movie_id
WHERE r.user_id = :id
ORDER BY created_at DESC; 