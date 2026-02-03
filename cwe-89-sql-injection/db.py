"""
CWE-89 — SQL Injection Lab (INTENTIONALLY VULNERABLE)

This file contains the insecure DB code that attendees will fix later.

We intentionally include multiple unsafe query patterns:
- login auth bypass (string interpolation)
- debug query (error leakage)
- user search (UNION-based injection)

Important: These are separated by endpoint in app.py (one vulnerability type per endpoint).
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


def authenticate_user(username: str, password: str):
    """
    ❌ SQLi (boolean-based/auth bypass):
    vulnerable query built with string interpolation.

    ✅ returns username FROM DB if auth succeeds (more realistic UI).
    """
    conn = get_connection()
    cur = conn.cursor()

    query = (
        f"SELECT username FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )

    cur.execute(query)
    row = cur.fetchone()
    conn.close()

    return row["username"] if row else None


def debug_lookup(q: str):
    """
    ❌ SQLi (error-based):
    unbalanced quotes can trigger an SQL error.

    This function intentionally does NOT handle exceptions.
    app.py will intentionally reflect the error back to the user for the demo.
    """
    conn = get_connection()
    cur = conn.cursor()

    query = f"SELECT username FROM users WHERE username = '{q}'"
    cur.execute(query)
    rows = cur.fetchall()

    conn.close()
    return rows


def search_users(search: str):
    """
    ❌ SQLi (UNION-based):
    vulnerable LIKE query, string interpolation.

    Example payload (for demo):
      ' UNION SELECT password FROM users --
    """
    conn = get_connection()
    cur = conn.cursor()

    query = f"SELECT username FROM users WHERE username LIKE '%{search}%'"
    cur.execute(query)
    rows = cur.fetchall()

    conn.close()
    return rows
