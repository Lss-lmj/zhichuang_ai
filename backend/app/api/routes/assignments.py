from fastapi import APIRouter, Header

from app.schemas.assignments import (
    AssignmentDashboardResponse,
    AssignmentAnalysisRequest,
    AssignmentAnalysisResponse,
)
from app.services.assignment_service import AssignmentService
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/analyze", response_model=AssignmentAnalysisResponse)
def analyze_assignment(
    payload: AssignmentAnalysisRequest,
    authorization: str | None = Header(default=None),
) -> AssignmentAnalysisResponse:
    account = AuthService().current_account(authorization)
    return AssignmentService().analyze(payload, account=account)


@router.get("/{assignment_id}/reports/{student_id}", response_model=AssignmentAnalysisResponse)
def get_assignment_report(
    assignment_id: str,
    student_id: str,
    authorization: str | None = Header(default=None),
) -> AssignmentAnalysisResponse:
    account = AuthService().current_account(authorization)
    return AssignmentService().get_report(assignment_id, student_id, account=account)


@router.get("/{assignment_id}/dashboard", response_model=AssignmentDashboardResponse)
def get_assignment_dashboard(
    assignment_id: str,
    authorization: str | None = Header(default=None),
) -> AssignmentDashboardResponse:
    account = AuthService().current_account(authorization)
    return AssignmentService().get_dashboard(assignment_id, account=account)
