import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_FILE = "spendly.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "name TEXT NOT NULL,"
        "email TEXT UNIQUE NOT NULL,"
        "password_hash TEXT NOT NULL,"
        "created_at TEXT DEFAULT (datetime('now'))"
        ")"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS expenses ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "user_id INTEGER NOT NULL,"
        "amount REAL NOT NULL,"
        "category TEXT NOT NULL,"
        "date TEXT NOT NULL,"
        "description TEXT,"
        "created_at TEXT DEFAULT (datetime('now')),"
        "FOREIGN KEY (user_id) REFERENCES users(id)"
        ")"
    )
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cursor = conn.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count > 0:
        conn.close()
        return

    demo_user = (
        "Demo User",
        "demo@spendly.com",
        generate_password_hash("demo123"),
    )
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        demo_user,
    )
    user_id = conn.execute("SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)).fetchone()[0]

    categories = [
        "Food", "Transport", "Bills", "Health",
        "Entertainment", "Shopping", "Other",
    ]
    # 8 expenses: 7 categories + one extra Food
    expenses = [
        (user_id, 45.50, "Food", "2026-10-01", "Lunch"),
        (user_id, 12.00, "Transport", "2026-10-03", "Bus ticket"),
        (user_id, 120.00, "Bills", "2026-10-05", "Electricity"),
        (user_id, 30.00, "Health", "2026-10-07", "Pharmacy"),
        (user_id, 25.75, "Entertainment", "2026-10-09", "Movie"),
        (user_id, 89.99, "Shopping", "2026-10-11", "New shoes"),
        (user_id, 15.00, "Other", "2026-10-13", "Gift"),
        (user_id, 22.30, "Food", "2026-10-15", "Dinner"),
    ]
    for exp in expenses:
        conn.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            exp,
        )
    conn.commit()
    conn.close()
