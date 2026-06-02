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

@app.post("/chat")
def chat(req: ChatRequest):

    # 1. salva input utente
    set_memory("user", req.message)

    # 2. leggi memoria
    history = get_memory()

    # 3. genera risposta (per ora mock)
    response = generate_ai_response(req.message)

    # 4. salva risposta AI
    set_memory("ai", response)

    return {
        "input": req.message,
        "memory": history,
        "response": response,
        "mode": "memory-active"
    }


def generate_ai_response(message: str):

    # 🔥 QUI INSERIREMO IL MODELLO AI (step successivo)
    return f"AI placeholder: {message}"
