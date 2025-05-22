import { Pool, QueryResult } from 'pg';
import pool from './config';

export class Database {
  private pool: Pool;

  constructor() {
    this.pool = pool;
  }

  async query<T>(text: string, params?: any[]): Promise<QueryResult<T>> {
    const start = Date.now();
    try {
      const res = await this.pool.query(text, params);
      const duration = Date.now() - start;
      console.log('Executed query', { text, duration, rows: res.rowCount });
      return res;
    } catch (error) {
      console.error('Error executing query', { text, error });
      throw error;
    }
  }

  async getClient() {
    const client = await this.pool.connect();
    const query = client.query;
    const release = client.release;

    // Set a timeout of 5 seconds, after which we will log this client's last query
    const timeout = setTimeout(() => {
      console.error('A client has been checked out for more than 5 seconds!');
      console.error(`The last executed query on this client was: ${client.lastQuery}`);
    }, 5000);

    // Monkey patch the query method to keep track of the last query executed
    client.query = (...args: any[]) => {
      client.lastQuery = args;
      return query.apply(client, args);
    };

    client.release = () => {
      clearTimeout(timeout);
      client.query = query;
      client.release = release;
      return release.apply(client);
    };

    return client;
  }
}

export default new Database(); 