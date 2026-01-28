from fastapi import APIRouter
from app.schemas.quiz import QuizEvaluation
from app.services.quiz_service import evaluate_quiz

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.post("/evaluate")
def evaluate(req: QuizEvaluation):

    score, feedback = evaluate_quiz(req.quiz, req.answers)

    return {
        "score": score,
        "feedback": feedback
    }
