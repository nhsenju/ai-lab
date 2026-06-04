# ==================================
# COMMAND SYSTEM
# ==================================

def handle_command(message: str):

    # Rimuoviamo eventuali spazi
    cmd = message.strip()

    # --------------------------
    # RESET MEMORY
    # --------------------------
    if cmd == "/reset":

        # svuota database
        from db import conn, cursor

        cursor.execute("DELETE FROM chat")
        conn.commit()

        return {
            "response": "Memoria resettata 🧠"
        }

    # --------------------------
    # MEMORY INFO
    # --------------------------
    if cmd == "/memory":

        chat = get_chat()

        return {
            "response": f"Messaggi salvati: {len(chat)}"
        }

    # --------------------------
    # HELP
    # --------------------------
    if cmd == "/help":

        return {
            "response": (
                "Comandi disponibili:\n"
                "/reset → cancella memoria\n"
                "/memory → mostra stato memoria\n"
                "/help → mostra comandi"
            )
        }

    # fallback
    return None
