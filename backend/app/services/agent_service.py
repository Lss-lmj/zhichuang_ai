from app.schemas.agent import ChatRequest, ChatResponse, Citation
from app.rag.pipeline import RagPipeline


class AgentService:
    def chat(self, payload: ChatRequest) -> ChatResponse:
        answer, chunks = RagPipeline().answer(payload.message)
        return ChatResponse(
            answer=answer,
            citations=[
                Citation(
                    title=chunk.title,
                    source_type=chunk.source_type,
                    snippet=chunk.content,
                )
                for chunk in chunks
            ],
        )
