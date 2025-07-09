-- basic feature: delete a review

DELETE FROM reviews
WHERE review_id = :id;