-- basic feature: add a review for a movie

INSERT INTO reviews (movie_id, user_id, rating, comment_txt)
VALUES (:m, :u, :r, :c);
SELECT LAST_INSERT_ID() as review_id;