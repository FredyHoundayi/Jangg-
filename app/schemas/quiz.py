from pydantic import BaseModel
from typing import List, Dict


class QuizEvaluation(BaseModel):
    quiz: List[Dict]
    answers: List[int]
