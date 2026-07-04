from __future__ import annotations

from app.rag.pipeline import DEMO_CHUNKS, RagPipeline
from app.schemas.knowledge import (
    KnowledgeDocument,
    KnowledgeDocumentsResponse,
    KnowledgeSearchResponse,
    KnowledgeSearchResult,
)


class KnowledgeService:
    updated_at = "2026-07-05T09:30:00+08:00"

    def list_documents(self) -> KnowledgeDocumentsResponse:
        documents = [
            KnowledgeDocument(
                document_id=f"doc_{index:03d}",
                title=chunk.title,
                source_type=chunk.source_type,
                path=chunk.path,
                tags=chunk.tags,
                chunk_count=1,
                status="已入库",
                updated_at=self.updated_at,
            )
            for index, chunk in enumerate(DEMO_CHUNKS, start=1)
        ]
        return KnowledgeDocumentsResponse(total=len(documents), documents=documents)

    def search(self, query: str, limit: int = 5) -> KnowledgeSearchResponse:
        chunks = RagPipeline().retrieve(query, limit=limit)
        results = [
            KnowledgeSearchResult(
                title=chunk.title,
                source_type=chunk.source_type,
                path=chunk.path,
                snippet=chunk.content,
                score=round(chunk.score, 3),
                tags=chunk.tags,
            )
            for chunk in chunks
        ]
        return KnowledgeSearchResponse(query=query, total=len(results), results=results)
