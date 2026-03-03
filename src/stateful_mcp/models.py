from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    text: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    text: str