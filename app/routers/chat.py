from fastapi import APIRouter
from app.schemas.chat import LearnRequest
from app.services.learning_agent import generate_course_and_quiz
from app.services.audio_service import text_to_audio

router = APIRouter(prefix="/chat", tags=["Learning"])


@router.post("/learn")
def learn(req: LearnRequest):

    course, quiz = generate_course_and_quiz(req.dict())

    audio_url = text_to_audio(course)

    return {
        "course": course,
        "quiz": quiz,
        "audio_url": audio_url
    }
