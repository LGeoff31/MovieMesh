#!/usr/bin/env python3
"""
Load imdb_top_1000.csv into the MySQL schema.
Usage:
  python scripts/load_data.py imdb_top_1000.csv
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
eng, people, genres = create_engine(DB_URL, future=True), {}, {}

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
        mid = conn.execute(text("""
          INSERT INTO movies(title, year, certificate, runtime_min, imdb_rating,
                            overview, metascore, votes, gross_usd, poster_link)
          VALUES (:t,:y,:c,:rt,:ir,:ov,:ms,:v,:g,:p)
          ON DUPLICATE KEY UPDATE movie_id=LAST_INSERT_ID(movie_id)
          """),
          dict(t=r.Series_Title,
              y=clean_int(r.Released_Year),
              c=none_if_nan(r.Certificate),
              rt=minutes(r.Runtime),
              ir=r.IMDB_Rating,
              ov=none_if_nan(r.Overview),
              ms=clean_int(r.Meta_score),
              v=clean_int(r.No_of_Votes),
              g=money(r.Gross),
              p=none_if_nan(r.Poster_Link))
        ).lastrowid

        # director
        did = people.get(r.Director) or conn.execute(
              text("INSERT IGNORE INTO people(name) VALUES(:n)"), {'n': r.Director}
              ).lastrowid or conn.execute(
              text("SELECT person_id FROM people WHERE name=:n"), {'n': r.Director}
              ).scalar()
        people[r.Director] = did
        conn.execute(text("INSERT IGNORE INTO movie_directors VALUES(:m,:d)"),
                     {'m': mid, 'd': did})

        # cast
        for order, col in enumerate(["Star1", "Star2", "Star3", "Star4"], 1):
            name = r[col]
            pid = people.get(name) or conn.execute(
                  text("INSERT IGNORE INTO people(name) VALUES(:n)"), {'n': name}
                  ).lastrowid or conn.execute(
                  text("SELECT person_id FROM people WHERE name=:n"), {'n': name}
                  ).scalar()
            people[name] = pid
            conn.execute(text(
              "INSERT IGNORE INTO movie_cast VALUES(:m,:p,:o)"),
              {'m': mid, 'p': pid, 'o': order})

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
