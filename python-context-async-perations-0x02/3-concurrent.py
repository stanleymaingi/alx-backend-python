# File: 3-concurrent.py

import asyncio
import aiosqlite

DB_FILE = "example.db"  # Replace with your actual database


async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All users:")
            for row in rows:
                print(row)
            return rows


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)
            return rows


async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather."""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
