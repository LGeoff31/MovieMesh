-- basic feature: add a review for a movie

INSERT INTO reviews (movie_id, rating, comment_txt)
VALUES (:m, :r, :c);