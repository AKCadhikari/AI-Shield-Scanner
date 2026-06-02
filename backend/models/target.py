"""
backend/models/target.py
Written by: Dheeshana
Purpose: Target ORM model - chatbot endpoint to be scanned.
FR01: Register and manage target chatbot systems.
"""

from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, LargeBinary, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from.backend.database.base import Base

if TYPE_CHECKING:
    from backend.models.user import User
    from backend.models.scan import Scan

class Target(Base):
    """A registered chatbot endpoint."""

    __tablename__ = "targets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    endpoint_url: Mapped[str] = mapped_column(Text, nullable=False)
    auth_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="none"
    )
    auth_secret: Mapped[bytes | None] = mapped_column(LargeBinary)
    headers: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    timeout_sec: Mapped[int] = mapped_column(
        Integer, nullable=False, default=30
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    owner: Mapped["User"] = relationship("User", back_populates="targets")
    scans: Mapped[list["Scan"]] = relationship(
        "Scan", back_populates="target", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Target id={self.id} name={self.name!r}>"


