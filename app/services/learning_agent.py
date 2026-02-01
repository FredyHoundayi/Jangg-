from langchain_core.prompts import PromptTemplate
from app.core.llm import llm
from app.prompts.course_prompt import COURSE_TEMPLATE
from app.prompts.quiz_prompt import QUIZ_TEMPLATE
from app.prompts.complete_course_prompt import COMPLETE_COURSE_TEMPLATE
import json
import re


def generate_course_and_quiz(params):
    """Legacy function - generates course and quiz separately"""
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


def generate_complete_learning_package(params):
    """
    Generate course, quiz, and video-ready scenes in a single LLM inference.
    
    Returns:
        dict: {
            "course": str,
            "quiz": list,
            "video_scenes": list
        }
    """
    complete_prompt = PromptTemplate.from_template(COMPLETE_COURSE_TEMPLATE)
    
    response = llm.invoke(
        complete_prompt.format(**params)
    ).content
    
    # Extract JSON from response
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        try:
            complete_data = json.loads(json_match.group(0))
            
            # Validate structure
            required_keys = ["course", "quiz", "video_scenes"]
            if all(key in complete_data for key in required_keys):
                return complete_data
            else:
                raise ValueError("Missing required keys in LLM response")
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return _fallback_generation(params)
    else:
        print("No JSON found in LLM response")
        return _fallback_generation(params)


def _fallback_generation(params):
    """Fallback to separate generation if unified approach fails"""
    print("Falling back to separate generation...")
    course, quiz = generate_course_and_quiz(params)
    
    # Basic scene parsing from course
    scenes = []
    sections = re.split(r'\n\d+\.\s*|\n\n', course)
    sections = [s.strip() for s in sections if s.strip()]
    
    for i, section in enumerate(sections[:8]):
        sentences = section.split('.')
        title = sentences[0].strip() if sentences else section[:50]
        content = section.strip()
        duration = max(5, min(15, len(content.split()) * 0.5))
        
        scenes.append({
            "title": title,
            "content": content,
            "duration": int(duration),
            "visual_prompt": f"{params.get('style', 'cartoon')}, {title}, educational content"
        })
    
    return {
        "course": course,
        "quiz": quiz,
        "video_scenes": scenes
    }
