from typing import Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Task name")
    description: Optional[str] = Field(
        None, max_length=150, description="Task description"
    )
    is_done: bool = Field(..., description="Task completion status")


class TaskCreate(TaskBase):
    pass


class TaskResponse(BaseModel):
    id: int = Field(..., gt=0, description="Task unique identifier")
    name: str
    description: str
    is_done: bool

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
