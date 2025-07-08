SELECT user_id, username, name, password_hash 
FROM users 
WHERE username = :username;