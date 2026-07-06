from fastapi.testclient import TestClient

from app.main import app


def test_agent_chat_returns_rag_answer_with_citations() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/agent/chat",
        json={
            "message": "如何准备算法竞赛？",
            "scenario": "student",
            "session_id": "session_student_001",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == "session_student_001"
    assert "算法竞赛" in payload["answer"]
    assert payload["is_uncertain"] is False
    assert payload["retrieval_status"] == "matched"
    assert len(payload["citations"]) >= 1
    assert payload["citations"][0]["title"]
    assert payload["citations"][0]["path"]
    assert payload["citations"][0]["updated_at"]


def test_agent_chat_keeps_context_for_three_turns() -> None:
    client = TestClient(app)
    history = []
    questions = [
        "教师怎么看本次代码项目共性问题？",
        "哪些问题适合课堂讲评？",
        "下一次课应该安排什么练习？",
    ]

    response_payload = None
    for question in questions:
        response = client.post(
            "/api/agent/chat",
            json={
                "message": question,
                "scenario": "teacher",
                "session_id": "session_teacher_001",
                "history": history,
            },
        )
        assert response.status_code == 200
        response_payload = response.json()
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": response_payload["answer"]})

    assert response_payload is not None
    assert response_payload["session_id"] == "session_teacher_001"
    assert "教师视角" in response_payload["context_summary"]
    assert response_payload["suggested_next_questions"]


def test_agent_chat_is_uncertain_without_supporting_chunks() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/agent/chat",
        json={
            "message": "火星农业灌溉系统怎么验收？",
            "scenario": "student",
            "session_id": "session_unknown_001",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == "session_unknown_001"
    assert payload["is_uncertain"] is True
    assert payload["retrieval_status"] == "no_match"
    assert "不确定" in payload["answer"]
    assert payload["citations"] == []
