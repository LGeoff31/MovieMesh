-- advanced feature: trigger to update movie rating

DELIMITER $$
CREATE TRIGGER IF NOT EXISTS trg_reviews_insert
AFTER INSERT ON reviews
FOR EACH ROW
BEGIN
  INSERT INTO movie_rating (movie_id, rating, votes)
  VALUES (NEW.movie_id, NEW.rating, 1)
  ON DUPLICATE KEY UPDATE
    rating = ((rating * votes) + NEW.rating) / (votes + 1),
    votes = votes + 1;
END$$
DELIMITER ;

