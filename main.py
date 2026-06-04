# ==================================
# IMPORT LIBRERIE
# ==================================

# Framework API
from fastapi import FastAPI

# Validazione input JSON
from pydantic import BaseModel

# Funzioni database
from db import (
    init_db,
    add_chat,
    get_chat,
    get_last_chat,
    trim_chat
)

# Variabili ambiente
import os

# Richieste HTTP
import requests


# ==================================
# CREAZIONE APP FASTAPI
# ==================================

app = FastAPI()


# ==================================
# INIZIALIZZAZIONE DATABASE
# ==================================

init_db()


# ==================================
# SYSTEM PROMPT
# ==================================

# Questo messaggio viene inviato
# SEMPRE al modello.
#
# Serve a definire comportamento,
# stile e regole.

SYSTEM_PROMPT = {
    "role": "system",
    "content": """
    Sei un assistente AI tecnico.

    Rispondi in modo:

    - chiaro
    - preciso
    - pratico
    - educativo

    Quando spieghi codice,
    spiega anche il motivo
    delle scelte tecniche.
    """
}


# ==================================
# MODELLO INPUT CHAT
# ==================================

class ChatRequest(BaseModel):

    message: str


# ==================================
# HOME PAGE
# ==================================

@app.get("/")
def home():

    return {
        "status": "online",
        "message": "AI Lab attivo 🚀"
    }


# ==================================
# MEMORIA COMPLETA
# ==================================

@app.get("/memory")
def memory():

    return get_chat()


# ==================================
# COSTRUZIONE PROMPT
# ==================================

def build_messages(history):

    # Lista finale inviata all'LLM

    messages = [SYSTEM_PROMPT]

    # Aggiungiamo la cronologia

    for role, msg in history:

        # Filtriamo soltanto
        # i ruoli compatibili OpenAI

        if role in ["user", "assistant"]:

            messages.append({
                "role": role,
                "content": msg
            })

    return messages


# ==================================
# MOTORE AI
# ==================================

def generate_ai_response(history):

    # Recuperiamo API KEY

    api_key = os.getenv(
        "OPENROUTER_API_KEY"
    )

    # Convertiamo history
    # in formato OpenAI

    messages = build_messages(history)

    # ==================================
    # LOGGING PROMPT
    # ==================================

    print("\n===== PROMPT INVIATO =====")

    for msg in messages:
        print(msg)

    print("=========================\n")

    try:

        response = requests.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers={

                "Authorization":
                f"Bearer {api_key}",

                "Content-Type":
                "application/json"
            },

            json={

                "model":
                "openai/gpt-oss-20b",

                "messages":
                messages
            },

            # Se OpenRouter non risponde
            # entro 20 secondi,
            # interrompiamo la richiesta

            timeout=20
        )

        # Verifica codice risposta

        if response.status_code != 200:

            print(
                f"ERRORE OPENROUTER: "
                f"{response.status_code}"
            )

            return (
                f"Errore OpenRouter: "
                f"{response.status_code}"
            )

        # Conversione JSON

        data = response.json()

        # Estrazione testo AI

        ai_response = (
            data["choices"][0]
            ["message"]
            ["content"]
        )

        # ==================================
        # LOGGING RISPOSTA AI
        # ==================================

        print("\n===== RISPOSTA AI =====")
        print(ai_response)
        print("=======================\n")

        return ai_response

    except Exception as e:

        print(
            f"ERRORE CONNESSIONE AI: "
            f"{str(e)}"
        )

        return (
            f"Errore connessione AI: "
            f"{str(e)}"
        )


# ==================================
# CHAT PRINCIPALE
# ==================================

@app.post("/chat")
def chat(req: ChatRequest):

    # --------------------------
    # 1. Salvataggio utente
    # --------------------------

    add_chat(
        "user",
        req.message
    )

    # --------------------------
    # 2. Recupero ultimi messaggi
    # --------------------------

    history = get_last_chat(10)

    # ==================================
    # LOGGING HISTORY
    # ==================================

    print("\n===== HISTORY =====")

    for role, msg in history:
        print(f"{role}: {msg}")

    print("===================\n")

    # --------------------------
    # 3. Generazione risposta
    # --------------------------

    response = generate_ai_response(
        history
    )

    # --------------------------
    # 4. Salvataggio risposta
    # --------------------------

    add_chat(
        "assistant",
        response
    )

    # --------------------------
    # 5. Pulizia database
    # --------------------------

    trim_chat(200)

    # --------------------------
    # 6. Risposta API
    # --------------------------

    return {
        "input": req.message,
        "response": response,
        "memory_used": len(history)
    }
