SELECT * FROM v_movie_card
WHERE title LIKE :pat
ORDER BY year DESC
LIMIT 30;