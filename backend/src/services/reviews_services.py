from utils.sql_utils import load_sql
from sqlalchemy import text


def check_movie_exists(movie_id, db):
    sql = text(load_sql("reviews/check_movie_exists.sql"))
    return db.execute(sql, {"id": movie_id}).first()

def add_review(movie_id, rating, comment, user_id, db):
    sql = text(load_sql("reviews/add_review.sql"))
    res = db.execute(sql, {"m": movie_id, "u": user_id, "r": rating, "c": comment})
    db.commit()
    return res.lastrowid

def get_reviews_by_movie(movie_id, db):
    sql = text(load_sql("reviews/get_reviews_by_movie.sql"))
    rows = db.execute(sql, {"id": movie_id}).mappings().all()
    return rows

def get_reviews_by_user(user_id, db):
    sql = text(load_sql("reviews/get_reviews_by_user.sql"))
    rows = db.execute(sql, {"id": user_id}).mappings().all()
    return rows

def delete_review(review_id, db):
    sql = text(load_sql("reviews/delete_review.sql"))
    db.execute(sql, {"id": review_id})
    db.commit()
    return review_id

def get_recent_reviews(db):
    sql = text(load_sql("reviews/get_recent_reviews.sql"))
    rows = db.execute(sql).mappings().all()
    return rows