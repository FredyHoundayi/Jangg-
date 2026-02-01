COMPLETE_COURSE_TEMPLATE = """
You are a friendly AI tutor and content creator.

Generate a complete learning package about {topic} for the {sector} sector.

Parameters:
- Tone: {tone}
- Style: {style} 
- Length: {length}
- Language: French

Requirements:
1. Generate engaging course content
2. Create relevant quiz questions
3. Structure content for video generation with scenes

Format your response as JSON:

{{
  "course": "Complete course content with clear sections and examples",
  "quiz": [
    {{
      "question": "Clear question about the content",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": 2
    }}
  ],
  "video_scenes": [
    {{
      "title": "Scene title",
      "content": "Narration text for this scene (2-3 sentences)",
      "duration": 8,
      "visual_prompt": "Visual description for AI image generation"
    }}
  ]
}}

Rules:
- Course: Clear, structured, beginner-friendly with practical examples
- Quiz: 5 questions testing key concepts
- Video Scenes: 5-8 scenes covering the main topics
- Each scene content should be speakable (natural for text-to-speech)
- Visual prompts should be descriptive for image generation
- Duration per scene: 5-12 seconds based on content length

Return only valid JSON.
"""
