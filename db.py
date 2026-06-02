import sqlite3

conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT,
        value TEXT
    )
    """)
    conn.commit()

def set_memory(key, value):
    cursor.execute("INSERT INTO memory (key, value) VALUES (?, ?)", (key, value))
    conn.commit()

def get_memory():
    cursor.execute("SELECT key, value FROM memory")
    return cursor.fetchall()
