from __future__ import annotations

from pydantic import BaseModel, Field


class KnowledgeDocument(BaseModel):
    document_id: str
    title: str
    source_type: str
    path: str
    tags: list[str] = Field(default_factory=list)
    chunk_count: int
    status: str
    updated_at: str


class KnowledgeSearchResult(BaseModel):
    title: str
    source_type: str
    path: str
    snippet: str
    score: float
    tags: list[str] = Field(default_factory=list)


class KnowledgeSearchResponse(BaseModel):
    query: str
    total: int
    results: list[KnowledgeSearchResult]


class KnowledgeDocumentsResponse(BaseModel):
    total: int
    documents: list[KnowledgeDocument]
