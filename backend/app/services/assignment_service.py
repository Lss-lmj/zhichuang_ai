from __future__ import annotations

from app.schemas.assignments import (
    AssignmentDashboardMetric,
    AssignmentDashboardResponse,
    AssignmentAnalysisRequest,
    AssignmentAnalysisResponse,
    AssignmentFinding,
    AssignmentReportSummary,
    AssignmentScore,
    CapabilityEvidence,
    Citation,
)


class AssignmentService:
    generated_at = "2026-07-04T21:00:00+08:00"

    course = {
        "id": "course_web_2026",
        "name": "Web 应用开发",
    }
    class_group = {
        "id": "class_cs_2024_01",
        "name": "2024 级计算机科学与技术 1 班",
    }
    assignment = {
        "id": "assignment_flask_mvp",
        "title": "Flask Web 项目实践",
    }
    students = {
        "student_001": "林一舟",
        "student_002": "陈星然",
        "student_003": "周明远",
        "student_004": "沈知夏",
        "student_005": "许嘉木",
    }

    def analyze(self, payload: AssignmentAnalysisRequest) -> AssignmentAnalysisResponse:
        student_id = payload.student_id or "student_001"
        return self._build_report(
            student_id=student_id,
            assignment_title=payload.assignment_title,
            course_id=payload.course_id or self.course["id"],
            class_id=payload.class_id or self.class_group["id"],
            repository_url=payload.repository_url,
            description=payload.description,
            file_count=len(payload.files),
        )

    def get_report(self, assignment_id: str, student_id: str) -> AssignmentAnalysisResponse:
        title = self.assignment["title"] if assignment_id == self.assignment["id"] else assignment_id
        return self._build_report(
            student_id=student_id,
            assignment_title=title,
            course_id=self.course["id"],
            class_id=self.class_group["id"],
            repository_url="https://example.edu/demo/flask-project",
            description="示例作业包含 Flask 路由、SQLite 数据访问、README 和基础测试。",
            file_count=18,
        )

    def get_dashboard(self, assignment_id: str) -> AssignmentDashboardResponse:
        reports = [self.get_report(assignment_id, student_id) for student_id in self.students]
        dimension_names = [score.dimension for score in reports[0].scores]
        dimension_averages = []
        for dimension in dimension_names:
            dimension_scores = [
                score.score
                for report in reports
                for score in report.scores
                if score.dimension == dimension
            ]
            avg = round(sum(dimension_scores) / len(dimension_scores))
            dimension_averages.append(
                AssignmentScore(
                    dimension=dimension,
                    score=avg,
                    summary=self._dimension_summary(dimension, avg),
                    evidence=[f"{len(dimension_scores)} 份提交的同维度证据汇总"],
                )
            )

        average_score = round(sum(self._overall_score(report) for report in reports) / len(reports))
        return AssignmentDashboardResponse(
            assignment_id=assignment_id,
            assignment_title=self.assignment["title"],
            course_id=self.course["id"],
            course_name=self.course["name"],
            class_id=self.class_group["id"],
            class_name=self.class_group["name"],
            generated_at=self.generated_at,
            submitted_count=len(reports),
            total_students=32,
            average_score=average_score,
            metrics=[
                AssignmentDashboardMetric(label="已提交", value="5 / 32", trend="演示样例"),
                AssignmentDashboardMetric(label="平均分", value=str(average_score), trend="+6 较上次项目"),
                AssignmentDashboardMetric(label="共性问题", value="3", trend="集中在测试和异常处理"),
                AssignmentDashboardMetric(label="讲评重点", value="2", trend="分层设计、测试覆盖"),
            ],
            dimension_averages=dimension_averages,
            common_findings=[
                AssignmentFinding(
                    severity="medium",
                    title="异常路径处理不足",
                    detail="多数提交覆盖了主流程，但对表单为空、数据库写入失败等情况缺少处理。",
                    suggestion="讲评时可以集中演示请求校验、异常捕获和错误提示的标准写法。",
                ),
                AssignmentFinding(
                    severity="medium",
                    title="测试覆盖偏弱",
                    detail="示例提交中只有少量同学提供接口测试或 service 层单元测试。",
                    suggestion="下一次作业要求提交至少 3 个 API 测试和 2 个业务逻辑测试。",
                ),
                AssignmentFinding(
                    severity="low",
                    title="README 运行说明不完整",
                    detail="部分项目缺少环境变量、初始化数据库和启动命令说明。",
                    suggestion="提供课程统一 README 模板，作为工程规范评分依据。",
                ),
            ],
            reports=[
                AssignmentReportSummary(
                    report_id=report.report_id,
                    student_id=report.student_id,
                    student_name=report.student_name,
                    overall_score=self._overall_score(report),
                    status="已分析",
                    summary=report.summary,
                )
                for report in reports
            ],
        )

    def _build_report(
        self,
        student_id: str,
        assignment_title: str,
        course_id: str,
        class_id: str,
        repository_url: str | None,
        description: str | None,
        file_count: int,
    ) -> AssignmentAnalysisResponse:
        student_name = self.students.get(student_id, "演示学生")
        repository_signal = bool(repository_url)
        description_signal = bool(description and len(description) >= 20)
        file_signal = min(file_count, 20)
        base = 72 + (4 if repository_signal else 0) + (3 if description_signal else 0)
        structure_score = min(92, base + file_signal // 3)
        quality_score = min(88, base - 2 + file_signal // 4)
        test_score = min(82, base - 8 + file_signal // 5)
        document_score = min(90, base + (6 if description_signal else 0))

        scores = [
            AssignmentScore(
                dimension="功能完成度",
                score=min(90, base + 5),
                summary="核心页面、接口和数据流基本完整，主流程可以闭环运行。",
                evidence=["存在作业入口、数据提交路径和结果展示结构", "能围绕课程要求解释实现结果"],
            ),
            AssignmentScore(
                dimension="代码结构",
                score=structure_score,
                summary="项目具备基本分层，路由、业务逻辑和配置有初步边界。",
                evidence=["可识别入口文件和业务模块", "模块命名与 Web 项目结构基本一致"],
            ),
            AssignmentScore(
                dimension="工程规范",
                score=quality_score,
                summary="依赖、配置和运行说明具备雏形，异常处理和日志仍可加强。",
                evidence=["有 README 或作业描述支撑运行说明", "部分边界情况缺少稳定处理"],
            ),
            AssignmentScore(
                dimension="测试意识",
                score=test_score,
                summary="能看到基础验证意识，但自动化测试数量和覆盖面仍不足。",
                evidence=["主流程可人工验证", "接口和 service 层测试证据偏少"],
            ),
            AssignmentScore(
                dimension="文档表达",
                score=document_score,
                summary="能描述项目目标和运行方式，建议补充架构图、接口说明和已知限制。",
                evidence=["作业描述和 README 可支持教师快速了解项目", "改进建议可追溯到提交物"],
            ),
        ]

        return AssignmentAnalysisResponse(
            report_id=f"report_{self.assignment['id']}_{student_id}",
            assignment_id=self.assignment["id"],
            assignment_title=assignment_title,
            course_id=course_id,
            course_name=self.course["name"],
            class_id=class_id,
            class_name=self.class_group["name"],
            student_id=student_id,
            student_name=student_name,
            generated_at=self.generated_at,
            summary=(
                f"{student_name} 的提交已经完成多维度分析。整体表现显示其具备 Web 项目主流程搭建能力，"
                "后续应重点提升异常处理、自动化测试和工程文档完整度。"
            ),
            scores=[
                *scores,
            ],
            findings=[
                AssignmentFinding(
                    severity="high",
                    title="测试覆盖不足",
                    detail="当前提交更偏向功能实现，缺少对登录失败、空表单、数据库异常等路径的自动化测试。",
                    suggestion="补充 pytest 或前端请求层测试，并将关键异常路径纳入评分 Rubric。",
                ),
                AssignmentFinding(
                    severity="medium",
                    title="配置和业务逻辑边界仍可加强",
                    detail="部分运行参数和业务处理容易混在同一层，后续扩展课程项目时维护成本会上升。",
                    suggestion="将配置读取、数据库访问和页面路由拆到独立模块，保持 service 层职责清晰。",
                ),
                AssignmentFinding(
                    severity="low",
                    title="项目说明可继续结构化",
                    detail="说明中已经能看出项目目标，但缺少接口、数据表和启动步骤的稳定格式。",
                    suggestion="按课程模板补齐环境准备、启动命令、接口列表和已知问题。",
                ),
            ],
            capability_evidence=[
                CapabilityEvidence(
                    dimension="工程实践",
                    evidence="能完成 Web 项目从需求到页面、接口、数据流的基础闭环。",
                    source="课程作业代码提交",
                ),
                CapabilityEvidence(
                    dimension="问题拆解",
                    evidence="提交物体现出按功能模块拆解任务的意识，但边界说明仍需加强。",
                    source="项目结构与 README",
                ),
                CapabilityEvidence(
                    dimension="质量意识",
                    evidence="具备基础运行验证，但自动化测试和异常处理证据不足。",
                    source="测试文件与代码路径分析",
                ),
            ],
            improvement_tasks=[
                "补充至少 3 个接口测试，覆盖成功、失败和空输入路径。",
                "把数据库连接、环境变量和业务 service 拆分到独立模块。",
                "按课程模板补齐 README 中的启动步骤、接口说明和数据表说明。",
            ],
            citations=[
                Citation(
                    title="Web 应用开发课程作业 Rubric",
                    source_type="rubric",
                    snippet="评分参考功能完成度、代码结构、工程规范、测试意识和文档表达。",
                ),
                Citation(
                    title="软件项目实践知识库",
                    source_type="knowledge_base",
                    snippet="项目报告应包含需求背景、架构设计、接口设计、测试和可扩展方向。",
                ),
            ],
        )

    def _overall_score(self, report: AssignmentAnalysisResponse) -> int:
        return round(sum(score.score for score in report.scores) / len(report.scores))

    def _dimension_summary(self, dimension: str, score: int) -> str:
        if score >= 85:
            return f"{dimension}整体表现较好，可作为讲评中的正向样例。"
        if score >= 75:
            return f"{dimension}达到课程阶段要求，但仍有集中改进空间。"
        return f"{dimension}低于预期，需要在下一次作业中重点跟进。"
