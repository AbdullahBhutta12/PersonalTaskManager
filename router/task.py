from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
import database
from typing import List
from repository import task

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

@router.get('/', response_model=List[schemas.Task])
def get_all(db: Session = Depends(database.get_db)):
    return task.get_all(db)

@router.post('/create_task', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Task, db: Session= Depends(database.get_db)):
    return task.create(request, db)

@router.put('/update_task/{task_id}')
def updated(task_id: int, completed: bool, db: Session= Depends(database.get_db)):
    return task.updated(task_id, db, completed)

@router.delete('/delete_task/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(task_id: int, db: Session= Depends(database.get_db)):
    return task.delete(task_id, db)

# //  POST http://0.0.0.0:8000/tasks/create_task
# body
# {
#   "title": "test",
#   "location": "string"
# }