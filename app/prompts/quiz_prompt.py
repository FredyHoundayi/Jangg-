QUIZ_TEMPLATE = """
Based on this course, generate 5 MCQ questions.

Course:
{course}

Return STRICT JSON:

[
 {{
   "question": "...",
   "options": ["A","B","C","D"],
   "answer": 0
 }}
]
"""
