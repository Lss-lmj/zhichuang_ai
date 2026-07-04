from __future__ import annotations

from pydantic import BaseModel, Field


class CapabilityDimension(BaseModel):
    dimension: str
    score: int
    confidence: float
    summary: str
    evidence: list[str] = Field(default_factory=list)


class GrowthProfileResponse(BaseModel):
    student_id: str
    student_name: str
    target_path: str
    generated_at: str
    dimensions: list[CapabilityDimension]
    strengths: list[str]
    risks: list[str]
    next_actions: list[str]
    ai_generated: bool = True


class LearningPlanRequest(BaseModel):
    student_id: str = "student_001"
    goal: str = "三个月内完成 AI 应用开发 Demo 并准备校级双创项目"
    weeks: int = 8


class PlanTask(BaseModel):
    week: int
    title: str
    outcome: str
    resources: list[str] = Field(default_factory=list)


class LearningPlanResponse(BaseModel):
    plan_id: str
    student_id: str
    goal: str
    weeks: int
    overview: str
    tasks: list[PlanTask]
    checkpoints: list[str]
    ai_generated: bool = True


class CompetitionRecommendRequest(BaseModel):
    student_id: str = "student_001"
    target: str = "AI 应用开发与软件项目实践"
    available_weeks: int = 8


class CompetitionRecommendation(BaseModel):
    name: str
    category: str
    match_score: int
    reason: str
    preparation: list[str]
    risk: str


class CompetitionRecommendResponse(BaseModel):
    student_id: str
    target: str
    recommendations: list[CompetitionRecommendation]
    ai_generated: bool = True


class TeamRecommendRequest(BaseModel):
    student_id: str = "student_001"
    project_goal: str = "做一个课程作业代码分析与教师看板 Demo"
    team_request_id: str | None = None


class TeamCandidate(BaseModel):
    student_id: str
    name: str
    role: str
    match_score: int
    complement: str
    evidence: list[str] = Field(default_factory=list)


class TeamRecommendResponse(BaseModel):
    requester_id: str
    project_goal: str
    candidates: list[TeamCandidate]
    collaboration_tips: list[str]
    ai_generated: bool = True


class TeamRequestCreate(BaseModel):
    student_id: str = "student_001"
    competition_name: str = "中国大学生计算机设计大赛"
    project_direction: str = "AI 应用开发与教学智能体"
    missing_roles: list[str] = Field(default_factory=lambda: ["前端与交互", "算法与评测"])
    expected_skills: list[str] = Field(default_factory=lambda: ["React", "RAG", "测试评测"])
    weekly_hours: int = 8
    communication: str = "每周一次线上同步，平时使用项目文档和任务看板沟通"
    team_status_enabled: bool = True


class TeamRequestCard(BaseModel):
    team_request_id: str
    student_id: str
    competition_name: str
    project_direction: str
    missing_roles: list[str]
    expected_skills: list[str]
    weekly_hours: int
    communication: str
    team_status_enabled: bool
    contact_visible: bool
    status: str
    created_at: str


class TeamPoolStatus(BaseModel):
    student_id: str
    team_status_enabled: bool
    contact_visible: bool
    visibility_note: str
