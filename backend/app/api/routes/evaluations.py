from fastapi import APIRouter

from app.schemas.evaluations import (
    EvaluationCase,
    EvaluationDashboardResponse,
    EvaluationRecord,
)
from app.services.evaluation_service import EvaluationService

router = APIRouter()


@router.get("/dashboard", response_model=EvaluationDashboardResponse)
def get_evaluation_dashboard() -> EvaluationDashboardResponse:
    return EvaluationService().dashboard()


@router.get("/cases", response_model=list[EvaluationCase])
def list_evaluation_cases() -> list[EvaluationCase]:
    return EvaluationService().list_cases()


@router.get("/records", response_model=list[EvaluationRecord])
def list_evaluation_records() -> list[EvaluationRecord]:
    return EvaluationService().list_records()
