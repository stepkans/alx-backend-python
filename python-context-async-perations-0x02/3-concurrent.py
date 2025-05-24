#!/usr/bin/env python3
"""
Concurrent asynchronous database queries using aiosqlite and asyncio.
"""

import aiosqlite
import asyncio


DB_FILE = "my_database.db"


async def async_fetch_users():
    """Fetch all users from the database."""
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        await cursor.close()
        print("All users:")
        for user in users:
            print(user)


async def async_fetch_older_users():
    """Fetch users older than 40 from the database."""
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        older_users = await cursor.fetchall()
        await cursor.close()
        print("Users older than 40:")
        for user in older_users:
            print(user)


async def fetch_concurrently():
    """Run both fetch functions concurrently."""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


if __name__ == "__main__":
    # Optional setup: create table and add data if needed
    import sqlite3
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )""")
        cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 30),
            ("Bob", 45),
            ("Charlie", 50),
            ("Diana", 22),
        ])
        conn.commit()

    asyncio.run(fetch_concurrently())
