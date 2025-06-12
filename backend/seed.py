import psycopg2
import getpass

# Use macOS username for default Postgres setup
mac_user = getpass.getuser()

try:
    # Connect to the default "postgres" DB
    conn = psycopg2.connect(
        dbname="postgres",
        user=mac_user,
        host="localhost",
        port="5432"
    )
    print("✅ Connected to database.")

    # Create a cursor to execute SQL commands
    cur = conn.cursor()

    # Create a sample table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            year INT,
            rating FLOAT
        );
    """)

    # Insert sample data (if not already inserted)
    cur.execute("""
        INSERT INTO movies (title, year, rating)
        VALUES 
            ('The Matrix', 1999, 8.7),
            ('Inception', 2010, 8.8),
            ('Interstellar', 2014, 8.6)
        ON CONFLICT DO NOTHING;  -- avoid duplicates if rerunning
    """)

    # Commit the transaction
    conn.commit()

    # Query and print the results
    cur.execute("SELECT * FROM movies WHERE rating > 8.6;")
    rows = cur.fetchall()

    print("\n🎬 Movies:")
    for row in rows:
        print(f"ID: {row[0]}, Title: {row[1]}, Year: {row[2]}, Rating: {row[3]}")

    # Clean up
    cur.close()
    conn.close()
    print("\n✅ Done.")

except Exception as e:
    print("❌ Connection or query failed:")
    print(e)
