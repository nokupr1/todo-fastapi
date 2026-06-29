from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, index=False)
    is_active = Column(Boolean, index=True)

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, name={self.name}, is_active={self.is_active})>"
