from utils.sql_utils import load_sql
from sqlalchemy import text

def get_highest_grossing_actors(db):
    sql = text(load_sql("lists/get_highest_grossing_actors.sql"))
    return db.execute(sql).mappings().all()