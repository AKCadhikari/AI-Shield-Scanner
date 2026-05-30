"""
backend/database/base.py
SQLAlchemy declarative base shared by all ORM models.
NFR15: Single base class to alembic can auto-detect all tables.
"""
from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    """
    Project-wide SQLAlchemy base.

    All ORM models must inherit from this class so Alembic
    can discover them via `target_metadata = Base.metadata`.
    """
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Derive table name from class name"""
        import re
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        return name + "s")