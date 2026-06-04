# ==================================
# IMPORT LIBRERIE
# ==================================

from fastapi import FastAPI
from pydantic import BaseModel

from db import (
    init_db,
    add_chat,
    get_chat,
    get_last_chat,
    trim_chat,
    conn,
    cursor
)

import os
import requests


# ==================================
# APP FASTAPI
# ==================================

app = FastAPI()


# ==================================
# INIT DB
# ==================================

init_db()


# ==================================
# SYSTEM PROMPT
# ==================================

SYSTEM_PROMPT = {
    "role": "system",
    "content": """
Sei un assistente AI tecnico.

Rispondi in modo:
- chiaro
- pratico
- educativo

Spiega sempre il motivo delle scelte tecniche.
"""
}


# ==================================
# INPUT MODEL
# ==================================

class ChatRequest(BaseModel):
    message: str


# ==================================
# COMMAND SYSTEM
# ==================================

def handle_command(message: str):

    cmd = message.strip()

    # ----------------------
    # RESET
    # ----------------------
    if cmd == "/reset":

        cursor.execute("DELETE FROM chat")
        conn.commit()

        return {
            "response": "Memoria resettata 🧠"
        }

    # ----------------------
    # MEMORY STATUS
    # ----------------------
    if cmd == "/memory":

        chat = get_chat()

        return {
            "response": f"Messaggi salvati: {len(chat)}"
        }

    # ----------------------
    # HELP
    # ----------------------
    if cmd == "/help":

        return {
            "response": (
                "Comandi disponibili:\n"
                "/reset → cancella memoria\n"
                "/memory → mostra numero messaggi\n"
                "/help → mostra questo aiuto"
            )
        }

    return None


# ==================================
# HOME
# ==================================

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "AI Lab attivo 🚀"
    }


# ==================================
# MEMORY
# ==================================

@app.get("/memory")
def memory():
    return get_chat()


# ==================================
# BUILD PROMPT
# ==================================

def build_messages(history):

    messages = [SYSTEM_PROMPT]

    for role, msg in history:

        if role in ["user", "assistant"]:

            messages.append({
                "role": role,
                "content": msg
            })

    return messages


# ==================================
# AI ENGINE
# ==================================

def generate_ai_response(history):

    api_key = os.getenv("OPENROUTER_API_KEY")

    messages = build_messages(history)

    # =========================
    # LOG PROMPT
    # =========================

    print("\n===== HISTORY =====")
    for role, msg in history:
        print(f"{role}: {msg}")
    print("===================\n")

    print("\n===== PROMPT INVIATO =====")
    for m in messages:
        print(m)
    print("=========================\n")

    try:

        response = requests.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },

            json={
                "model": "openai/gpt-oss-20b",
                "messages": messages
            },

            timeout=20
        )

        if response.status_code != 200:

            return f"Errore OpenRouter: {response.status_code}"

        data = response.json()

        ai_response = data["choices"][0]["message"]["content"]

        print("\n===== RISPOSTA AI =====")
        print(ai_response)
        print("=======================\n")

        return ai_response

    except Exception as e:

        return f"Errore connessione AI: {str(e)}"


# ==================================
# CHAT ENDPOINT
# ==================================

@app.post("/chat")
def chat(req: ChatRequest):

    # ----------------------
    # COMMAND CHECK
    # ----------------------

    command_result = handle_command(req.message)

    if command_result:

        return {
            "input": req.message,
            "response": command_result["response"],
            "mode": "command"
        }

    # ----------------------
    # SAVE USER MESSAGE
    # ----------------------

    add_chat("user", req.message)

    # ----------------------
    # GET HISTORY
    # ----------------------

    history = get_last_chat(10)

    # ----------------------
    # AI RESPONSE
    # ----------------------

    response = generate_ai_response(history)

    # ----------------------
    # SAVE AI MESSAGE
    # ----------------------

    add_chat("assistant", response)

    # ----------------------
    # CLEAN DB
    # ----------------------

    trim_chat(200)

    # ----------------------
    # RETURN RESPONSE
    # ----------------------

    return {
        "input": req.message,
        "response": response,
        "memory_used": len(history),
        "mode": "ai"
    }
