from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_tasks(self) -> list[Task]:
        return self.db.query(Task).all()

    def get_all_tasks_filtered(self, is_done: bool) -> list[Task]:
        return self.db.query(Task).filter(Task.is_done == is_done).all()

    def create_task(self, task_data: TaskCreate) -> Task:
        db_task = Task(**task_data.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: int) -> Task:
        db_task = self.db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found",
            )
        self.db.delete(db_task)
        self.db.commit()
        return db_task

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Task:

        db_task = self.db.query(Task).filter(Task.id == task_id).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found",
            )

        update_data = task_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_task, key, value)

        self.db.commit()
        self.db.refresh(db_task)

        return db_task
