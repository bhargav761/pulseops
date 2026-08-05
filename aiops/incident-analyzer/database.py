import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "pulseops.db"


def get_connection():
    """Return SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Create required database tables."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp TEXT NOT NULL,

        service TEXT NOT NULL,

        severity TEXT NOT NULL,

        title TEXT,

        description TEXT,

        root_cause TEXT,

        recommendation TEXT,

        status TEXT DEFAULT 'OPEN'

    )
    """)

    conn.commit()
    conn.close()


def execute_query(query, params=()):
    """Execute INSERT, UPDATE, DELETE."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    last_id = cursor.lastrowid

    conn.close()

    return last_id


def fetch_one(query, params=()):
    """Return a single database record."""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    row = cursor.fetchone()

    conn.close()

    return row


def fetch_all(query, params=()):
    """Return multiple database records."""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return rows