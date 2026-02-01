from pydantic import BaseModel, Field
from typing import List, Dict


class VideoScene(BaseModel):
    title: str = Field(..., description="Title of the video scene")
    content: str = Field(..., description="Narration text for the scene")
    duration: int = Field(..., description="Duration in seconds")
    visual_prompt: str = Field(..., description="Visual description for AI image generation")


class CompleteCourseResponse(BaseModel):
    course: str = Field(..., description="Complete course content")
    quiz: List[Dict] = Field(..., description="Quiz questions with options and answers")
    video_scenes: List[VideoScene] = Field(..., description="Scenes ready for video generation")
    message: str = Field(default="Complete learning package generated successfully")
    generation_method: str = Field(default="unified", description="How the content was generated")


class VideoFromScenesRequest(BaseModel):
    topic: str = Field(..., description="Topic of the course")
    style: str = Field(default="cartoon", description="Visual style")
    tone: str = Field(default="educational", description="Content tone")
    language: str = Field(default="fr", description="Language for audio")
    scenes: List[VideoScene] = Field(..., description="Pre-generated scenes")
