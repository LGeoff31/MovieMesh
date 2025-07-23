from utils.sql_utils import load_sql
from sqlalchemy import text

def fetch_actors_by_name(db, q):
    sql = text(load_sql("actors/search.sql"))
    return db.execute(sql, {"q": f"%{q}%"}).mappings().all()

def get_highest_grossing_actors(db):
    sql = text(load_sql("lists/get_highest_grossing_actors.sql"))
    rows = db.execute(sql).mappings().all()
    return rows

def get_actor_by_id(db, id):
    sql = text(load_sql("actors/get_actor.sql"))
    return db.execute(sql, {"id": id}).mappings().first()

def get_movies_by_actor(db, id):
    sql = text(load_sql("actors/get_movies_by_actor.sql"))
    return db.execute(sql, {"id": id}).mappings().all()

def get_costars_by_actor(db, id):
    sql = text(load_sql("actors/costars.sql"))
    return db.execute(sql, {"id": id}).mappings().all()