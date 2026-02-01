# JANGG API

API complète pour la génération de contenu éducatif avec IA

## Installation

1. Cloner le dépôt
2. Créer un environnement virtuel : `python -m venv venv`
3. Activer l'environnement :
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Installer les dépendances : `pip install -r requirements.txt`
5. Copier `.env.example` vers `.env` et configurer les variables
6. Lancer l'API : `uvicorn main:app --reload`

## Structure

- `app/` - Code source principal
  - `routers/` - Définition des routes API
  - `schemas/` - Modèles Pydantic
  - `services/` - Logique métier
  - `prompts/` - Templates pour les prompts IA
- `static/` - Fichiers statiques (images, audio, vidéos)
- `main.py` - Point d'entrée de l'application

