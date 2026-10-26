import sqlite3
from contextlib import closing

DB_PATH = "links.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Al posto di una tupla, viene
    # restituito un oggetto simile
    # a un dizionario, che consente di accedere
    # ai valori delle colonne per nome.
    #
    # Esempio:
    # row = cursor.fetchone()
    # print(row["url"])
    return conn

def init_db():
    with closing(get_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                clicks INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')


def db_link_out(row, request):
    # Returns the dictonary with all 5 fields
    # specified in the schema, including the short_url.

    return {
        "code": row["code"],
        "url": str(row["url"]),
        "clicks": row["clicks"],
        "created_at": row["created_at"],
        "short_url": str(request.base_url).rstrip("/") + "/" + row["code"]
    }

def db_create_link(url, code):
    with closing(get_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO links (url, code)
            VALUES (?, ?)
            """,
            (url, code)
        )
        row = cursor.execute(
            """
            SELECT * FROM links WHERE code = ?
            """,
            (code,)
        ).fetchone()
        return row

def db_fifty_latest_links():
    with closing(get_db()) as conn, conn:
        cursor = conn.cursor()
        rows = cursor.execute(
            """
            SELECT * FROM links
            ORDER BY created_at DESC
            LIMIT 50
            """
        ).fetchall()
        return rows

def db_delete_link(code: str):
    with closing(get_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM links WHERE code = ?
            """,
            (code,)
        )
        return cursor.rowcount > 0  # Returns True if a row was deleted, False otherwise

def db_add_click(code: str):
    with closing(get_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE links
            SET clicks = clicks + 1
            WHERE code = ?
            """,
            (code,)
        )
        return cursor.rowcount > 0  # Returns True if a row was updated, False otherwise

def db_get_link_by_code(code: str):
    with closing(get_db()) as conn, conn:
        cursor = conn.cursor()
        row = cursor.execute(
            """
            SELECT * FROM links WHERE code = ?
            """,
            (code,)
        ).fetchone()
        return row