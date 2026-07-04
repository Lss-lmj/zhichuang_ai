from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    scenario: str = "general"


class Citation(BaseModel):
    title: str
    source_type: str
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    ai_generated: bool = True
