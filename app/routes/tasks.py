from asyncio import tasks

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.services.task_services import TaskService

from ..database import get_db
from ..schemas.task import TaskCreate, TaskListResponse, TaskResponse

tasks_router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@tasks_router.get("", response_model=TaskListResponse, description="Get all tasks", status_code=status.HTTP_200_OK)
def get_all_tasks(db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_all_tasks()

@tasks_router.get("/to-complete", response_model=TaskListResponse, description="Get all uncomplete tasks", status_code=status.HTTP_200_OK)
def get_all_tasks_to_complete(db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_all_tasks_to_complete()

@tasks_router.post("", response_model=TaskResponse, description="Create new task", status_code=status.HTTP_200_OK)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.create_task(task_data)

@tasks_router.delete("/{task_id}", description="Delete existing task", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.delete_task(task_id)

# @tasks_router.put("/{task_id}", description="Change task status", status_code=status.HTTP_200_OK)
# def change_task_status(task_id: int, db: Session = Depends(get_db)):
#     service = TaskService(db)
#     return service.change_task_status()
