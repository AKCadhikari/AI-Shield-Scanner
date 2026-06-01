"""
backend/models/user.py
Written by: Dheeshana
Purpose: User, Role and RefreshToken ORM models.
NFR09: Supports RBAC - every user carries a role.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.models.target import Target
    from backend.models.scan import Scan
    from backend.models.report import Report

class Role(Base):
    """Lookup table for user roles."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text)

    users: Mapped[list["User"]] = relationship(
        "User", back_populates="role"
    )

    def __repr__(self) -> str:
        return f"<Role id={self.id} name={self.name!r}>"
 
class User(Base):
    """Application user account."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    role: Mapped["Role"] = relationship("Role", back_populates="users")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )
    targets: Mapped[list["Target"]] = relationship(
        "Target", back_populates="owner"
    )
    scans: Mapped[list["Scan"]] = relationship(
        "Scan", back_populates="initiator"
    )
    reports: Mapped[list["Report"]] = relationship(
        "Report", back_populates="generator"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
    
class RefreshToken(Base):
   """Stored refresh token for JWT rotation."""

   __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    token_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="refresh_tokens"
    )

    @property
    def is_valid(self) -> bool:
        from datetime import timezone
        return not self.revoked and self.expires_at > datetime.now(tz=timezone.utc)

    def __repr__(self) -> str:
        return f"<RefreshToken id={self.id} revoked={self.revoked}>"