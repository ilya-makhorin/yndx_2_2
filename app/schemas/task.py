from pydantic import BaseModel, Field
from enum import StrEnum


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100, examples=["Изучить FastApi"])
    description:  str | None = Field(
        default=None,
        max_length=100
    )
    priority: int = Field(default=1, ge=1, le=5)


class TaskUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: int
    status: TaskStatus


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
