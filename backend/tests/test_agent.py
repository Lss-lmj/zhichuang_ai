from fastapi.testclient import TestClient

from app.main import app


def test_agent_chat_returns_rag_answer_with_citations() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/agent/chat",
        json={"message": "如何准备算法竞赛？", "scenario": "student"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "算法竞赛" in payload["answer"]
    assert len(payload["citations"]) >= 1
    assert payload["citations"][0]["title"]
