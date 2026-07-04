from __future__ import annotations

from pydantic import BaseModel, Field


class EvaluationCitation(BaseModel):
    title: str
    source_type: str
    path: str
    snippet: str


class EvaluationCase(BaseModel):
    case_id: str
    scenario: str
    input_question: str
    expected_focus: list[str] = Field(default_factory=list)
    priority: str
    status: str


class EvaluationRecord(BaseModel):
    record_id: str
    case_id: str
    scenario: str
    input_question: str
    system_output: str
    citations: list[EvaluationCitation] = Field(default_factory=list)
    manual_score: int
    issue_notes: str
    reviewer: str
    evaluated_at: str
    ai_generated: bool = True


class EvaluationSummary(BaseModel):
    total_cases: int
    completed_records: int
    average_score: int
    pass_rate: int


class EvaluationDashboardResponse(BaseModel):
    summary: EvaluationSummary
    cases: list[EvaluationCase]
    records: list[EvaluationRecord]
