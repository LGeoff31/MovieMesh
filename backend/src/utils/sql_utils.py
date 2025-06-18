from pathlib import Path
from functools import lru_cache

# Directory containing .sql files at project_root/backend/sql/
# (this file lives in backend/src/utils/)
# We go three levels up: utils/ → src/ → backend/ then append 'sql'
SQL_DIR = Path(__file__).resolve().parent.parent.parent / "sql"

@lru_cache(maxsize=None)
def load_sql(filename: str) -> str:
    """Return the contents of a .sql file located in backend/sql/.

    Use with sqlalchemy.text(load_sql("my_query.sql"))
    to keep raw SQL in separate, syntax-highlighted files.
    """
    path = SQL_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {path}")
    return path.read_text(encoding="utf-8") 