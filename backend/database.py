from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

load_dotenv()                                    # reads ../.env
DB_URL = os.getenv("DB_URL")                     # mysql+pymysql://...

# echo=False  → silence SQL logs; change to True while debugging
engine = create_engine(DB_URL, pool_pre_ping=True, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Small helper to run SELECT returning list-of-dicts
def fetch_all(db, sql, **params):
    return db.execute(sql, params).mappings().all()
