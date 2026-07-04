from fastapi.testclient import TestClient

from app.main import app


def test_student_profile_returns_capability_dimensions() -> None:
    client = TestClient(app)
    response = client.get("/api/students/student_001/profile")

    assert response.status_code == 200
    payload = response.json()
    assert payload["student_name"] == "林一舟"
    assert len(payload["dimensions"]) == 4


def test_learning_plan_and_recommendations() -> None:
    client = TestClient(app)
    plan_response = client.post("/api/plans/generate", json={"student_id": "student_001", "weeks": 4})
    catalog_response = client.get("/api/competitions")
    competition_response = client.post(
        "/api/competitions/recommend",
        json={"student_id": "student_001", "target": "AI 应用开发"},
    )
    team_response = client.post(
        "/api/teams/recommend",
        json={"student_id": "student_001", "project_goal": "作业代码分析 Demo"},
    )

    assert plan_response.status_code == 200
    assert catalog_response.status_code == 200
    assert competition_response.status_code == 200
    assert team_response.status_code == 200
    assert len(plan_response.json()["tasks"]) == 4
    assert catalog_response.json()["total"] >= 8
    assert catalog_response.json()["competitions"][0]["official_url"]
    assert len(competition_response.json()["recommendations"]) >= 2
    assert len(team_response.json()["candidates"]) >= 2


def test_team_request_and_pool_status() -> None:
    client = TestClient(app)
    request_response = client.post(
        "/api/teams/requests",
        json={
            "student_id": "student_001",
            "competition_name": "中国大学生计算机设计大赛",
            "project_direction": "AI 应用开发与教学智能体",
            "missing_roles": ["前端与交互", "算法与评测"],
            "expected_skills": ["React", "RAG"],
            "weekly_hours": 8,
            "communication": "每周一次线上同步",
            "team_status_enabled": True,
        },
    )
    status_response = client.get("/api/students/student_001/team-status")

    assert request_response.status_code == 200
    assert status_response.status_code == 200
    assert request_response.json()["team_status_enabled"] is True
    assert request_response.json()["contact_visible"] is False
    assert status_response.json()["contact_visible"] is False
