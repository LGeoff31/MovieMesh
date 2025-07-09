#!/usr/bin/env python3
"""
Load data/reviews.csv into the `reviews` table.
Usage:
  python scripts/_load_reviews.py data/reviews.csv
CSV expected columns:
  user_id,movie_id,rating,comment_txt
The script reads .env for DB_URL (mysql+pymysql://user:pwd@localhost/imdb_clone)
"""
import sys, os, csv
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from tqdm import tqdm

if len(sys.argv) != 2:
    print("Usage: python scripts/_load_reviews.py data/reviews.csv")
    sys.exit(1)

csv_path = sys.argv[1]

load_dotenv()
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    print("DB_URL missing in .env")
    sys.exit(1)

eng = create_engine(DB_URL, future=True)

with eng.begin() as conn, open(csv_path, newline='', encoding='utf-8') as fh:
    reader = csv.DictReader(fh)
    for row in tqdm(reader, total=sum(1 for _ in open(csv_path))-1, desc="loading reviews"):
        conn.execute(
            text("""
            INSERT INTO reviews (movie_id, user_id, rating, comment_txt)
            VALUES (:m,:u,:r,:c)
            ON DUPLICATE KEY UPDATE rating=VALUES(rating), comment_txt=VALUES(comment_txt)
            """),
            {"m": int(row["movie_id"]),
             "u": int(row["user_id"]),
             "r": int(row["rating"]),
             "c": row["comment_txt"][:1000]})
print("Reviews loaded ✅")
