
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parents[1] / "app.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query(sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

def query_one(sql: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
        if not rows:
            return None
        return dict(rows[0])
