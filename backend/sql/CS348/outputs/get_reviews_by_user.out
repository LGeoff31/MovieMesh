-- basic feature: display reviews made by a user

SELECT review_id,
       rating,
       comment_txt,
       created_at
FROM reviews
WHERE user_id = :id
ORDER BY created_at DESC; 