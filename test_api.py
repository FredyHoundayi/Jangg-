#!/usr/bin/env python3
"""
Script de test simple pour l'API JANGG
"""
import sys
import os

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    # Créer une version simplifiée de l'API pour tester
    app = FastAPI(title="JANGG API Test", version="1.0.0")
    
    @app.get("/")
    async def root():
        return {"message": "JANGG API is running!", "status": "healthy"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "api": "JANGG API", "version": "1.0.0"}
    
    @app.get("/test-endpoints")
    async def test_endpoints():
        """Liste des endpoints disponibles"""
        endpoints = {
            "chat": {
                "path": "/chat/learn",
                "method": "POST",
                "description": "Générer cours et quiz",
                "input": {
                    "topic": "Finance personnelle",
                    "sector": "finance",
                    "tone": "friendly",
                    "style": "simple",
                    "length": "full"
                }
            },
            "quiz": {
                "path": "/quiz/evaluate",
                "method": "POST", 
                "description": "Évaluer les réponses du quiz"
            },
            "audio": {
                "path": "/audio/generate",
                "method": "POST",
                "description": "Convertir texte en audio"
            },
            "video": {
                "path": "/video/generate",
                "method": "POST",
                "description": "Générer vidéo avec IA"
            },
            "integrated": {
                "complete-course": {
                    "path": "/integrated/complete-course",
                    "method": "POST",
                    "description": "Générer package complet (cours + quiz + scènes vidéo) en une inference"
                },
                "video-from-scenes": {
                    "path": "/integrated/video-from-scenes", 
                    "method": "POST",
                    "description": "Générer vidéo à partir des scènes"
                },
                "full-pipeline": {
                    "path": "/integrated/full-pipeline",
                    "method": "POST",
                    "description": "Pipeline complet (contenu + vidéo) en un appel"
                }
            }
        }
        return {"endpoints": endpoints, "total_count": len(endpoints)}
    
    if __name__ == "__main__":
        import uvicorn
        print("🚀 Lancement de l'API JANGG en mode test...")
        print("📖 Documentation: http://localhost:8000/docs")
        print("🔍 Test endpoints: http://localhost:8000/test-endpoints")
        uvicorn.run(app, host="0.0.0.0", port=8000)

except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("📦 Installation des dépendances de base...")
    os.system("pip3 install fastapi uvicorn --break-system-packages")
    print("✅ Installation terminée. Relancez le script.")
