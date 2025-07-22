DELIMITER $$
CREATE TRIGGER IF NOT EXISTS trg_reviews_insert
AFTER INSERT ON reviews
FOR EACH ROW
BEGIN
  INSERT INTO movie_rating (movie_id, rating, votes)
  VALUES (NEW.movie_id, NEW.rating, 1)
  ON DUPLICATE KEY UPDATE
    rating = ((rating * votes) + NEW.rating) / (votes + 1),
    votes  = votes + 1;
END$$

CREATE TRIGGER IF NOT EXISTS trg_reviews_delete
AFTER DELETE ON reviews
FOR EACH ROW
BEGIN
  DECLARE avgRating DECIMAL(3,1);
  DECLARE totalVotes INT;

  SELECT ROUND(AVG(rating), 1), COUNT(*) INTO avgRating, totalVotes
  FROM reviews WHERE movie_id = OLD.movie_id;

  IF totalVotes = 0 THEN
    DELETE FROM movie_rating WHERE movie_id = OLD.movie_id;
  ELSE
    UPDATE movie_rating SET rating = avgRating, votes = totalVotes
    WHERE movie_id = OLD.movie_id;
  END IF;
END$$
DELIMITER ;