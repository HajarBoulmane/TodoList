from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.task import Task
from ..database import get_db
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    completed: bool = False


router = APIRouter()

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(title=task.title, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": "Task deleted"}
    return {"message": "Task not found"}

@router.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.title = updated_task.title
        task.completed = updated_task.completed
        db.commit()
        db.refresh(task)
        return task
    return {"message": "Task not found"}