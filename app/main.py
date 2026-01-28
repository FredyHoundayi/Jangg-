from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import chat, quiz, audio

app = FastAPI(title="Brain API MVP")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(audio.router)
