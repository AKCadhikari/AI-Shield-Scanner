"""
backend/models/report.py
Written by: Dheeshana
Purpose: Report ORM model - metadata for generated exports.
FR11: Generate and download security reports.
"""

from __future__ import annotations

import enum 
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.models.scan import Scan
    from backend.models.user import User

class ReportFormat(str, enum.Enum):
    PDF = "pdf"
    CSV = "csv"
    JSON = "json"

class Report(Base):
    """Metadata record for a generated report export."""

    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scans.id", ondelete="CASCADE"),
        nullable=False,
    )
    generated_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    format: Mapped[ReportFormat] = mapped_column(
        Enum(ReportFormat, name="report_format"), nullable=False
    )
    file_path: Mapped[str | None] = mapped_column(Text)
    file_size_kb: Mapped[int | None] = mapped_column(Integer)
    summary: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    scan: Mapped["Scan"] = relationship("Scan", back_populates="reports")
    generator: Mapped["User"] = relationship("User", back_populates="reports")

    @property
    def download_filename(self) -> str:
        return f"report_{self.scan_id}_{self.created_at.strftime('%Y%m%d')}.{self.format.value}"
    
    def __repr__(self) -> str:
        return f"<Report id={self.id} format={self.format.value!r}>"

