import time
from fastapi import APIRouter, HTTPException
from app.schemas.video import VideoRequest, VideoResponse
from app.services.video_service import video_service

router = APIRouter(prefix="/video", tags=["Video"])


@router.post("/generate", response_model=VideoResponse)
def generate_course_video(request: VideoRequest):
    """
    Generate a course video based on the provided scenes and settings.
    
    This endpoint creates a video by:
    1. Generating images for each scene using Stable Diffusion
    2. Converting text to speech using gTTS
    3. Creating video segments with FFmpeg
    4. Concatenating all segments into a final video
    """
    try:
        start_time = time.time()
        
        # Convert request to dict for service
        course_data = {
            "topic": request.topic,
            "style": request.style,
            "tone": request.tone,
            "language": request.language,
            "scenes": [
                {
                    "title": scene.title,
                    "content": scene.content,
                    "duration": scene.duration
                }
                for scene in request.scenes
            ]
        }
        
        # Generate video
        video_path = video_service.generate_course_video(course_data)
        
        processing_time = time.time() - start_time
        
        return VideoResponse(
            video_path=video_path,
            message="Video generated successfully",
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Video generation failed: {str(e)}"
        )


@router.get("/health")
def video_health_check():
    """Check if video generation service is available"""
    try:
        # Check if the model is loaded
        model_loaded = video_service.pipe is not None
        return {
            "status": "healthy" if model_loaded else "degraded",
            "model_loaded": model_loaded,
            "service": "video_generation"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Video service unavailable: {str(e)}"
        )
