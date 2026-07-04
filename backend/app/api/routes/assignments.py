from fastapi import APIRouter

from app.schemas.assignments import (
    AssignmentDashboardResponse,
    AssignmentAnalysisRequest,
    AssignmentAnalysisResponse,
)
from app.services.assignment_service import AssignmentService

router = APIRouter()


@router.post("/analyze", response_model=AssignmentAnalysisResponse)
def analyze_assignment(payload: AssignmentAnalysisRequest) -> AssignmentAnalysisResponse:
    return AssignmentService().analyze(payload)


@router.get("/{assignment_id}/reports/{student_id}", response_model=AssignmentAnalysisResponse)
def get_assignment_report(assignment_id: str, student_id: str) -> AssignmentAnalysisResponse:
    return AssignmentService().get_report(assignment_id, student_id)


@router.get("/{assignment_id}/dashboard", response_model=AssignmentDashboardResponse)
def get_assignment_dashboard(assignment_id: str) -> AssignmentDashboardResponse:
    return AssignmentService().get_dashboard(assignment_id)
