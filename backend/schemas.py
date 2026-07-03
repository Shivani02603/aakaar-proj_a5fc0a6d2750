"""Pydantic schemas — STAMPED from the build contract. Do not hand-edit;
these mirror database/models.py and frontend/src/types.ts exactly."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: str
