from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "AI Lab attivo 🚀"
    }

# 🔥 AGGIUNTA IMPORTANTE PER RENDER
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(app, host="0.0.0.0", port=port)
