#!/usr/bin/env python3
"""
Reusable class-based context manager for executing
a SQL query with parameters using sqlite3.
"""

import sqlite3


class ExecuteQuery:
    """
    Custom context manager to execute a given query
    with parameters and return the result.
    """

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is not None:
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()


if __name__ == "__main__":
    db_file = "my_database.db"

    # Optional setup: ensure users table and data exist
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )""")
        cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 30),
            ("Bob", 22),
            ("Charlie", 28),
        ])
        conn.commit()

    # Use the ExecuteQuery context manager
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(db_file, query, params) as results:
        for row in results:
            print(row)
