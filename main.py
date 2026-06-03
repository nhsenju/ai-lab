from fastapi import FastAPI
from pydantic import BaseModel
from db import init_db, add_chat, get_chat
import os
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
    return get_chat()


@app.post("/chat")
def chat(req: ChatRequest):

    # salva messaggio user
    add_chat("user", req.message)

    # recupera storia
    history = get_chat()

    # risposta AI vera
    response = generate_ai_response(req.message, history)

    # salva risposta AI
    add_chat("ai", response)

    return {
        "input": req.message,
        "history": history,
        "response": response,
        "mode": "openrouter-ai"
    }


def generate_ai_response(message: str, history=None):

    api_key = os.getenv("OPENROUTER_API_KEY")

    messages = []

    # aggiungiamo solo gli ultimi 10 messaggi
if history:
    last_messages = history[-10:]

    for role, msg in last_messages:
        messages.append({
            "role": role,
            "content": msg
        })

    # messaggio nuovo utente
    messages.append({
        "role": "user",
        "content": message
    })

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-oss-20b",
            "messages": messages
        }
    )

    data = response.json()

    return data["choices"][0]["message"]["content"]
