from fastapi.testclient import TestClient

from app.main import app


def test_assignment_analysis_returns_report() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/assignments/analyze",
        json={
            "assignment_title": "Flask Web 项目实践",
            "student_id": "student_001",
            "repository_url": "https://example.edu/demo/flask-project",
            "description": "示例作业包含 Flask 路由、SQLite 数据访问、README 和基础测试。",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["student_name"] == "林一舟"
    assert len(payload["scores"]) == 5
    assert payload["findings"][0]["severity"] == "high"


def test_assignment_dashboard_returns_teacher_view() -> None:
    client = TestClient(app)
    response = client.get("/api/assignments/assignment_flask_mvp/dashboard")

    assert response.status_code == 200
    payload = response.json()
    assert payload["submitted_count"] == 5
    assert payload["total_students"] == 32
    assert len(payload["reports"]) == 5
