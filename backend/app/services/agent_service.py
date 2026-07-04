from app.schemas.agent import ChatRequest, ChatResponse, Citation


class AgentService:
    def chat(self, payload: ChatRequest) -> ChatResponse:
        return ChatResponse(
            answer=(
                "这是一个占位回答。后续将由 LangGraph 工作流调用 RAG、画像、"
                "作业分析和推荐服务生成可追溯结果。"
            ),
            citations=[
                Citation(
                    title="首批知识库资料需求",
                    source_type="project_document",
                    snippet="课程大纲、课程作业要求、评分 Rubric、代码样例、竞赛规则、项目案例和常见问题。",
                )
            ],
        )
