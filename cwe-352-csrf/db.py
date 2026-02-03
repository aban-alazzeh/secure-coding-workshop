import sqlite3
from pathlib import Path
from typing import Optional, List, Tuple

DB_PATH = Path(__file__).with_name("lab.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                email    TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS balances (
                username TEXT PRIMARY KEY,
                balance  INTEGER NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username)
            );

            CREATE TABLE IF NOT EXISTS payees (
                owner  TEXT NOT NULL,
                payee  TEXT NOT NULL,
                PRIMARY KEY(owner, payee),
                FOREIGN KEY (owner) REFERENCES users(username)
            );

            CREATE TABLE IF NOT EXISTS transfers (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                sender    TEXT NOT NULL,
                recipient TEXT NOT NULL,
                amount    INTEGER NOT NULL
            );
            """
        )

        # Seed demo users if missing
        seed_user(conn, "alice", "password123", "alice@bank.test", 1000)
        seed_user(conn, "bob", "password123", "bob@bank.test", 500)
        seed_user(conn, "attacker", "password123", "attacker@evil.test", 0)


def seed_user(conn: sqlite3.Connection, username: str, password: str, email: str, balance: int) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO users (username, password, email) VALUES (?, ?, ?)",
        (username, password, email),
    )
    conn.execute(
        "INSERT OR IGNORE INTO balances (username, balance) VALUES (?, ?)",
        (username, balance),
    )


def authenticate(username: str, password: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
        return row is not None


def get_email(username: str) -> str:
    with get_conn() as conn:
        row = conn.execute("SELECT email FROM users WHERE username = ?", (username,)).fetchone()
        return row["email"] if row else ""


def set_email(username: str, email: str) -> None:
    with get_conn() as conn:
        conn.execute("UPDATE users SET email = ? WHERE username = ?", (email, username))


def get_balance(username: str) -> int:
    with get_conn() as conn:
        row = conn.execute("SELECT balance FROM balances WHERE username = ?", (username,)).fetchone()
        return int(row["balance"]) if row else 0


def add_payee(owner: str, payee: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO payees (owner, payee) VALUES (?, ?)",
            (owner, payee),
        )


def list_payees(owner: str) -> List[str]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT payee FROM payees WHERE owner = ? ORDER BY payee ASC",
            (owner,),
        ).fetchall()
        return [r["payee"] for r in rows]


def transfer(sender: str, recipient: str, amount: int) -> Tuple[bool, str]:
    if amount <= 0:
        return False, "Amount must be positive."

    with get_conn() as conn:
        sender_bal = conn.execute(
            "SELECT balance FROM balances WHERE username = ?",
            (sender,),
        ).fetchone()
        if not sender_bal:
            return False, "Sender not found."

        if int(sender_bal["balance"]) < amount:
            return False, "Insufficient funds."

        # Ensure recipient exists (simplify)
        recip_exists = conn.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (recipient,),
        ).fetchone()
        if not recip_exists:
            return False, "Recipient does not exist."

        conn.execute("UPDATE balances SET balance = balance - ? WHERE username = ?", (amount, sender))
        conn.execute("UPDATE balances SET balance = balance + ? WHERE username = ?", (amount, recipient))
        conn.execute(
            "INSERT INTO transfers (sender, recipient, amount) VALUES (?, ?, ?)",
            (sender, recipient, amount),
        )
        return True, "Transfer complete."


def recent_transfers(username: str, limit: int = 10) -> List[sqlite3.Row]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT sender, recipient, amount
            FROM transfers
            WHERE sender = ? OR recipient = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (username, username, limit),
        ).fetchall()
        return list(rows)
