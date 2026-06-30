from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.services.task_services import TaskService

from ..database import get_db
from ..schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate

tasks_router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@tasks_router.get(
    "",
    response_model=TaskListResponse,
    description="Get all tasks",
    status_code=status.HTTP_200_OK,
)
def get_all_tasks(is_done: Optional[bool] = None, db: Session = Depends(get_db)):
    service = TaskService(db)
    if is_done != None:
        return service.get_all_tasks_filtered(is_done)
    return service.get_all_tasks()


@tasks_router.post(
    "",
    response_model=TaskResponse,
    description="Create new task",
    status_code=status.HTTP_201_CREATED,
)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.create_task(task_data)


@tasks_router.delete(
    "/{task_id}",
    response_model=TaskResponse,
    description="Delete existing task",
    status_code=status.HTTP_200_OK,
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    service = TaskService(db)
    deleted_task = service.delete_task(task_id)
    if not deleted_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return deleted_task


@tasks_router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    description="Update task",
    status_code=status.HTTP_200_OK,
)
def change_task_status(
    task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)
):
    service = TaskService(db)
    updated_task = service.update_task(task_id, task_data)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return updated_task
