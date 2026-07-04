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
    competition_response = client.post(
        "/api/competitions/recommend",
        json={"student_id": "student_001", "target": "AI 应用开发"},
    )
    team_response = client.post(
        "/api/teams/recommend",
        json={"student_id": "student_001", "project_goal": "作业代码分析 Demo"},
    )

    assert plan_response.status_code == 200
    assert competition_response.status_code == 200
    assert team_response.status_code == 200
    assert len(plan_response.json()["tasks"]) == 4
    assert len(competition_response.json()["recommendations"]) >= 2
    assert len(team_response.json()["candidates"]) >= 2
