"""
database.py
SQLite persistence layer for the CKA Exam Tracker.

Stores: topic_id, topic_name, status, last_updated timestamp.
All functions take an explicit db_path so the module is easy to test
and so app.py never has to know about SQL directly.
"""

import sqlite3
import datetime
from contextlib import contextmanager

DB_PATH = "cka_tracker.db"


@contextmanager
def _connect(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path: str = DB_PATH):
    """Create the progress table if it doesn't already exist."""
    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
                topic_id INTEGER PRIMARY KEY,
                topic_name TEXT NOT NULL,
                status TEXT NOT NULL,
                last_updated TEXT NOT NULL
            )
            """
        )


def load_progress(db_path: str = DB_PATH) -> dict:
    """Return {topic_id: status} for every row saved so far."""
    with _connect(db_path) as conn:
        rows = conn.execute("SELECT topic_id, status FROM progress").fetchall()
    return {row[0]: row[1] for row in rows}


def save_status(topic_id: int, topic_name: str, status: str, db_path: str = DB_PATH):
    """Insert or update the status of a single topic."""
    now = datetime.datetime.now().isoformat(timespec="seconds")
    with _connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO progress (topic_id, topic_name, status, last_updated)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(topic_id) DO UPDATE SET
                status = excluded.status,
                last_updated = excluded.last_updated
            """,
            (topic_id, topic_name, status, now),
        )


def save_many(entries: list, db_path: str = DB_PATH):
    """Bulk insert/update — used by CSV import."""
    now = datetime.datetime.now().isoformat(timespec="seconds")
    with _connect(db_path) as conn:
        conn.executemany(
            """
            INSERT INTO progress (topic_id, topic_name, status, last_updated)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(topic_id) DO UPDATE SET
                status = excluded.status,
                last_updated = excluded.last_updated
            """,
            [(e["id"], e["name"], e["status"], now) for e in entries],
        )


def reset_progress(topic_ids: list, default_status: str, db_path: str = DB_PATH):
    """Reset every given topic back to the default status."""
    now = datetime.datetime.now().isoformat(timespec="seconds")
    with _connect(db_path) as conn:
        conn.executemany(
            "UPDATE progress SET status = ?, last_updated = ? WHERE topic_id = ?",
            [(default_status, now, tid) for tid in topic_ids],
        )


def get_last_updated(db_path: str = DB_PATH) -> dict:
    """Return {topic_id: last_updated} for export purposes."""
    with _connect(db_path) as conn:
        rows = conn.execute("SELECT topic_id, last_updated FROM progress").fetchall()
    return {row[0]: row[1] for row in rows}
