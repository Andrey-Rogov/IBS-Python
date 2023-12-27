from pydantic import BaseModel
from sqlalchemy import String, Integer, Column, Boolean
from sqlalchemy.orm import DeclarativeBase

HOST = 'localhost'
PORT = '5432'
USER = 'postgres'
PASSWORD = '12345'
DATABASE = 'IBS'


class InTask(BaseModel):
    task: str
    status: bool


class OutTask(BaseModel):
    task_id: int
    task: str
    status: bool


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = "todo"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, nullable=False)
    status = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"TODO(task_id={self.task_id!r}, task={self.task!r}, status={self.status!r})"
