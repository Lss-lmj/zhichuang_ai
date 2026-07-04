from fastapi.testclient import TestClient

from app.main import app


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
