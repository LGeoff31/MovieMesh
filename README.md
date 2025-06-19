# CS-348 Course Project: MovieMesh

This repository contains a complete full-stack project with:

• MySQL 8 database  
• Python / FastAPI back-end  
• React + Vite front-end  

## 0. Prerequisites

- Python ≥ 3.10
- Node ≥ 18 + npm
- Git
- MySQL 8 Community Server

## 1. Getting Started

Clone the repo:

```shell
git clone https://github.com/LGeoff31/CS-348.git
cd CS-348
```

Folder structure:

.  
├─ backend/ ← FastAPI code  
├─ db/ ← schema.sql  
├─ data/ ← imdb_top_1000.csv
├─ scripts/ ← CSV loader(s) 
├─ frontend/ ← React app 
├─ requirements.txt ← Python dependencies 
└─ README.md

## 2. MySQL Setup (Native Install)

Install MySQL Community Server: 
Mac: `brew install mysql`
Windows: Windows MSI or use `choco install mysql` / `winget install Oracle.MySQL`

### Create database & user:

Open Terminal:

Start mysql
```shell
mysql -u root -p
```

Inside the MySQL prompt:

```sql
CREATE DATABASE imdb_clone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'imdb_app'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON imdb_clone.\* TO 'imdb_app'@'localhost';
FLUSH PRIVILEGES;
exit
```

### Load the schema:

Terminal:

```shell
Get-Content db\schema.sql | mysql -u imdb_app -p imdb_clone
```

## 3. Python Environment Setup

Terminal:

```shell
python -m venv venv
.\venv\Scripts\Activate # mac/linux: source venv/bin/activate
```

Install dependencies from requirements.txt

```shell
pip install -r requirements.txt
```

## 4. Import the CSV

Download Kaggle dataset `imdb_top_1000.csv` into `data/`.

Run the loader (venv must be active):

```shell
python scripts\load_data.py data\imdb_top_1000.csv
```

Wait until “Loaded ✅”

## 5. Run the Back-End (FastAPI)

Newer:
```shell
fastapi dev main.py
```

Older:
```shell
uvicorn backend.main:app --reload
```

- API root: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/api/docs

## 6. Front-End (React + Vite)

```shell
cd frontend
npm install
npm install bootstrap react-bootstrap react-router-dom
npm run dev
```

Vite will print something like:  
Local: http://localhost:5173

The dev server proxies `/api/*` to FastAPI, so both parts work together.

## 7. Try It Out

- Open http://localhost:5173
- Search for "batman", press Enter
- Click a movie → detail page
- Add a rating/comment (1–10)
- Refresh to see your review

## 8. Production Build (Optional)

```shell
cd frontend
npm run build # static files go in dist/
```

You can then mount the `dist/` folder using `StaticFiles` in FastAPI  
or serve it with any static web server.
