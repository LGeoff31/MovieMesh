from utils.sql_utils import load_sql
from sqlalchemy import text


def check_movie_exists(movie_id, db):
    sql = text(load_sql("reviews/check_movie_exists.sql"))
    return db.execute(sql, {"id": movie_id}).first()

def add_review(movie_id, user_id, rating, comment, db):
    sql = text(load_sql("reviews/add_review.sql"))
    db.execute(sql, {"m": movie_id, "u": user_id, "r": rating, "c": comment})
    db.commit()

def get_reviews_by_movie(movie_id, db):
    sql = text(load_sql("reviews/get_reviews_by_movie.sql"))
    return db.execute(sql, {"id": movie_id}).fetchall()