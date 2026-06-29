from sqlalchemy.orm import Session

from ..database import get_db
from ..models.task import Task
from ..schemas.task import TaskCreate


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_tasks(self) -> list[Task]:
        return self.db.query(Task).all()

    def create(self, task_data: TaskCreate) -> Task:
        db_task = Task(**task_data.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task
