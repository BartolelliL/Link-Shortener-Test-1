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


def link_out(row, request):
    return {
        "code": row["code"],
        "url": str(row["url"]),
        "clicks": row["clicks"],
        "created_at": row["created_at"],
        "short_url": str(request.base_url).rstrip("/") + "/" + row["code"]
    }

def create_link(url, code):
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
