import os
import sqlite3

from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(os.getenv("DATABASE_PATH", "data/pocketsmart.db"))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            planner TEXT NOT NULL,
            request_json TEXT NOT NULL,
            response_json TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """)

        c.commit()


def create_user(
    username: str,
    email: str,
    password_hash: str
):
    try:
        with get_conn() as c:
            cur = c.execute(
                """
                INSERT INTO users(
                    username,
                    email,
                    password_hash
                )
                VALUES(?,?,?)
                """,
                (
                    username.strip(),
                    email.strip().lower(),
                    password_hash
                )
            )

            c.commit()
            return cur.lastrowid

    except sqlite3.IntegrityError:
        return None


def get_user_by_username(
    username: str
) -> Optional[Dict[str, Any]]:

    with get_conn() as c:
        row = c.execute(
            """
            SELECT *
            FROM users
            WHERE username=?
            """,
            (username,)
        ).fetchone()

        return dict(row) if row else None


def get_user_by_id(
    user_id: int
) -> Optional[Dict[str, Any]]:

    with get_conn() as c:
        row = c.execute(
            """
            SELECT *
            FROM users
            WHERE id=?
            """,
            (user_id,)
        ).fetchone()

        return dict(row) if row else None


def save_history(
    user_id: int,
    planner: str,
    request_json: str,
    response_json: str
):

    with get_conn() as c:
        c.execute(
            """
            INSERT INTO history(
                user_id,
                planner,
                request_json,
                response_json
            )
            VALUES(?,?,?,?)
            """,
            (
                user_id,
                planner,
                request_json,
                response_json
            )
        )

        c.commit()


def get_history(
    user_id: int,
    limit: int = 50
) -> List[Dict[str, Any]]:

    with get_conn() as c:
        rows = c.execute(
            """
            SELECT *
            FROM history
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                user_id,
                limit
            )
        ).fetchall()

        return [dict(row) for row in rows]


def get_history_item(
    user_id: int,
    history_id: int
) -> Optional[Dict[str, Any]]:

    with get_conn() as c:
        row = c.execute(
            """
            SELECT *
            FROM history
            WHERE id=? AND user_id=?
            """,
            (
                history_id,
                user_id
            )
        ).fetchone()

        return dict(row) if row else None