from fastapi.testclient import TestClient

from app.main import app


def test_academic_base_data() -> None:
    client = TestClient(app)
    courses_response = client.get("/api/courses")
    classes_response = client.get("/api/courses/course_web_2026/classes")
    students_response = client.get("/api/classes/class_cs_2024_01/students")

    assert courses_response.status_code == 200
    assert classes_response.status_code == 200
    assert students_response.status_code == 200
    assert len(courses_response.json()["courses"]) >= 2
    assert classes_response.json()["classes"][0]["class_id"] == "class_cs_2024_01"
    assert len(students_response.json()["students"]) >= 5
