from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, JSON, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EvaluationCaseRecord(Base):
    __tablename__ = "evaluation_cases"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    scenario: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    input_question: Mapped[str] = mapped_column(Text, nullable=False)
    expected_focus_json: Mapped[list[str]] = mapped_column(JSON, default=list)
    priority: Mapped[str] = mapped_column(String(32), default="P1", index=True)
    status: Mapped[str] = mapped_column(String(32), default="已记录", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class EvaluationRecordItem(Base):
    __tablename__ = "evaluation_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    scenario: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    input_question: Mapped[str] = mapped_column(Text, nullable=False)
    system_output: Mapped[str] = mapped_column(Text, nullable=False)
    citations_json: Mapped[list[dict]] = mapped_column(JSON, default=list)
    manual_score: Mapped[int] = mapped_column(Integer, nullable=False)
    issue_notes: Mapped[str] = mapped_column(Text, default="")
    reviewer: Mapped[str] = mapped_column(String(100), default="项目评测组")
    evaluated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
