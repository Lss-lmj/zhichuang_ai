from uuid import uuid4

from app.schemas.assignments import (
    AssignmentAnalysisRequest,
    AssignmentAnalysisResponse,
    AssignmentScore,
)


class AssignmentService:
    def analyze(self, payload: AssignmentAnalysisRequest) -> AssignmentAnalysisResponse:
        return AssignmentAnalysisResponse(
            report_id=str(uuid4()),
            summary=f"{payload.assignment_title} 的代码分析任务已创建。当前返回占位报告。",
            scores=[
                AssignmentScore(dimension="功能完成度", score=0, summary="等待代码分析工作流执行。"),
                AssignmentScore(dimension="代码结构", score=0, summary="等待项目结构解析。"),
                AssignmentScore(dimension="工程规范", score=0, summary="等待 README、依赖和测试检查。"),
            ],
            findings=["MVP 阶段将由 CodeAnalysisGraph 生成正式报告。"],
        )
