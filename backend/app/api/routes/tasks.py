from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.tasks import (
    LearningTask,
    ReviewRequest,
    ReviewResponse,
    SaveTaskRequest,
    TaskListResponse,
)
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/students/{student_id}/tasks", response_model=TaskListResponse)
def list_student_tasks(
    student_id: str,
    db: Session = Depends(get_db),
) -> TaskListResponse:
    return TaskService(db).list_tasks(student_id)


@router.post("/tasks", response_model=LearningTask)
def save_task(
    payload: SaveTaskRequest,
    db: Session = Depends(get_db),
) -> LearningTask:
    return TaskService(db).save_task(payload)


@router.post("/reviews/generate", response_model=ReviewResponse)
def generate_review(
    payload: ReviewRequest,
    db: Session = Depends(get_db),
) -> ReviewResponse:
    return TaskService(db).review(payload)
