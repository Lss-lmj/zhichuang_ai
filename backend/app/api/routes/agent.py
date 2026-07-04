from fastapi import APIRouter

from app.schemas.agent import ChatRequest, ChatResponse
from app.services.agent_service import AgentService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    return AgentService().chat(payload)
