#!/usr/bin/env python3
"""Generate data/reviews.csv with one sample review per movie.

Assumes data/imdb_top_1000.csv exists. The generated CSV has columns:
    user_id,movie_id,rating,comment_txt

Logic:
- movie_id is 1..N in the same order as imdb_top_1000.csv (matches IDs after load_data).
- user_id cycles 1..16.
- rating alternates 6-10 to look realistic.
- comment is a short template string.
"""
import csv, random, pathlib

data_dir = pathlib.Path(__file__).resolve().parent.parent / "data"
source = data_dir / "imdb_top_1000.csv"
dest = data_dir / "reviews.csv"

comments_pool = [
    "Loved it!", "Great movie!", "Really enjoyed this.", "A classic.",
    "Not bad at all.", "Amazing cinematography!", "Fantastic performances.",
]

with source.open(newline='', encoding='utf-8') as f_in, dest.open('w', newline='', encoding='utf-8') as f_out:
    reader = csv.reader(f_in)
    header = next(reader)  # skip header
    writer = csv.writer(f_out)
    writer.writerow(["user_id", "movie_id", "rating", "comment_txt"])

    for idx, _ in enumerate(reader, start=1):
        user_id = ((idx - 1) % 16) + 1
        rating = random.randint(6, 10)
        comment = random.choice(comments_pool)
        writer.writerow([user_id, idx, rating, comment])

print(f"Generated {dest} with {idx} reviews ✅") 