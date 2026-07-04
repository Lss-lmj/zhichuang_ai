from __future__ import annotations

from pydantic import BaseModel


class AssignmentAnalysisRequest(BaseModel):
    assignment_title: str
    course_id: str | None = None
    student_id: str | None = None
    rubric_id: str | None = None
    repository_url: str | None = None
    description: str | None = None


class AssignmentScore(BaseModel):
    dimension: str
    score: int
    summary: str


class AssignmentAnalysisResponse(BaseModel):
    report_id: str
    summary: str
    scores: list[AssignmentScore]
    findings: list[str]
    ai_generated: bool = True
