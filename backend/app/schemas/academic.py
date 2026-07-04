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


class AcademicImportCourse(BaseModel):
    course_id: str
    name: str
    term: str = ""
    teacher_id: str = "teacher_001"
    teacher_name: str = "周老师"
    teacher_no: str | None = None
    description: str = ""


class AcademicImportClass(BaseModel):
    class_id: str
    course_id: str
    name: str
    grade: str = ""
    major: str = ""


class AcademicImportStudent(BaseModel):
    student_id: str
    name: str
    student_no: str
    class_id: str
    course_ids: list[str] = Field(default_factory=list)
    target_path: str = "软件项目实践"
    tags: list[str] = Field(default_factory=list)


class AcademicImportRequest(BaseModel):
    courses: list[AcademicImportCourse] = Field(default_factory=list)
    classes: list[AcademicImportClass] = Field(default_factory=list)
    students: list[AcademicImportStudent] = Field(default_factory=list)


class AcademicImportResponse(BaseModel):
    imported_courses: int
    imported_classes: int
    imported_students: int
    imported_memberships: int
    message: str
