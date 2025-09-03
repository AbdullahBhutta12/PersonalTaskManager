from fastapi import Depends
from sqlalchemy.orm import Session
import schemas
from fastapi import HTTPException, status
import models
from database import *



def get_all(db: Session):
    tasks = db.query(models.Task).all()
    return tasks

def create(request: schemas.Task, db: Session):
    new_task = models.Task(title=request.title, location=request.location)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# def update(task_id: int, request: schemas.UpdateTask, db: Session= Depends(get_db)):
#     updated = db.query(models.Task).filter(task_id == models.Task.id)
#     if not updated.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
#     updated.update(
#         {
#             "title": request.title,
#             "location": request.location,
#             "completed": request.completed
#         }
#     )
#     db.commit()
#     return "Task update"

def delete(task_id: int, db: Session):
    deleted = db.query(models.Task).filter(task_id == models.Task.id)
    if not deleted.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    deleted.delete(synchronize_session=False)
    db.commit()
    return "Deleted"