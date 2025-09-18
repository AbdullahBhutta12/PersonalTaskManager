from fastapi import APIRouter, Depends, status
from typing import List

import schemas, oauth2
import database
from repository import task

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)


@router.get('/', response_model=List[schemas.Task])
def get_all(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.get_all(db)


@router.post('/create_task', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Task, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.create(request, db)


@router.put('/update_task/{task_id}')
def update(task_id: int, completed: bool, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.update(task_id, db, completed)


@router.delete('/delete_task/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(task_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.delete(task_id, db)

# //  POST http://0.0.0.0:8000/tasks/create_task
# body
# {
#   "title": "test",
#   "location": "string"
# }
