from fastapi import APIRouter

from app.api.routes import agent, assignments, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
api_router.include_router(assignments.router, prefix="/assignments", tags=["assignments"])
