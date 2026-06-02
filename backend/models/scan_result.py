"""
backend/models/scan_result.py
ScanResult ORM model — outcome of one test case within a scan.
FR07: Pass/Fail/Warning classification.
FR09: Risk severity scoring.
"""
from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped , mapped_column, relationship
from sqlalchemy.sql import func

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.models.scan import Scan
    from backend.models.test_case import TestCase
    from backend.models.evidence import Evidence

class ResultVerdict(str, enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    ERROR = "error"

class SeverityLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ScanResult(Base):
    """
    The outcome of running one TestCase against a Target during a Scan.
    Linked to Evidence for the encrypted prompt/response pair.
    """

    __tablename__ = "scan_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scans.id", ondelete="CASCADE"),
        nullable=False,
    )
    test_case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("test_cases.id", ondelete="RESTRICT"),
        nullable=False,
    )

    # Classification
    verdict: Mapped[ResultVerdict] = mapped_column(
        Enum(ResultVerdict, name="result_verdict"), nullable=False
    )
    severity: Mapped[SeverityLevel | None] = mapped_column(
        Enum(SeverityLevel, name="severity_level")
    )
    risk_score: Mapped[float | None] = mapped_column(Numeric(5, 2))

    # AI analysis
    ai_judge_reason: Mapped[str | None] = mapped_column(Text)
    detector_flags: Mapped[list[Any]] = mapped_column(
        JSONB, nullable=False, default=list
    )  # list of detector names that fired

    # Performance
    response_time_ms: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    scan: Mapped["Scan"] = relationship("Scan", back_populates="results")
    test_case: Mapped["TestCase"] = relationship("TestCase", back_populates="results")
    evidence: Mapped["Evidence | None"] = relationship(
        "Evidence",
        back_populates="scan_result",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # ── helpers ──────────────────────────────────────────────
    @property
    def is_vulnerable(self) -> bool:
        return self.verdict == ResultVerdict.FAIL

    def __repr__(self) -> str:
        return (
            f"<ScanResult id={self.id} verdict={self.verdict.value!r} "
            f"severity={self.severity} score={self.risk_score}>"
        )
    