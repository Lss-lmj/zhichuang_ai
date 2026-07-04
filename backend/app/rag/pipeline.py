from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    title: str
    source_type: str
    content: str
    score: float


class RagPipeline:
    def answer(self, query: str) -> tuple[str, list[RetrievedChunk]]:
        chunk = RetrievedChunk(
            title="RAG Pipeline 占位资料",
            source_type="system",
            content="后续接入课程大纲、作业要求、评分 Rubric、竞赛规则和项目案例。",
            score=1.0,
        )
        return f"RAG 占位回答：{query}", [chunk]
