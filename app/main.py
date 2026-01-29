from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import chat, quiz, audio

app = FastAPI(title="Brain API MVP")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(audio.router)

@app.get("/")
async def root():
    return {"status": "healthy", "message": "JANGG AI API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
