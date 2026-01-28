from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.audio_service import text_to_audio

router = APIRouter(prefix="/audio", tags=["Audio"])


class AudioRequest(BaseModel):
    text: str = Field(..., description="Text to convert to audio")


@router.post("/generate")
def generate_audio(req: AudioRequest):
    try:
        audio_url = text_to_audio(req.text)
        return {
            "audio_url": audio_url,
            "message": "Audio generated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")
