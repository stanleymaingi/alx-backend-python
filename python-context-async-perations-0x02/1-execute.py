# File: 1-execute.py

import sqlite3

class ExecuteQuery:
    """Reusable context manager to execute a query with parameters."""
    
    def __init__(self, db_file, query, params=None):
        self.db_file = db_file
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        # Open connection and execute the query
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        # Commit changes if no exception, close connection
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        # Do not suppress exceptions
        return False


# Usage example
if __name__ == "__main__":
    db_file = "example.db"  # Replace with your database

    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    # Using the reusable query context manager
    with ExecuteQuery(db_file, query, params) as results:
        for row in results:
            print(row)
