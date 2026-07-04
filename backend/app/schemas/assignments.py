from __future__ import annotations

from pydantic import BaseModel, Field


class CodeFile(BaseModel):
    path: str
    content: str = ""


class AssignmentAnalysisRequest(BaseModel):
    assignment_title: str
    course_id: str | None = None
    class_id: str | None = None
    student_id: str | None = None
    rubric_id: str | None = None
    repository_url: str | None = None
    description: str | None = None
    files: list[CodeFile] = Field(default_factory=list)


class AssignmentScore(BaseModel):
    dimension: str
    score: int
    summary: str
    evidence: list[str] = Field(default_factory=list)


class AssignmentFinding(BaseModel):
    severity: str
    title: str
    detail: str
    suggestion: str


class CapabilityEvidence(BaseModel):
    dimension: str
    evidence: str
    source: str


class CodeStructureSummary(BaseModel):
    file_count: int
    entry_files: list[str] = Field(default_factory=list)
    test_files: list[str] = Field(default_factory=list)
    documentation_files: list[str] = Field(default_factory=list)
    config_files: list[str] = Field(default_factory=list)
    detected_frameworks: list[str] = Field(default_factory=list)
    detected_capabilities: list[str] = Field(default_factory=list)
    risk_signals: list[str] = Field(default_factory=list)


class Citation(BaseModel):
    title: str
    source_type: str
    snippet: str


class AssignmentReportSummary(BaseModel):
    report_id: str
    student_id: str
    student_name: str
    overall_score: int
    status: str
    summary: str


class AssignmentDashboardMetric(BaseModel):
    label: str
    value: str
    trend: str | None = None


class TeachingSuggestion(BaseModel):
    knowledge_point: str
    class_evidence: str
    suggested_activity: str
    practice_task: str
    expected_improvement: str


class AbilityHeatmapCell(BaseModel):
    student_id: str
    student_name: str
    dimension: str
    score: int
    level: str


class DirectionDistributionItem(BaseModel):
    direction: str
    count: int
    ratio: float


class DataCoverageMetric(BaseModel):
    label: str
    covered: int
    total: int
    ratio: float


class ClassAbilityProfile(BaseModel):
    heatmap: list[AbilityHeatmapCell] = Field(default_factory=list)
    direction_distribution: list[DirectionDistributionItem] = Field(default_factory=list)
    data_coverage: list[DataCoverageMetric] = Field(default_factory=list)
    common_weaknesses: list[str] = Field(default_factory=list)
    summary: str


class AssignmentAnalysisResponse(BaseModel):
    report_id: str
    assignment_id: str
    assignment_title: str
    course_id: str
    course_name: str
    class_id: str
    class_name: str
    student_id: str
    student_name: str
    generated_at: str
    summary: str
    code_structure: CodeStructureSummary
    scores: list[AssignmentScore]
    findings: list[AssignmentFinding]
    capability_evidence: list[CapabilityEvidence]
    improvement_tasks: list[str]
    citations: list[Citation] = Field(default_factory=list)
    access_scope: str = "demo"
    ai_generated: bool = True


class AssignmentDashboardResponse(BaseModel):
    assignment_id: str
    assignment_title: str
    course_id: str
    course_name: str
    class_id: str
    class_name: str
    generated_at: str
    submitted_count: int
    total_students: int
    average_score: int
    metrics: list[AssignmentDashboardMetric]
    dimension_averages: list[AssignmentScore]
    common_findings: list[AssignmentFinding]
    teaching_suggestions: list[TeachingSuggestion]
    class_profile: ClassAbilityProfile
    reports: list[AssignmentReportSummary]
    access_scope: str = "demo"
    ai_generated: bool = True
