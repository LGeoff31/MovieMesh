#!/usr/bin/env python3
"""Load users from data/users.csv into users table with password hashing."""
import os, sys, csv
from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from tqdm import tqdm

if len(sys.argv)!=2:
    print("Usage: python scripts/_load_users.py data/users.csv"); sys.exit(1)

csv_path = sys.argv[1]
load_dotenv()
DB_URL=os.getenv("DB_URL")
if not DB_URL:
    print("DB_URL missing"); sys.exit(1)

pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
eng=create_engine(DB_URL,future=True)

with eng.begin() as conn, open(csv_path, newline='',encoding='utf-8') as fh:
    reader=csv.DictReader(fh)
    for row in tqdm(reader, desc="loading users"):
        hash=pwd.hash(row['password'])
        conn.execute(text("""
            INSERT INTO users (user_id,username,name,password_hash)
            VALUES (:id,:u,:n,:p)
            ON DUPLICATE KEY UPDATE username=VALUES(username),name=VALUES(name)
        """),{"id":int(row['user_id']),"u":row['username'],"n":row['name'],"p":hash})
print("Users loaded ✅")