import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "prices.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    con = get_connection()
    con.execute("""
        CREATE TABLE IF NOT EXISTS products (
            item_id   TEXT PRIMARY KEY,
            title     TEXT,
            url       TEXT,
            threshold REAL DEFAULT 5.0
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id   TEXT,
            price     REAL,
            currency  TEXT,
            timestamp TEXT DEFAULT (datetime('now'))
        )
    """)
    con.commit()
    con.close()
    print("✅ Database initialized.")


def add_product(item_id: str, title: str, url: str = "", threshold: float = 5.0):
    con = get_connection()
    con.execute(
        "INSERT OR IGNORE INTO products (item_id, title, url, threshold) VALUES (?,?,?,?)",
        (item_id, title, url, threshold)
    )
    con.commit()
    con.close()


def save_price(item_id: str, price: float, currency: str = "ARS"):
    con = get_connection()
    con.execute(
        "INSERT INTO prices (item_id, price, currency) VALUES (?,?,?)",
        (item_id, price, currency)
    )
    con.commit()
    con.close()


def get_products():
    con = get_connection()
    rows = con.execute("SELECT item_id, title, url, threshold FROM products").fetchall()
    con.close()
    return [{"item_id": r[0], "title": r[1], "url": r[2], "threshold": r[3]} for r in rows]


def get_price_history(item_id: str):
    con = get_connection()
    rows = con.execute(
        "SELECT price, currency, timestamp FROM prices WHERE item_id=? ORDER BY timestamp ASC",
        (item_id,)
    ).fetchall()
    con.close()
    return [{"price": r[0], "currency": r[1], "timestamp": r[2]} for r in rows]


def get_min_price(item_id: str):
    con = get_connection()
    row = con.execute(
        "SELECT MIN(price) FROM prices WHERE item_id=?", (item_id,)
    ).fetchone()
    con.close()
    return row[0] if row else None
