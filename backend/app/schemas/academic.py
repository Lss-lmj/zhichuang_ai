from __future__ import annotations

from pydantic import BaseModel, Field


class CourseSummary(BaseModel):
    course_id: str
    name: str
    term: str
    teacher_name: str
    description: str


class ClassSummary(BaseModel):
    class_id: str
    course_id: str
    name: str
    grade: str
    major: str
    student_count: int


class StudentSummary(BaseModel):
    student_id: str
    name: str
    student_no: str
    class_id: str
    target_path: str
    tags: list[str] = Field(default_factory=list)


class CourseListResponse(BaseModel):
    courses: list[CourseSummary]


class ClassListResponse(BaseModel):
    course_id: str
    classes: list[ClassSummary]


class StudentListResponse(BaseModel):
    class_id: str
    students: list[StudentSummary]
