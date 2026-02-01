from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, quiz, audio, video, integrated

app = FastAPI(
    title="🤖 JANGG AI API",
    description="API complète pour la génération de contenu éducatif avec IA",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routeurs
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
app.include_router(audio.router, prefix="/audio", tags=["Audio"])
app.include_router(video.router, prefix="/video", tags=["Video"])
app.include_router(integrated.router, prefix="/integrated", tags=["Integrated"])

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Bienvenue sur l'API JANGG AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

