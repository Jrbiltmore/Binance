import sqlite3
from sqlite3 import Error
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_file):
        """
        Initialize the Database class with the database file path.
        
        :param db_file: Path to the SQLite database file
        """
        self.db_file = db_file
        self.conn = self.create_connection()

    def create_connection(self):
        """
        Create a database connection to the SQLite database specified by db_file.
        
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(self.db_file, check_same_thread=False)
            logger.info(f"Connected to database: {self.db_file}")
            return conn
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
            return None

    def create_table(self, create_table_sql):
        """
        Create a table from the create_table_sql statement.
        
        :param create_table_sql: A CREATE TABLE statement
        """
        try:
            with self.transaction():
                self.conn.execute(create_table_sql)
                logger.info("Table created successfully")
        except Error as e:
            logger.error(f"Error creating table: {e}")

    def insert_data(self, table, data):
        """
        Insert data into a table.
        
        :param table: Table name
        :param data: Dictionary with column names as keys and data as values
        :return: The last row id of the inserted row
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            with self.transaction():
                cur = self.conn.cursor()
                cur.execute(sql, tuple(data.values()))
                logger.info(f"Data inserted into {table}: {data}")
                return cur.lastrowid
        except Error as e:
            logger.error(f"Error inserting data into {table}: {e}")
            return None

    def query_data(self, query, params=None):
        """
        Query data from the database.
        
        :param query: The SELECT query
        :param params: Parameters for the query
        :return: List of rows
        """
        try:
            cur = self.conn.cursor()
            cur.execute(query, params or ())
            rows = cur.fetchall()
            logger.info(f"Query executed: {query} with params: {params}")
            return rows
        except Error as e:
            logger.error(f"Error querying data: {e}")
            return []

    @contextmanager
    def transaction(self):
        """
        Context manager for handling transactions.
        """
        try:
            yield
            self.conn.commit()
        except Error as e:
            self.conn.rollback()
            logger.error(f"Transaction failed and rolled back: {e}")
            raise e

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def __enter__(self):
        """
        Enter the runtime context related to this object.
        """
        if not self.conn:
            self.conn = self.create_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context related to this object.
        """
        self.close_connection()

# Example usage:
if __name__ == "__main__":
    db = Database("trading.db")
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS trades (
        id integer PRIMARY KEY,
        symbol text NOT NULL,
        price real NOT NULL,
        quantity real NOT NULL,
        timestamp text NOT NULL
    );
    """
    db.create_table(create_table_sql)
    db.insert_data("trades", {"symbol": "BTCUSD", "price": 40000, "quantity": 1, "timestamp": "2021-01-01 00:00:00"})
    print(db.query_data("SELECT * FROM trades"))
    db.close_connection()
