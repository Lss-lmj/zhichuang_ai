from fastapi import APIRouter

from app.schemas.growth import (
    CompetitionRecommendRequest,
    CompetitionRecommendResponse,
    GrowthProfileResponse,
    LearningPlanRequest,
    LearningPlanResponse,
    TeamRecommendRequest,
    TeamRecommendResponse,
)
from app.services.growth_service import GrowthService

router = APIRouter()


@router.get("/students/{student_id}/profile", response_model=GrowthProfileResponse)
def get_student_profile(student_id: str) -> GrowthProfileResponse:
    return GrowthService().get_profile(student_id)


@router.post("/plans/generate", response_model=LearningPlanResponse)
def generate_plan(payload: LearningPlanRequest) -> LearningPlanResponse:
    return GrowthService().generate_plan(payload)


@router.post("/competitions/recommend", response_model=CompetitionRecommendResponse)
def recommend_competitions(
    payload: CompetitionRecommendRequest,
) -> CompetitionRecommendResponse:
    return GrowthService().recommend_competitions(payload)


@router.post("/teams/recommend", response_model=TeamRecommendResponse)
def recommend_team(payload: TeamRecommendRequest) -> TeamRecommendResponse:
    return GrowthService().recommend_team(payload)
