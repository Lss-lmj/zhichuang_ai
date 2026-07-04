from __future__ import annotations

from dataclasses import dataclass, field
from re import findall


@dataclass
class RetrievedChunk:
    title: str
    source_type: str
    content: str
    score: float
    path: str
    tags: list[str] = field(default_factory=list)


DEMO_CHUNKS = [
    RetrievedChunk(
        title="Web 应用开发课程作业 Rubric",
        source_type="rubric",
        path="软件项目实践",
        tags=["作业分析", "Rubric", "Web"],
        content=(
            "课程作业评分参考功能完成度、代码结构、工程规范、测试意识和文档表达。"
            "报告需要给出证据，不把分数表达为绝对能力判断。"
        ),
        score=0,
    ),
    RetrievedChunk(
        title="软件项目实践案例模板",
        source_type="project_case",
        path="软件项目实践",
        tags=["项目案例", "README", "接口设计"],
        content=(
            "项目案例建议包含需求背景、功能清单、技术栈、数据模型、接口设计、"
            "测试记录、评价 Rubric 和可扩展方向。"
        ),
        score=0,
    ),
    RetrievedChunk(
        title="AI 应用开发学习路径",
        source_type="course_material",
        path="AI 应用开发",
        tags=["RAG", "Agent", "大模型应用"],
        content=(
            "AI 应用开发首批路径包括 Prompt 基础、RAG 文档问答、Agent 工作流、"
            "评测记录和应用部署。建议先完成一个带引用的课程知识库问答 Demo。"
        ),
        score=0,
    ),
    RetrievedChunk(
        title="算法竞赛训练路径",
        source_type="competition_material",
        path="算法竞赛",
        tags=["蓝桥杯", "算法", "训练计划"],
        content=(
            "算法竞赛准备建议按基础语法、常用数据结构、搜索、动态规划、图论和真题复盘推进。"
            "训练计划应结合可用时间和已有题量。"
        ),
        score=0,
    ),
    RetrievedChunk(
        title="组队推荐能力互补规则",
        source_type="project_rule",
        path="软件项目实践",
        tags=["组队推荐", "能力画像", "双创"],
        content=(
            "组队推荐需要说明能力互补关系，例如算法、后端、前端、产品表达和项目管理。"
            "推荐理由应基于证据，不直接给出未经解释的名单。"
        ),
        score=0,
    ),
    RetrievedChunk(
        title="教师学情诊断看板说明",
        source_type="teacher_dashboard",
        path="软件项目实践",
        tags=["教师看板", "作业分析", "学情诊断"],
        content=(
            "教师端直接查看班级提交情况、维度分布、共性问题和学生个人作业报告。"
            "教师端不是审核流程，而是学情分析结果消费端。"
        ),
        score=0,
    ),
]


class RagPipeline:
    def retrieve(self, query: str, limit: int = 3) -> list[RetrievedChunk]:
        tokens = self._tokenize(query)
        scored = []
        for chunk in DEMO_CHUNKS:
            haystack = " ".join([chunk.title, chunk.content, chunk.path, " ".join(chunk.tags)])
            score = self._score(tokens, haystack)
            if score > 0:
                scored.append(
                    RetrievedChunk(
                        title=chunk.title,
                        source_type=chunk.source_type,
                        content=chunk.content,
                        path=chunk.path,
                        tags=chunk.tags,
                        score=score,
                    )
                )

        if not scored:
            scored = [
                RetrievedChunk(
                    title=chunk.title,
                    source_type=chunk.source_type,
                    content=chunk.content,
                    path=chunk.path,
                    tags=chunk.tags,
                    score=0.1,
                )
                for chunk in DEMO_CHUNKS[:limit]
            ]

        return sorted(scored, key=lambda item: item.score, reverse=True)[:limit]

    def answer(self, query: str) -> tuple[str, list[RetrievedChunk]]:
        chunks = self.retrieve(query)
        answer = self._compose_answer(query, chunks)
        return answer, chunks

    def _compose_answer(self, query: str, chunks: list[RetrievedChunk]) -> str:
        lead = "基于当前首批知识库资料，可以这样处理："
        if "竞赛" in query or "蓝桥" in query or "算法" in query:
            lead = "如果目标是算法竞赛准备，建议按训练路径拆成阶段任务："
        elif "作业" in query or "代码" in query or "教师" in query:
            lead = "如果目标是课程作业分析和教师学情诊断，建议围绕证据生成报告："
        elif "组队" in query:
            lead = "如果目标是组队推荐，建议先明确项目目标和能力互补关系："
        elif "RAG" in query or "知识库" in query or "Agent" in query:
            lead = "如果目标是 AI 应用开发，可以先完成带引用的知识库问答闭环："

        bullets = [f"{index}. {chunk.content}" for index, chunk in enumerate(chunks, start=1)]
        return "\n".join([lead, *bullets])

    def _tokenize(self, query: str) -> set[str]:
        normalized = query.lower()
        words = set(findall(r"[a-zA-Z0-9_]+", normalized))
        keywords = {
            "作业",
            "代码",
            "教师",
            "看板",
            "学情",
            "竞赛",
            "算法",
            "蓝桥",
            "组队",
            "项目",
            "案例",
            "知识库",
            "大模型",
            "RAG",
            "Agent",
            "测试",
            "Rubric",
        }
        return words | {keyword for keyword in keywords if keyword.lower() in normalized}

    def _score(self, tokens: set[str], haystack: str) -> float:
        normalized = haystack.lower()
        matched = sum(1 for token in tokens if token.lower() in normalized)
        return matched / max(len(tokens), 1)
