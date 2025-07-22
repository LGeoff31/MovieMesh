SELECT r.review_id,
       r.rating,
       r.comment_txt,
       r.created_at,
       u.username,
       m.movie_id,
       m.title
FROM reviews r
JOIN users u ON r.user_id = u.user_id
JOIN movies m ON r.movie_id = m.movie_id
ORDER BY r.created_at DESC
LIMIT 5;