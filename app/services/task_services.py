from sqlalchemy.orm import Session

from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskListResponse, TaskResponse


class TaskService:
    def __init__(self, db: Session):
        self.task_repository = TaskRepository(db)

    def get_all_tasks(self) -> TaskListResponse:
        tasks = self.task_repository.get_all_tasks()
        tasks_response = [TaskResponse.model_validate(task) for task in tasks]
        return TaskListResponse(tasks=tasks_response)
