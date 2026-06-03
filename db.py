# Libreria standard di Python per usare SQLite
import sqlite3


# ==================================
# CONNESSIONE DATABASE
# ==================================

# Creiamo (o apriamo) il file memory.db
#
# check_same_thread=False
#
# permette a FastAPI di usare la stessa
# connessione anche su thread diversi
#
conn = sqlite3.connect(
    "memory.db",
    check_same_thread=False
)

cursor = conn.cursor()


# ==================================
# CREAZIONE TABELLA
# ==================================

def init_db():

    # Se la tabella chat non esiste,
    # viene creata

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        role TEXT,

        message TEXT

    )
    """)

    conn.commit()


# ==================================
# SALVATAGGIO MESSAGGI
# ==================================

def add_chat(role, message):

    cursor.execute(
        """
        INSERT INTO chat (role, message)
        VALUES (?, ?)
        """,
        (role, message)
    )

    conn.commit()


# ==================================
# RECUPERO ULTIMI MESSAGGI
# ==================================

def get_last_chat(limit=10):

    # Recuperiamo SOLO gli ultimi N messaggi
    #
    # ORDER BY id DESC
    # prende i più recenti
    #
    # LIMIT ?
    # limita il numero di record

    cursor.execute(
        """
        SELECT role, message
        FROM chat
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    # Poiché li abbiamo presi al contrario,
    # li invertiamo per ripristinare
    # l'ordine cronologico

    return rows[::-1]


# ==================================
# RECUPERO TUTTA LA MEMORIA
# ==================================

def get_chat():

    cursor.execute(
        """
        SELECT role, message
        FROM chat
        ORDER BY id ASC
        """
    )

    return cursor.fetchall()


# ==================================
# PULIZIA DATABASE
# ==================================

def trim_chat(max_rows=200):

    # Manteniamo soltanto gli ultimi
    # max_rows messaggi

    cursor.execute(
        """
        DELETE FROM chat
        WHERE id NOT IN (

            SELECT id
            FROM chat
            ORDER BY id DESC
            LIMIT ?

        )
        """,
        (max_rows,)
    )

    conn.commit()
