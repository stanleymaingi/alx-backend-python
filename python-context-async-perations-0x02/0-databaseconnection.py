# File: 0-databaseconnection.py

import sqlite3

class DatabaseConnection:
    """Custom context manager for SQLite database connections."""
    
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open the database connection and return the cursor
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        return self.cursor

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
    db_file = "example.db"  # Replace with your actual database file

    # Using the custom context manager
    with DatabaseConnection(db_file) as cursor:
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
