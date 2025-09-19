from fastapi import HTTPException, status

import schemas
import models

from sqlalchemy.orm import Session



def get_all(db: Session):
    tasks = db.query(models.Task).all()
    return tasks

def create(request: schemas.Task, db: Session, current_user: schemas.User):
    new_task = models.Task(title=request.title, description=request.description, location=request.location, completed=False, user_id=current_user)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update(task_id: int, db: Session, completed: bool):
    tasks = db.query(models.Task).filter(task_id == models.Task.id).first()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    tasks.completed= completed
    db.commit()
    db.refresh(tasks)
    return "Task update"

def delete(task_id: int, db: Session):
    deleted = db.query(models.Task).filter(task_id == models.Task.id)
    if not deleted.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    deleted.delete(synchronize_session=False)
    db.commit()
    return "Deleted"