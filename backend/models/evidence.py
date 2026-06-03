"""
backend/models/evidence.py
Written by: Dheeshana
Purpose: Encrypted storage of test prompt and chatbot response.
FR10: All evidence must be stored encrypted at rest (AES-256).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.models.scan_result import ScanResult

class Evidence(Base):
    """
    Encrypted record of the exact prompt sent to a chatbot
    and the response received, linked to one ScanResult.
    Encryption scheme: AES-256-GCM with unique IV per row.
    """

    __tablename__ = "evidence"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_result_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scan_results.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # Encrypted blobs
    prompt_enc: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    response_enc: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    iv: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    # Integrity
    hash_sha256: Mapped[str] = mapped_column(String(64), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationship
    scan_result: Mapped["ScanResult"] = relationship(
        "ScanResult", back_populates="evidence"
    )

    def __repr__(self) -> str:
        return (
            f"<Evidence id={self.id}"
            f"scan_result_id={self.scan_result_id} "
            f"hash={self.hash_sha256[:8]}...>"
        )