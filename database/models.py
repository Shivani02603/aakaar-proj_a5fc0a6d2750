"""Data models. The User model is scaffold-owned (auth depends on it).

Domain entity models are STAMPED below the marker by Aakaar's type stamper from the build
contract — do not hand-edit stamped sections; they must stay in sync with backend/schemas.py
and frontend/src/types.ts, which are stamped from the same source.
"""
import uuid

from sqlalchemy import Boolean, Text, ForeignKey, Column, String, TIMESTAMP, func

from database.config import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


# ── AAKAAR:STAMPED_MODELS (do not remove this marker) ─────────────────────────────


class Todo(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, default=_uuid)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(TIMESTAMP, nullable=True, server_default=func.now())
    completed = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
