# CS-348

## PostgreSQL Setup

1. Install PostgreSQL if you haven't already:
   - **macOS**: `brew install postgresql`
   - **Ubuntu**: `sudo apt-get install postgresql`
   - **Windows**: Download from [PostgreSQL website](https://www.postgresql.org/download/windows/)

2. Start PostgreSQL service:
   - **macOS**: `brew services start postgresql`
   - **Ubuntu**: `sudo service postgresql start`
   - **Windows**: PostgreSQL service should start automatically

3. Create a database:
   ```bash
   createdb postgres
   ```

4. Configure environment variables:
   Create a `.env` file in the backend directory with:
   ```
   DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"
   ```

5. Install dependencies:
   ```bash
   npm install
   ```

6. Test the connection:
   The application will automatically test the database connection on startup. You should see "Successfully connected to the database" in the console.

## Default Database Configuration
- Host: localhost
- Port: 5432
- Database: postgres
- Username: postgres
- Password: postgres

## Troubleshooting
- If you get a connection error, ensure PostgreSQL is running
- Verify your database credentials in the `.env` file
- Check if the database exists using `psql -l`
- Ensure port 5432 is not blocked by your firewall 
