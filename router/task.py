from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas
import models
from database import *
from typing import List
from repository import task

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

@router.get('/', response_model=List[schemas.Task])
def get_all(db: Session = Depends(get_db)):
    return task.get_all(db)

@router.post('/create_task', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Task, db: Session= Depends(get_db)):
    return task.create(request, db)

# @router.put('/update_task')
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

@router.delete('/delete_task', status_code=status.HTTP_204_NO_CONTENT)
def delete(task_id: int, db: Session= Depends(get_db)):
    return task.delete(task_id, db)

# //  POST http://0.0.0.0:8000/tasks/create_task
# body
# {
#   "title": "test",
#   "location": "string"
# }