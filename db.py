import sqlite3
from datetime import datetime

DB_PATH = "prices.db"


def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id   TEXT NOT NULL,
            title     TEXT,
            price     REAL NOT NULL,
            currency  TEXT,
            recorded_at TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()


def save_price(item_id: str, title: str, price: float, currency: str):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT INTO prices (item_id, title, price, currency, recorded_at) VALUES (?,?,?,?,?)",
        (item_id, title, price, currency, datetime.now().isoformat()),
    )
    con.commit()
    con.close()


def get_history(item_id: str) -> list[dict]:
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT price, recorded_at FROM prices WHERE item_id=? ORDER BY recorded_at",
        (item_id,),
    ).fetchall()
    con.close()
    return [{"price": r[0], "recorded_at": r[1]} for r in rows]


def get_min_price(item_id: str) -> float | None:
    con = sqlite3.connect(DB_PATH)
    row = con.execute(
        "SELECT MIN(price) FROM prices WHERE item_id=?", (item_id,)
    ).fetchone()
    con.close()
    return row[0] if row else None


def get_tracked_items() -> list[str]:
    con = sqlite3.connect(DB_PATH)
    rows = con.execute("SELECT DISTINCT item_id FROM prices").fetchall()
    con.close()
    return [r[0] for r in rows]
