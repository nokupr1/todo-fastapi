from sqlalchemy.orm import Session

from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse


class TaskService:
    def __init__(self, db: Session):
        self.task_repository = TaskRepository(db)

    def get_all_tasks(self) -> TaskListResponse:
        tasks = self.task_repository.get_all_tasks()
        tasks_response = [TaskResponse.model_validate(task) for task in tasks]
        return TaskListResponse(tasks=tasks_response)

    def get_all_tasks_to_complete(self) -> TaskListResponse:
        tasks = self.task_repository.get_all_tasks_to_complete()
        tasks_response = [TaskResponse.model_validate(task) for task in tasks]
        return TaskListResponse(tasks=tasks_response)

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        db_task = self.task_repository.create_task(task_data)
        return TaskResponse.model_validate(db_task)

    def delete_task(self, task_id: int) -> TaskResponse:
        db_task = self.task_repository.delete_task(task_id)
        return TaskResponse.model_validate(db_task)

    # def change_task_status(self, task_id: int) -> TaskResponse:
    #     db_task = self.task_repository.change_task_status(task_id)
    #     return TaskResponse.model_validate(db_task)

    class Config:
        from_attributes = True
