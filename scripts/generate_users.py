#!/usr/bin/env python3
"""Generate data/users.csv with sample users starting id=17."""
import csv, pathlib, random, string

data_dir = pathlib.Path(__file__).resolve().parent.parent / "data"
dest = data_dir / "users.csv"

first_names = ["Alex","Jamie","Taylor","Jordan","Casey","Riley","Morgan","Drew","Avery","Skyler"]
last_names = ["Smith","Johnson","Brown","Davis","Miller","Wilson","Moore","Taylor","Anderson","Thomas"]

with dest.open('w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["user_id","username","name","password"])
    uid_start = 17
    for i in range(10):
        uid = uid_start + i
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        name = f"{fn} {ln}"
        username = f"{fn.lower()}{uid}"
        # simple password
        password = ''.join(random.choices(string.ascii_letters+string.digits,k=8))
        writer.writerow([uid, username, name, password])

print(f"Generated {dest} with 10 sample users starting at id 17 ✅") 