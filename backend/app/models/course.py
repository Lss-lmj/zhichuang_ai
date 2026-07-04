from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    term: Mapped[str | None] = mapped_column(String(64))
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ClassGroup(Base):
    __tablename__ = "classes"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    grade: Mapped[str | None] = mapped_column(String(64))
    major: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CourseMembership(Base):
    __tablename__ = "course_memberships"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"), index=True)
    class_id: Mapped[str | None] = mapped_column(ForeignKey("classes.id"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    role_in_course: Mapped[str] = mapped_column(String(32), nullable=False)


class StudentAcademicProfile(Base):
    __tablename__ = "student_academic_profiles"

    student_id: Mapped[str] = mapped_column(ForeignKey("users.id"), primary_key=True)
    class_id: Mapped[str] = mapped_column(ForeignKey("classes.id"), index=True)
    target_path: Mapped[str] = mapped_column(String(200), default="软件项目实践")
    tags_json: Mapped[list[str]] = mapped_column(JSON, default=list)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
