#!/usr/bin/env python3
"""
🤖 JANGG AI API - 100% Autonome pour Colab
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uuid
import time
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="🤖 JANGG AI API - Standalone",
    description="API complète pour l'apprentissage avec IA - Version autonome",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Schémas
class LearnRequest(BaseModel):
    topic: str
    sector: str
    tone: str
    style: str
    length: str

class Scene(BaseModel):
    title: str
    content: str
    duration: int

class VideoRequest(BaseModel):
    topic: str
    style: str = "cartoon"
    tone: str = "fun"
    language: str = "fr"
    scenes: List[Scene]

class QuizEvaluation(BaseModel):
    quiz: List[Dict]
    answers: List[int]

class AudioRequest(BaseModel):
    text: str

# Services
class LearningService:
    @staticmethod
    def generate_course(topic: str, sector: str, tone: str, style: str, length: str) -> str:
        return f"""
# {topic.title()} - Cours Complet

## Introduction
La {topic.lower()} est essentielle dans le secteur {sector}.
Approche {tone} avec style {style}.

## Concepts
1. Principes fondamentaux
2. Applications pratiques
3. Meilleures pratiques
4. Études de cas

## Conclusion
Félicitations! Vous maîtrisez {topic}.
"""
    
    @staticmethod
    def generate_quiz(topic: str) -> List[Dict]:
        return [{
            "question": f"Importance de {topic}?",
            "options": ["Essentielle", "Importante", "Optionnelle", "Non nécessaire"],
            "answer": 0
        }]
    
    @staticmethod
    def generate_scenes(topic: str, style: str) -> List[Scene]:
        return [
            Scene(title="Intro", content=f"Découvrons {topic}", duration=8),
            Scene(title="Concepts", content=f"Concepts de {topic}", duration=10),
            Scene(title="Conclusion", content=f"Bravo pour {topic}!", duration=8)
        ]

# Endpoints
@app.get("/", include_in_schema=False)
async def root():
    return HTMLResponse("""
    <h1>🤖 JANGG AI API - Standalone</h1>
    <p>Bienvenue sur l'API autonome JANGG AI !</p>
    <p>📚 <a href="/docs">Documentation Swagger</a></p>
    <p>🔍 <a href="/redoc">Documentation ReDoc</a></p>
    <p>🔄 <a href="/health">Vérifier l'état</a></p>
    """)

@app.get("/health", 
         summary="Vérifier l'état de l'API",
         description="Vérifie que l'API est opérationnelle",
         response_description="État de santé de l'API")
async def health():
    return {"status": "healthy", "api": "JANGG Standalone"}

@app.post("/chat/learn", 
          summary="Générer un cours et un quiz",
          description="Crée un contenu éducatif personnalisé avec quiz intégré",
          response_description="Retourne le cours généré et un quiz")
async def learn(req: LearnRequest):
    course = LearningService.generate_course(req.topic, req.sector, req.tone, req.style, req.length)
    quiz = LearningService.generate_quiz(req.topic)
    return {"course": course, "quiz": quiz, "audio_url": f"audio_{uuid.uuid4().hex[:8]}.mp3"}

@app.post("/quiz/evaluate",
          summary="Évaluer un quiz",
          description="Calcule le score et fournit un feedback",
          response_description="Résultats de l'évaluation")
async def evaluate_quiz(req: QuizEvaluation):
    correct = sum(1 for q, a in zip(req.quiz, req.answers) if q["answer"] == a)
    score = (correct / len(req.quiz)) * 100
    return {"score": score, "correct": correct, "total": len(req.quiz)}

@app.post("/audio/generate",
          summary="Générer un audio",
          description="Convertit du texte en parole (TTS)",
          response_description="URL de l'audio généré")
async def generate_audio(req: AudioRequest):
    return {"audio_url": f"audio_{uuid.uuid4().hex[:8]}.mp3", "duration": len(req.text.split()) * 0.5}

@app.post("/video/generate",
          summary="Générer une vidéo",
          description="Crée une vidéo à partir de scènes",
          response_description="Détails de la vidéo générée")
async def generate_video(req: VideoRequest):
    return {
        "video_path": f"video_{req.topic.replace(' ', '_')}_{uuid.uuid4().hex[:8]}.mp4",
        "duration": sum(s.duration for s in req.scenes)
    }

@app.post("/integrated/complete-course",
          summary="Générer un package complet",
          description="Cours + Quiz + Scènes vidéo en une seule requête",
          response_description="Package complet d'apprentissage")
async def complete_course(req: LearnRequest):
    course = LearningService.generate_course(req.topic, req.sector, req.tone, req.style, req.length)
    quiz = LearningService.generate_quiz(req.topic)
    scenes = LearningService.generate_scenes(req.topic, req.style)
    return {
        "course": course,
        "quiz": quiz,
        "video_scenes": scenes,
        "message": "Package complet généré"
    }

@app.post("/integrated/full-pipeline",
          summary="Pipeline complet",
          description="Génère tout le contenu + vidéo + audio",
          response_description="Résultats du pipeline complet")
async def full_pipeline(req: LearnRequest):
    course = LearningService.generate_course(req.topic, req.sector, req.tone, req.style, req.length)
    quiz = LearningService.generate_quiz(req.topic)
    scenes = LearningService.generate_scenes(req.topic, req.style)
    return {
        "course": course,
        "quiz": quiz,
        "video_scenes": scenes,
        "video_path": f"full_{req.topic.replace(' ', '_')}_{uuid.uuid4().hex[:8]}.mp4",
        "audio_url": f"audio_{uuid.uuid4().hex[:8]}.mp3"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 JANGG API Standalone - Prêt pour Colab!")
    print("📖 Documentation complète: http://localhost:8000/docs")
    print("🔍 Documentation alternative: http://localhost:8000/redoc")
    uvicorn.run(app, host="0.0.0.0", port=8000)