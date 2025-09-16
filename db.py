import sqlite3, time

DB_FILE = "zoho_tokens.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            name TEXT PRIMARY KEY,
            client_id TEXT,
            client_secret TEXT,
            refresh_token TEXT,
            access_token TEXT,
            expires_at INTEGER,
            department_id TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_client(name, client_id, client_secret, refresh_token, department_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO clients
        (name, client_id, client_secret, refresh_token, department_id, access_token, expires_at)
        VALUES (?, ?, ?, ?, ?, NULL, 0)
    """, (name, client_id, client_secret, refresh_token, department_id))
    conn.commit()
    conn.close()

def get_client(name):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE name=?", (name,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "name": row[0],
            "client_id": row[1],
            "client_secret": row[2],
            "refresh_token": row[3],
            "access_token": row[4],
            "expires_at": row[5],
            "department_id": row[6]
        }
    return None

def update_access_token(name, access_token, expires_in_sec):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    expires_at = int(time.time()) + expires_in_sec - 30  # refresh slightly early
    cur.execute("UPDATE clients SET access_token=?, expires_at=? WHERE name=?",
                (access_token, expires_at, name))
    conn.commit()
    conn.close()
