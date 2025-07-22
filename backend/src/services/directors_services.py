from utils.sql_utils import load_sql
from sqlalchemy import text

def get_top_directors(db):
    sql = text(load_sql("directors/top_directors.sql"))
    return db.execute(sql).mappings().all()