from fastapi.testclient import TestClient

from app.main import app


def test_knowledge_documents_and_search() -> None:
    client = TestClient(app)
    documents_response = client.get("/api/knowledge/documents")
    search_response = client.get("/api/knowledge/search", params={"q": "作业 Rubric"})

    assert documents_response.status_code == 200
    assert search_response.status_code == 200
    assert documents_response.json()["total"] >= 5
    assert search_response.json()["total"] >= 1
    assert search_response.json()["results"][0]["title"]
