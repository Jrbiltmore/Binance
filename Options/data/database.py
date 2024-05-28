import sqlite3
from sqlite3 import Error

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
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            print(f"Connected to database: {self.db_file}")
        except Error as e:
            print(e)
        return conn

    def create_table(self, create_table_sql):
        """
        Create a table from the create_table_sql statement.
        
        :param create_table_sql: A CREATE TABLE statement
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def insert_data(self, table, data):
        """
        Insert data into a table.
        
        :param table: Table name
        :param data: Dictionary with column names as keys and data as values
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cur = self.conn.cursor()
        cur.execute(sql, tuple(data.values()))
        self.conn.commit()
        return cur.lastrowid

    def query_data(self, query, params=None):
        """
        Query data from the database.
        
        :param query: The SELECT query
        :param params: Parameters for the query
        :return: List of rows
        """
        cur = self.conn.cursor()
        cur.execute(query, params or ())
        return cur.fetchall()

# Example usage:
# db = Database("trading.db")
# create_table_sql = """
# CREATE TABLE IF NOT EXISTS trades (
#     id integer PRIMARY KEY,
#     symbol text NOT NULL,
#     price real NOT NULL,
#     quantity real NOT NULL,
#     timestamp text NOT NULL
# );
# """
# db.create_table(create_table_sql)
# db.insert_data("trades", {"symbol": "BTCUSD", "price": 40000, "quantity": 1, "timestamp": "2021-01-01 00:00:00"})
# print(db.query_data("SELECT * FROM trades"))
