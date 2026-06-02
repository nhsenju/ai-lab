from fastapi import FastAPI
from pydantic import BaseModel
from db import init_db, set_memory, get_memory
import requests


app = FastAPI()
init_db()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "online", "message": "AI Lab attivo 🚀"}

@app.get("/memory")
def memory():
    return get_memory()

from db import add_chat, get_chat

@app.post("/chat")
def chat(req: ChatRequest):

    # salva user
    add_chat("user", req.message)

    # leggi storico
    history = get_chat()

    # risposta AI
    response = generate_ai_response(req.message)

    # salva AI
    add_chat("ai", response)

    return {
        "input": req.message,
        "history": history,
        "response": response,
        "mode": "chat-log-memory"
    }

def generate_ai_response(message: str):

    # 🔥 QUI INSERIREMO IL MODELLO AI (step successivo)
    return f"AI placeholder: {message}"
