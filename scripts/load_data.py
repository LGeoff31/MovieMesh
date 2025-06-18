#!/usr/bin/env python3
"""
Load imdb_top_1000.csv into the MySQL schema (schema_new.sql format).
Usage:
  python scripts/load_data.py data/imdb_top_1000.csv
Requires:
  pip install pandas sqlalchemy pymysql tqdm python-dotenv
"""
import math, os, re, sys, pandas as pd
from tqdm import tqdm
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()                                       # reads .env
DB_URL = os.getenv("DB_URL")                        # mysql+pymysql://user:pwd@localhost/imdb_clone
csv_path = sys.argv[1]

df = pd.read_csv(csv_path)
eng, actors, directors, genres = create_engine(DB_URL, future=True), {}, {}, {}

def none_if_nan(x):
    return None if (pd.isna(x) or (isinstance(x, float) and math.isnan(x))) else x

def clean_int(x):
    try:
        return int(float(str(x).replace(',', '').strip()))
    except (ValueError, TypeError):
        return None

def minutes(x):
    try:
        return int(float(str(x).split()[0]))
    except (ValueError, AttributeError):
        return None

def money(x):
    try:
        return int(re.sub(r'[^\d]', '', str(x)))
    except ValueError:
        return None

with eng.begin() as conn:
    for _, r in tqdm(df.iterrows(), total=len(df)):
        # Insert movie (without imdb_rating - that goes in movie_rating table)
        mid = conn.execute(text("""
          INSERT INTO movies(title, year, certificate, runtime_min, 
                            overview, gross_usd, poster_link)
          VALUES (:t,:y,:c,:rt,:ov,:g,:p)
          ON DUPLICATE KEY UPDATE movie_id=LAST_INSERT_ID(movie_id)
          """),
          dict(t=r.Series_Title,
              y=clean_int(r.Released_Year),
              c=none_if_nan(r.Certificate),
              rt=minutes(r.Runtime),
              ov=none_if_nan(r.Overview),
              g=money(r.Gross),
              p=none_if_nan(r.Poster_Link))
        ).lastrowid

        # Insert/update movie rating
        conn.execute(text("""
          INSERT INTO movie_rating(movie_id, rating, votes)
          VALUES (:m, :r, :v)
          ON DUPLICATE KEY UPDATE 
            rating = VALUES(rating),
            votes = VALUES(votes)
          """),
          dict(m=mid, 
               r=r.IMDB_Rating, 
               v=clean_int(r.No_of_Votes))
        )

        # director
        director_name = r.Director
        did = directors.get(director_name) or conn.execute(
              text("INSERT IGNORE INTO directors(name) VALUES(:n)"), {'n': director_name}
              ).lastrowid or conn.execute(
              text("SELECT director_id FROM directors WHERE name=:n"), {'n': director_name}
              ).scalar()
        directors[director_name] = did
        conn.execute(text("INSERT IGNORE INTO movie_directors VALUES(:m,:d)"),
                     {'m': mid, 'd': did})

        # cast (actors)
        for order, col in enumerate(["Star1", "Star2", "Star3", "Star4"], 1):
            actor_name = r[col]
            aid = actors.get(actor_name) or conn.execute(
                  text("INSERT IGNORE INTO actors(name) VALUES(:n)"), {'n': actor_name}
                  ).lastrowid or conn.execute(
                  text("SELECT actor_id FROM actors WHERE name=:n"), {'n': actor_name}
                  ).scalar()
            actors[actor_name] = aid
            conn.execute(text(
              "INSERT IGNORE INTO movie_cast VALUES(:m,:a,:o)"),
              {'m': mid, 'a': aid, 'o': order})

        # genres
        for g in map(str.strip, str(r.Genre).split(",")):
            if not g: continue
            gid = genres.get(g) or conn.execute(
                  text("INSERT IGNORE INTO genres(name) VALUES(:n)"), {'n': g}
                  ).lastrowid or conn.execute(
                  text("SELECT genre_id FROM genres WHERE name=:n"), {'n': g}
                  ).scalar()
            genres[g] = gid
            conn.execute(text(
              "INSERT IGNORE INTO movie_genres VALUES(:m,:g)"),
              {'m': mid, 'g': gid})

print("Loaded ✅")