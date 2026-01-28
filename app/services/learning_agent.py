from langchain_core.prompts import PromptTemplate
from app.core.llm import llm
from app.prompts.course_prompt import COURSE_TEMPLATE
from app.prompts.quiz_prompt import QUIZ_TEMPLATE
import json
import re


def generate_course_and_quiz(params):

    course_prompt = PromptTemplate.from_template(COURSE_TEMPLATE)

    course = llm.invoke(
        course_prompt.format(**params)
    ).content

    quiz_prompt = PromptTemplate.from_template(QUIZ_TEMPLATE)

    quiz_raw = llm.invoke(
        quiz_prompt.format(course=course)
    ).content

    # Extract JSON from response
    json_match = re.search(r'\[.*\]', quiz_raw, re.DOTALL)
    if json_match:
        quiz_json = json_match.group(0)
        quiz = json.loads(quiz_json)
    else:
        # Fallback quiz if JSON parsing fails
        quiz = [
            {
                "question": "What is the main topic of this course?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": 0
            }
        ]

    return course, quiz
