# Importiamo FastAPI per creare il server web
from fastapi import FastAPI

# Serve per definire la struttura dei dati ricevuti
from pydantic import BaseModel

# Importiamo le funzioni del database
from db import init_db, add_chat, get_chat

# Permette di leggere le variabili d'ambiente
import os

# Serve per fare richieste HTTP verso OpenRouter
import requests


# Creazione dell'app FastAPI
app = FastAPI()


# Inizializzazione del database all'avvio del server
init_db()


# ==========================
# MODELLO DATI INPUT CHAT
# ==========================

# Quando un utente invia un messaggio,
# FastAPI si aspetta un JSON tipo:
#
# {
#   "message": "ciao"
# }
#
class ChatRequest(BaseModel):
    message: str


# ==========================
# HOME PAGE
# ==========================

@app.get("/")
def home():

    # Endpoint di test
    # Serve per verificare che il server sia online

    return {
        "status": "online",
        "message": "AI Lab attivo 🚀"
    }


# ==========================
# MEMORIA
# ==========================

@app.get("/memory")
def memory():

    # Restituisce tutto lo storico salvato

    return get_chat()


# ==========================
# CHAT PRINCIPALE
# ==========================

@app.post("/chat")
def chat(req: ChatRequest):

    # ----------------------------------
    # 1. Salviamo il messaggio utente
    # ----------------------------------

    add_chat("user", req.message)

    # ----------------------------------
    # 2. Recuperiamo tutta la chat
    # ----------------------------------

    history = get_chat()

    # ----------------------------------
    # 3. Chiediamo risposta all'AI
    # ----------------------------------

    response = generate_ai_response(history)

    # ----------------------------------
    # 4. Salviamo la risposta AI
    # ----------------------------------

    add_chat("ai", response)

    # ----------------------------------
    # 5. Restituiamo il risultato
    # ----------------------------------

    return {
        "input": req.message,
        "history": history,
        "response": response,
        "mode": "openrouter-ai"
    }


# ==========================
# MOTORE AI
# ==========================

def generate_ai_response(history):

    # Leggiamo la chiave OpenRouter
    # salvata su Render

    api_key = os.getenv("OPENROUTER_API_KEY")

    # Lista messaggi che verrà inviata al modello

    messages = []

    # ----------------------------------
    # MEMORIA LIMITATA
    # ----------------------------------
    #
    # Prendiamo solo gli ultimi 10 messaggi
    #
    # Esempio:
    #
    # history[-10:]
    #
    # significa:
    #
    # "dammi gli ultimi 10 elementi"
    #

    if history:

        last_messages = history[-10:]

        for role, msg in last_messages:

            messages.append({
                "role": role,
                "content": msg
            })

    # ----------------------------------
    # CHIAMATA OPENROUTER
    # ----------------------------------

    response = requests.post(

        "https://openrouter.ai/api/v1/chat/completions",

        headers={

            # Autenticazione

            "Authorization": f"Bearer {api_key}",

            # Tipo dati

            "Content-Type": "application/json"
        },

        json={

            # Modello scelto

            "model": "openai/gpt-oss-20b",

            # Conversazione inviata

            "messages": messages
        }
    )

    # Convertiamo la risposta JSON
    # ricevuta dal server

    data = response.json()

    # Estraiamo il testo generato

    return data["choices"][0]["message"]["content"]
