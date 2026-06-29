from sqlalchemy.orm import Session

from ..models.task import Task
from ..schemas.task import TaskCreate


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_tasks(self) -> list[Task]:
        return self.db.query(Task).all()

    def get_all_tasks_to_complete(self) -> list[Task]:
        return self.db.query(Task).filter(Task.is_done == False).all()

    def create_task(self, task_data: TaskCreate) -> Task:
        db_task = Task(**task_data.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: int) -> Task:
        db_task = self.db.query(Task).filter(Task.id == task_id).first()
        self.db.delete(db_task)
        self.db.commit()
        return db_task
