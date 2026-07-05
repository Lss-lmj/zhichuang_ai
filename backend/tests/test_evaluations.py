from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.schemas.evaluations import EvaluationCaseCreate, EvaluationRecordCreate
from app.services.evaluation_service import EvaluationService


def test_evaluation_dashboard_contains_three_records() -> None:
    client = TestClient(app)
    response = client.get("/api/evaluations/dashboard")

    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["total_cases"] >= 3
    assert payload["summary"]["completed_records"] >= 3
    assert payload["summary"]["average_score"] >= 80
    assert len(payload["records"]) >= 3
    assert payload["records"][0]["citations"]
    assert payload["records"][0]["issue_notes"]


def test_admin_can_create_evaluation_case_and_record() -> None:
    client = TestClient(app)
    case_response = client.post(
        "/api/evaluations/cases",
        headers={"Authorization": "Bearer demo-token-admin_001"},
        json={
            "scenario": "竞赛准备计划",
            "input_question": "为中国大学生计算机设计大赛生成 4 周准备计划",
            "expected_focus": ["时间节点", "官方依据", "交付物"],
            "priority": "P0",
            "status": "已记录",
        },
    )
    record_response = client.post(
        "/api/evaluations/records",
        headers={"Authorization": "Bearer demo-token-admin_001"},
        json={
            "case_id": case_response.json()["item_id"],
            "scenario": "竞赛准备计划",
            "input_question": "为中国大学生计算机设计大赛生成 4 周准备计划",
            "system_output": "系统生成 4 周准备计划，包含报名节点和作品交付物。",
            "manual_score": 88,
            "issue_notes": "计划结构完整，引用依据明确。",
            "reviewer": "项目评测组",
        },
    )
    forbidden_response = client.post(
        "/api/evaluations/cases",
        headers={"Authorization": "Bearer demo-token-student_001"},
        json={"scenario": "学生尝试维护评测"},
    )
    dashboard_response = client.get("/api/evaluations/dashboard")

    assert case_response.status_code == 200
    assert record_response.status_code == 200
    assert forbidden_response.status_code == 403
    assert dashboard_response.json()["summary"]["total_cases"] >= 4
    assert dashboard_response.json()["summary"]["completed_records"] >= 4
    assert any(
        record["record_id"] == record_response.json()["item_id"]
        for record in dashboard_response.json()["records"]
    )


def test_admin_can_export_evaluation_report() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/evaluations/export",
        headers={"Authorization": "Bearer demo-token-admin_001"},
    )
    forbidden_response = client.get(
        "/api/evaluations/export",
        headers={"Authorization": "Bearer demo-token-student_001"},
    )

    assert response.status_code == 200
    assert forbidden_response.status_code == 403
    payload = response.json()
    assert payload["filename"].endswith(".md")
    assert payload["content_type"] == "text/markdown; charset=utf-8"
    assert "# 测试评测报告" in payload["markdown"]
    assert "## 测试案例" in payload["markdown"]
    assert "## 输出记录" in payload["markdown"]
    assert "知识库问答" in payload["markdown"]
    assert "引用来源" in payload["markdown"]


def test_evaluation_case_and_record_persist_in_sqlite_session(tmp_path) -> None:
    engine = create_engine(
        f"sqlite:///{tmp_path / 'evaluations.db'}",
        connect_args={"check_same_thread": False},
    )
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    with SessionLocal() as first_session:
        service = EvaluationService(first_session)
        case = service.create_case(
            EvaluationCaseCreate(
                scenario="教师看板稳定性",
                input_question="验证作业分析报告是否能跨服务实例读取",
                expected_focus=["报告持久化", "教师看板", "访问控制"],
                priority="P0",
                status="已记录",
            )
        )
        record = service.create_record(
            EvaluationRecordCreate(
                case_id=case.item_id,
                scenario="教师看板稳定性",
                input_question="验证作业分析报告是否能跨服务实例读取",
                system_output="报告已写入 SQLite，教师看板可汇总已分析报告。",
                manual_score=91,
                issue_notes="持久化链路可复现。",
                reviewer="项目评测组",
            )
        )

    with SessionLocal() as second_session:
        dashboard = EvaluationService(second_session).dashboard()

    assert any(item.case_id == case.item_id for item in dashboard.cases)
    assert any(item.record_id == record.item_id for item in dashboard.records)
    assert dashboard.summary.total_cases >= 4
    assert dashboard.summary.completed_records >= 4
    assert dashboard.summary.average_score >= 80
