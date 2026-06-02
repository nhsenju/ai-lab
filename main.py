from fastapi import FastAPI
from pydantic import BaseModel
from db import init_db, add_chat, get_chat

app = FastAPI()
init_db()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "online", "message": "AI Lab attivo 🚀"}

@app.post("/chat")
def chat(req: ChatRequest):

    add_chat("user", req.message)

    history = get_chat()

    response = generate_ai_response(req.message)

    add_chat("ai", response)

    return {
        "input": req.message,
        "history": history,
        "response": response,
        "mode": "chat-log-memory"
    }

def generate_ai_response(message: str):
    return f"AI placeholder: {message}"
