from __future__ import annotations

from datetime import datetime
from hashlib import sha1

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models.evaluation import EvaluationCaseRecord, EvaluationRecordItem
from app.schemas.evaluations import (
    EvaluationCase,
    EvaluationCaseCreate,
    EvaluationCitation,
    EvaluationDashboardResponse,
    EvaluationExportResponse,
    EvaluationRecord,
    EvaluationRecordCreate,
    EvaluationSummary,
    EvaluationUpsertResponse,
)


class EvaluationService:
    evaluated_at = "2026-07-05T10:30:00+08:00"

    cases = [
        EvaluationCase(
            case_id="eval_rag_algorithm_path",
            scenario="知识库问答",
            input_question="如何准备算法竞赛？",
            expected_focus=[
                "引用课程与竞赛资料",
                "给出阶段任务",
                "提示不确定信息需核验",
            ],
            priority="P0",
            status="已记录",
        ),
        EvaluationCase(
            case_id="eval_assignment_report",
            scenario="项目分析",
            input_question="分析 Flask Web 项目的工程质量和改进建议",
            expected_focus=["展示多维度评分", "关联代码证据", "给出下一步任务"],
            priority="P0",
            status="已记录",
        ),
        EvaluationCase(
            case_id="eval_growth_recommendation",
            scenario="成长与双创推荐",
            input_question="为 AI 应用开发方向学生推荐竞赛和队友",
            expected_focus=["说明适合原因", "说明需补足能力", "展示推荐证据"],
            priority="P0",
            status="已记录",
        ),
    ]

    records = [
        EvaluationRecord(
            record_id="record_001",
            case_id="eval_rag_algorithm_path",
            scenario="知识库问答",
            input_question="如何准备算法竞赛？",
            system_output=(
                "建议先按搜索、动态规划、图论和数学基础建立题单；"
                "每周保留固定复盘，比赛时间和规则以官方通知为准。"
            ),
            citations=[
                EvaluationCitation(
                    title="算法竞赛训练路径",
                    source_type="learning_path",
                    path="算法竞赛",
                    snippet=(
                        "算法竞赛首批路径包含搜索、动态规划、图论"
                        "和数学基础。"
                    ),
                ),
                EvaluationCitation(
                    title="蓝桥杯备赛说明",
                    source_type="competition",
                    path="算法竞赛",
                    snippet="竞赛安排、组别和报名节点应以官方通知为准。",
                ),
            ],
            manual_score=86,
            issue_notes=(
                "路径拆解清晰；后续需要补更多官方赛事链接和年份信息。"
            ),
            reviewer="项目评测组",
            evaluated_at=evaluated_at,
        ),
        EvaluationRecord(
            record_id="record_002",
            case_id="eval_assignment_report",
            scenario="项目分析",
            input_question="分析 Flask Web 项目的工程质量和改进建议",
            system_output=(
                "报告识别出路由、数据库模块和 README 基础完整，"
                "但测试覆盖、异常处理和输入校验不足；"
                "建议补充接口测试和错误提示样例。"
            ),
            citations=[
                EvaluationCitation(
                    title="Web 应用开发项目 Rubric",
                    source_type="rubric",
                    path="软件项目实践",
                    snippet=(
                        "课程项目评分参考功能完成度、代码结构、工程规范、"
                        "测试意识和文档表达。"
                    ),
                ),
            ],
            manual_score=90,
            issue_notes=(
                "能关联 Rubric 和项目证据；可继续补充具体文件级定位。"
            ),
            reviewer="项目评测组",
            evaluated_at=evaluated_at,
        ),
        EvaluationRecord(
            record_id="record_003",
            case_id="eval_growth_recommendation",
            scenario="成长与双创推荐",
            input_question="为 AI 应用开发方向学生推荐竞赛和队友",
            system_output=(
                "推荐中国大学生计算机设计大赛和中国国际大学生创新大赛"
                "作为主路径；"
                "队友侧优先匹配前端交互、算法评测和产品答辩能力互补者。"
            ),
            citations=[
                EvaluationCitation(
                    title="AI 应用开发项目案例",
                    source_type="project_case",
                    path="AI 应用开发",
                    snippet=(
                        "首个作品原型应聚焦可展示、可复现、"
                        "可解释的真实学习或教学场景。"
                    ),
                ),
                EvaluationCitation(
                    title="组队推荐证据规则",
                    source_type="policy",
                    path="软件项目实践",
                    snippet=(
                        "推荐结果需要展示能力依据、来源证据、"
                        "短板和下一步行动。"
                    ),
                ),
            ],
            manual_score=84,
            issue_notes="推荐理由完整；后续要把竞赛资料库扩展到更多赛道。",
            reviewer="项目评测组",
            evaluated_at=evaluated_at,
        ),
    ]

    def __init__(self, db: Session | None = None) -> None:
        self.db = db
        if self.db is not None:
            Base.metadata.create_all(bind=self.db.get_bind())
            self._ensure_seed_data()

    def dashboard(self) -> EvaluationDashboardResponse:
        cases = self.list_cases()
        records = self.list_records()
        average_score = round(
            sum(record.manual_score for record in records) / len(records)
        ) if records else 0
        passed = len([record for record in records if record.manual_score >= 80])
        pass_rate = round(passed / len(records) * 100) if records else 0

        return EvaluationDashboardResponse(
            summary=EvaluationSummary(
                total_cases=len(cases),
                completed_records=len(records),
                average_score=average_score,
                pass_rate=pass_rate,
            ),
            cases=cases,
            records=records,
        )

    def export_report(self) -> EvaluationExportResponse:
        dashboard = self.dashboard()
        generated_at = datetime.utcnow().isoformat()
        return EvaluationExportResponse(
            filename="evaluation_reproducible_report.md",
            markdown=self._report_markdown(dashboard, generated_at),
            generated_at=generated_at,
        )

    def list_cases(self) -> list[EvaluationCase]:
        if self.db is None:
            return self.cases
        records = self.db.scalars(
            select(EvaluationCaseRecord).order_by(
                EvaluationCaseRecord.created_at.asc(),
                EvaluationCaseRecord.id.asc(),
            )
        ).all()
        return [self._case_from_record(record) for record in records]

    def list_records(self) -> list[EvaluationRecord]:
        if self.db is None:
            return self.records
        records = self.db.scalars(
            select(EvaluationRecordItem).order_by(
                EvaluationRecordItem.evaluated_at.asc(),
                EvaluationRecordItem.id.asc(),
            )
        ).all()
        return [self._record_from_item(record) for record in records]

    def create_case(self, payload: EvaluationCaseCreate) -> EvaluationUpsertResponse:
        case_id = self._case_id(payload)
        if self.db is None:
            self.cases.append(
                EvaluationCase(
                    case_id=case_id,
                    scenario=payload.scenario,
                    input_question=payload.input_question,
                    expected_focus=payload.expected_focus,
                    priority=payload.priority,
                    status=payload.status,
                )
            )
            return EvaluationUpsertResponse(item_id=case_id, message="测试案例已记录。")

        existing = self.db.get(EvaluationCaseRecord, case_id)
        if existing is None:
            self.db.add(self._case_record(case_id, payload))
        else:
            existing.scenario = payload.scenario
            existing.input_question = payload.input_question
            existing.expected_focus_json = payload.expected_focus
            existing.priority = payload.priority
            existing.status = payload.status
        self.db.commit()
        return EvaluationUpsertResponse(item_id=case_id, message="测试案例已记录。")

    def create_record(self, payload: EvaluationRecordCreate) -> EvaluationUpsertResponse:
        record_id = self._record_id(payload)
        if self.db is None:
            self.records.append(
                EvaluationRecord(
                    record_id=record_id,
                    case_id=payload.case_id,
                    scenario=payload.scenario,
                    input_question=payload.input_question,
                    system_output=payload.system_output,
                    citations=payload.citations or self._default_citations(payload.scenario),
                    manual_score=payload.manual_score,
                    issue_notes=payload.issue_notes,
                    reviewer=payload.reviewer,
                    evaluated_at=self.evaluated_at,
                )
            )
            return EvaluationUpsertResponse(item_id=record_id, message="测试输出记录已保存。")

        existing = self.db.get(EvaluationRecordItem, record_id)
        if existing is None:
            self.db.add(self._record_item(record_id, payload))
        else:
            existing.case_id = payload.case_id
            existing.scenario = payload.scenario
            existing.input_question = payload.input_question
            existing.system_output = payload.system_output
            existing.citations_json = [
                citation.model_dump(mode="json")
                for citation in (payload.citations or self._default_citations(payload.scenario))
            ]
            existing.manual_score = payload.manual_score
            existing.issue_notes = payload.issue_notes
            existing.reviewer = payload.reviewer
            existing.evaluated_at = datetime.utcnow()
        self.db.commit()
        return EvaluationUpsertResponse(item_id=record_id, message="测试输出记录已保存。")

    def _ensure_seed_data(self) -> None:
        if self.db is None:
            return
        for item in self.cases:
            if self.db.get(EvaluationCaseRecord, item.case_id) is None:
                self.db.add(
                    EvaluationCaseRecord(
                        id=item.case_id,
                        scenario=item.scenario,
                        input_question=item.input_question,
                        expected_focus_json=item.expected_focus,
                        priority=item.priority,
                        status=item.status,
                        created_at=datetime.utcnow(),
                    )
                )
        for item in self.records:
            if self.db.get(EvaluationRecordItem, item.record_id) is None:
                self.db.add(
                    EvaluationRecordItem(
                        id=item.record_id,
                        case_id=item.case_id,
                        scenario=item.scenario,
                        input_question=item.input_question,
                        system_output=item.system_output,
                        citations_json=[
                            citation.model_dump(mode="json") for citation in item.citations
                        ],
                        manual_score=item.manual_score,
                        issue_notes=item.issue_notes,
                        reviewer=item.reviewer,
                        evaluated_at=self._parse_datetime(item.evaluated_at),
                    )
                )
        self.db.commit()

    def _case_id(self, payload: EvaluationCaseCreate) -> str:
        raw = f"{payload.scenario}:{payload.input_question}".encode("utf-8")
        return f"eval_custom_{sha1(raw).hexdigest()[:10]}"

    def _record_id(self, payload: EvaluationRecordCreate) -> str:
        raw = (
            f"{payload.case_id}:{payload.scenario}:{payload.input_question}:"
            f"{payload.system_output}"
        ).encode("utf-8")
        return f"record_custom_{sha1(raw).hexdigest()[:10]}"

    def _case_record(
        self,
        case_id: str,
        payload: EvaluationCaseCreate,
    ) -> EvaluationCaseRecord:
        return EvaluationCaseRecord(
            id=case_id,
            scenario=payload.scenario,
            input_question=payload.input_question,
            expected_focus_json=payload.expected_focus,
            priority=payload.priority,
            status=payload.status,
            created_at=datetime.utcnow(),
        )

    def _record_item(
        self,
        record_id: str,
        payload: EvaluationRecordCreate,
    ) -> EvaluationRecordItem:
        citations = payload.citations or self._default_citations(payload.scenario)
        return EvaluationRecordItem(
            id=record_id,
            case_id=payload.case_id,
            scenario=payload.scenario,
            input_question=payload.input_question,
            system_output=payload.system_output,
            citations_json=[citation.model_dump(mode="json") for citation in citations],
            manual_score=payload.manual_score,
            issue_notes=payload.issue_notes,
            reviewer=payload.reviewer,
            evaluated_at=datetime.utcnow(),
        )

    def _case_from_record(self, record: EvaluationCaseRecord) -> EvaluationCase:
        return EvaluationCase(
            case_id=record.id,
            scenario=record.scenario,
            input_question=record.input_question,
            expected_focus=list(record.expected_focus_json or []),
            priority=record.priority,
            status=record.status,
        )

    def _record_from_item(self, record: EvaluationRecordItem) -> EvaluationRecord:
        return EvaluationRecord(
            record_id=record.id,
            case_id=record.case_id,
            scenario=record.scenario,
            input_question=record.input_question,
            system_output=record.system_output,
            citations=[
                EvaluationCitation(**citation) for citation in list(record.citations_json or [])
            ],
            manual_score=record.manual_score,
            issue_notes=record.issue_notes,
            reviewer=record.reviewer,
            evaluated_at=record.evaluated_at.isoformat(),
        )

    def _parse_datetime(self, value: str) -> datetime:
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return datetime.utcnow()

    def _default_citations(self, scenario: str) -> list[EvaluationCitation]:
        return [
            EvaluationCitation(
                title=f"{scenario}测试依据",
                source_type="evaluation_case",
                path="测试评测",
                snippet="评测记录需要保存输入、输出、引用来源、评分和问题记录。",
            )
        ]

    def _report_markdown(
        self,
        dashboard: EvaluationDashboardResponse,
        generated_at: str,
    ) -> str:
        lines = [
            "# 测试评测报告",
            "",
            f"- 生成时间：{generated_at}",
            f"- 测试案例：{dashboard.summary.total_cases}",
            f"- 输出记录：{dashboard.summary.completed_records}",
            f"- 平均评分：{dashboard.summary.average_score}",
            f"- 通过率：{dashboard.summary.pass_rate}%",
            "",
            "> 本报告由系统汇总测试案例、输出记录、引用来源、评分和问题记录生成，用于技术验证、演示复现和迭代跟踪。",
            "",
            "## 核心指标",
            "",
            "| 指标 | 数值 |",
            "| --- | --- |",
            f"| 测试案例 | {dashboard.summary.total_cases} |",
            f"| 输出记录 | {dashboard.summary.completed_records} |",
            f"| 平均评分 | {dashboard.summary.average_score} |",
            f"| 通过率 | {dashboard.summary.pass_rate}% |",
            "",
            "## 测试案例",
            "",
            "| 场景 | 优先级 | 状态 | 输入问题 | 关注点 |",
            "| --- | --- | --- | --- | --- |",
        ]
        lines.extend(
            (
                f"| {item.scenario} | {item.priority} | {item.status} | "
                f"{self._cell(item.input_question)} | "
                f"{self._cell('；'.join(item.expected_focus)) or '-'} |"
            )
            for item in dashboard.cases
        )
        lines.extend(["", "## 输出记录", ""])
        for record in dashboard.records:
            lines.extend(
                [
                    f"### {record.scenario} · {record.manual_score} 分",
                    "",
                    f"- 记录 ID：{record.record_id}",
                    f"- 案例 ID：{record.case_id}",
                    f"- 输入问题：{record.input_question}",
                    f"- 评价人：{record.reviewer}",
                    f"- 评价时间：{record.evaluated_at}",
                    f"- 问题记录：{record.issue_notes}",
                    "",
                    "**系统输出**",
                    "",
                    record.system_output,
                    "",
                    "**引用来源**",
                    "",
                ]
            )
            if record.citations:
                lines.extend(
                    (
                        f"- {citation.title}（{citation.source_type} / {citation.path}）："
                        f"{citation.snippet}"
                    )
                    for citation in record.citations
                )
            else:
                lines.append("- 无")
            lines.append("")
        return "\n".join(lines)

    def _cell(self, value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ")
