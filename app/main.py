from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.routers import chat, quiz, audio

app = FastAPI(title="JANGG AI API", description="Intelligent API for interactive learning with AI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(audio.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>JANGG AI API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; color: #2c3e50; margin-bottom: 30px; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }
            .method { color: #27ae60; font-weight: bold; }
            .path { color: #2980b9; font-family: monospace; }
            .description { color: #34495e; margin-top: 5px; }
            .docs-link { background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 JANGG AI API</h1>
            <p>Intelligent API for interactive learning with AI</p>
        </div>
        
        <h2>📚 Available Endpoints</h2>
        
        <div class="endpoint">
            <span class="method">GET</span> <span class="path">/</span>
            <div class="description">API home page</div>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <span class="path">/health</span>
            <div class="description">API health check</div>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/chat/</span>
            <div class="description">AI chat interface for interactive conversations</div>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/quiz/generate</span>
            <div class="description">Generate personalized quizzes based on a topic</div>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/quiz/validate</span>
            <div class="description">Validate quiz answers</div>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/audio/text-to-speech</span>
            <div class="description">Convert text to speech</div>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/audio/speech-to-text</span>
            <div class="description">Convert speech to text</div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/docs" class="docs-link">📖 Interactive Documentation (Swagger)</a>
            <br><br>
            <a href="/redoc" class="docs-link">📋 Alternative Documentation (ReDoc)</a>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #7f8c8d;">
            <p>© 2026 JANGG AI API - Intelligent Learning Platform</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "api": "JANGG AI API", "version": "1.0.0"}
