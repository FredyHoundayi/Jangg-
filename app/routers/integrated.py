from fastapi import APIRouter, HTTPException
from app.schemas.chat import LearnRequest
from app.schemas.complete_course import CompleteCourseResponse, VideoFromScenesRequest
from app.services.learning_agent import generate_complete_learning_package
from app.services.video_service import video_service
import time

router = APIRouter(prefix="/integrated", tags=["Integrated Learning"])


@router.post("/complete-course", response_model=CompleteCourseResponse)
def generate_complete_learning_experience(req: LearnRequest):
    """
    Generate a complete learning package in a single LLM inference.
    
    This endpoint generates:
    1. Course content
    2. Quiz questions  
    3. Video-ready scenes with visual prompts
    
    All content is generated coherently in one LLM call for better consistency.
    """
    try:
        start_time = time.time()
        
        # Generate everything in one inference
        complete_data = generate_complete_learning_package(req.dict())
        
        processing_time = time.time() - start_time
        
        return CompleteCourseResponse(
            course=complete_data["course"],
            quiz=complete_data["quiz"],
            video_scenes=complete_data["video_scenes"],
            message="Complete learning package generated successfully",
            generation_method="unified_llm"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Complete course generation failed: {str(e)}"
        )


@router.post("/video-from-scenes")
def generate_video_from_scenes(req: VideoFromScenesRequest):
    """
    Generate video from pre-generated scenes.
    
    Use this with scenes from /integrated/complete-course for optimal results.
    """
    try:
        start_time = time.time()
        
        # Convert scenes to video service format
        video_data = {
            "topic": req.topic,
            "style": req.style,
            "tone": req.tone,
            "language": req.language,
            "scenes": [
                {
                    "title": scene.title,
                    "content": scene.content,
                    "duration": scene.duration
                }
                for scene in req.scenes
            ]
        }
        
        video_path = video_service.generate_course_video(video_data)
        
        processing_time = time.time() - start_time
        
        return {
            "video_path": video_path,
            "scenes_used": len(req.scenes),
            "processing_time": processing_time,
            "message": "Video generated from scenes successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Video from scenes generation failed: {str(e)}"
        )


@router.post("/full-pipeline")
def generate_full_learning_pipeline(req: LearnRequest):
    """
    Complete pipeline: generate content AND create video in one call.
    
    This combines content generation and video creation for maximum convenience.
    """
    try:
        start_time = time.time()
        
        # Step 1: Generate complete content package
        complete_data = generate_complete_learning_package(req.dict())
        
        # Step 2: Generate video from the scenes
        video_data = {
            "topic": req.topic,
            "style": req.style,
            "tone": req.tone,
            "language": "fr",
            "scenes": complete_data["video_scenes"]
        }
        
        video_path = video_service.generate_course_video(video_data)
        
        total_time = time.time() - start_time
        
        return {
            "course": complete_data["course"],
            "quiz": complete_data["quiz"],
            "video_scenes": complete_data["video_scenes"],
            "video_path": video_path,
            "total_processing_time": total_time,
            "generation_method": "unified_llm_plus_video",
            "message": "Full learning pipeline completed successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Full pipeline generation failed: {str(e)}"
        )
