"""
backend/models/scan.py
Written by: Dheeshana
Purpose: Scan ORM model - one full security scan session.
FR02: Configure test profile. FR03: Execute scan lifecycle.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.models.user import User
    from backend.models.target import Target
    from backend.models.scan_result import ScanResult
    from backend.models.report import Report

class ScanStatus(str, enum.Enum)
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ScanProfile(str, enum.Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"
    CUSTOM = "custom"

class Scan(Base):
    """One end-to-end security scan session."""

    __tablename__ = "scans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    target_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("targets.id", ondelete="CASCADE"),
        nullable=False,
    )
    initiated_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    profile: Mapped[ScanProfile] = mapped_column(
        Enum(ScanProfile, name="scan_profile"),
        nullable=False,
        default=ScanProfile.STANDARD,
    )
    custom_config: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    status: Mapped[ScanStatus] = mapped_column(
        Enum(ScanStatus, name="scan_status"),
        nullable=False,
        default=ScanStatus.PENDING,
    )
    celery_task_id: Mapped[str | None] = mapped_column(String(255))
    total_tests: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tests_run: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tests_passed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tests_failed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tests_warned: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    overall_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    target: Mapped["Target"] = relationship("Target", back_populates="scans")
    initiator: Mapped["User"] = relationship("User", back_populates="scans")
    results: Mapped[list["ScanResult"]] = relationship(
        "ScanResult", back_populates="scan", cascade="all, delete-orphan"
    )
    reports: Mapped[list["Report"]] = relationship(
        "Report", back_populates="scan", cascade="all, delete-orphan"
    )

    @property
    def progress_pct(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return round(self.tests_run / self.total_tests * 100,1)
    
    def __repr__(self) -> str:
        return f"<Scan id={self.id} status={self.status.value!r}>"
