import sqlite3

conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        message TEXT
    )
    """)
    conn.commit()

def add_chat(role, message):
    cursor.execute(
        "INSERT INTO chat (role, message) VALUES (?, ?)",
        (role, message)
    )
    conn.commit()

def get_chat():
    cursor.execute("SELECT role, message FROM chat ORDER BY id ASC")
    return cursor.fetchall()
