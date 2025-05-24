#!/usr/bin/env python3
"""
A custom class-based context manager for handling
database connections using sqlite3.
"""

import sqlite3


class DatabaseConnection:
    """Custom context manager for handling database connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection and return the cursor."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection."""
        if self.connection:
            if exc_type is not None:
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()


if __name__ == "__main__":
    db_file = "my_database.db"

    # Make sure the 'users' table exists (for demo/testing)
    with DatabaseConnection(db_file) as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )""")
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))

    # Use the context manager to perform a query
    with DatabaseConnection(db_file) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
