"""
CWE-89 Lab: Intentionally vulnerable database helpers.

The goal for attendees:
- Identify where SQL Injection is possible.
- Fix it using parameterized queries.
- Add safe error handling so DB errors don't leak.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("lab.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """
    )

    # Seed users (idempotent)
    for u, p in [("admin", "admin123"), ("alice", "alice123"), ("bob", "bob123")]:
        cur.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            (u, p),
        )

    conn.commit()
    conn.close()


def authenticate_user(username: str, password: str) -> bool:
    """
    ❌ INTENTIONALLY VULNERABLE:
    SQL is built using string interpolation (classic SQL injection).
    """
    conn = get_connection()
    cur = conn.cursor()

    query = (
        f"SELECT id FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )

    cur.execute(query)
    row = cur.fetchone()

    conn.close()
    return row is not None
