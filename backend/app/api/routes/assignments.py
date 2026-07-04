from fastapi import APIRouter

from app.schemas.assignments import AssignmentAnalysisRequest, AssignmentAnalysisResponse
from app.services.assignment_service import AssignmentService

router = APIRouter()


@router.post("/analyze", response_model=AssignmentAnalysisResponse)
def analyze_assignment(payload: AssignmentAnalysisRequest) -> AssignmentAnalysisResponse:
    return AssignmentService().analyze(payload)
