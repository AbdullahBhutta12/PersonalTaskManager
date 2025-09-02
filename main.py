from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import *

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.get('/tasks')
def get_all(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

@app.post('/tasks')
def create(request: schemas.Task, db: Session= Depends(get_db)):
    new_task = models.Task(title=request.title, location=request.location)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put('/tasks/{id}')
def update(task_id: int, request: schemas.Task, db: Session= Depends(get_db)):
    updated = db.query(models.Task).filter(task_id == models.Task.id)
    if not updated.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    updated.update(
        {
            "title": request.title,
            "location": request.location
        }
    )
    db.commit()
    return "Task update"

@app.delete('/tasks/{id}')
def delete(task_id: int, db: Session= Depends(get_db)):
    deleted = db.query(models.Task).filter(task_id == models.Task.id)
    if not deleted.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    deleted.delete(synchronize_session=False)
    db.commit()
    return "Deleted"

# @app.get('/tasks/{id}')
# def get_one(task_id: int, db: Session= Depends(get_db)):
#     task = db.query(models.Task).filter(task_id == models.Task.id).first()
#     return task