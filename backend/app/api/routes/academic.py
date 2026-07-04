from fastapi import APIRouter

from app.schemas.academic import ClassListResponse, CourseListResponse, StudentListResponse
from app.services.academic_service import AcademicService

router = APIRouter()


@router.get("/courses", response_model=CourseListResponse)
def list_courses() -> CourseListResponse:
    return AcademicService().list_courses()


@router.get("/courses/{course_id}/classes", response_model=ClassListResponse)
def list_classes(course_id: str) -> ClassListResponse:
    return AcademicService().list_classes(course_id)


@router.get("/classes/{class_id}/students", response_model=StudentListResponse)
def list_students(class_id: str) -> StudentListResponse:
    return AcademicService().list_students(class_id)
