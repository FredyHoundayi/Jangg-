from pydantic import BaseModel, Field


class LearnRequest(BaseModel):
    topic: str = Field(..., description="The topic to learn about")
    sector: str = Field(..., description="The target sector (e.g., finance, tech, healthcare)")
    tone: str = Field(..., description="The tone of the content (e.g., friendly, formal, casual)")
    style: str = Field(..., description="The style of explanation (e.g., simple, detailed, technical)")
    length: str = Field(..., description="Length of the course (short or full)")
