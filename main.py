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

    return {
        "input": req.message,
        "response": generate_ai_response(req.message),
        "mode": "external-ai"
    }


def generate_ai_response(message: str):

    # 🔥 QUI INSERIREMO IL MODELLO AI (step successivo)
    return f"AI placeholder: {message}"
