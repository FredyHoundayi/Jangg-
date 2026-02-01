from pydantic import BaseModel, Field
from typing import List, Optional


class Scene(BaseModel):
    title: str = Field(..., description="Title of the scene")
    content: str = Field(..., description="Content/narration for the scene")
    duration: int = Field(..., description="Duration in seconds")


class VideoRequest(BaseModel):
    topic: str = Field(..., description="Topic of the course")
    style: str = Field(default="cartoon", description="Visual style for video generation")
    tone: str = Field(default="fun", description="Tone of the content")
    language: str = Field(default="fr", description="Language for audio generation")
    scenes: List[Scene] = Field(..., description="List of scenes for the video")


class VideoResponse(BaseModel):
    video_path: str = Field(..., description="Path to the generated video file")
    message: str = Field(..., description="Status message")
    processing_time: Optional[float] = Field(None, description="Total processing time in seconds")
