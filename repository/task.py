from fastapi import HTTPException, status

import schemas
import models
from router.notification import send_notification_others#, send_notification

from sqlalchemy.orm import Session


def get_all(db: Session, current_user: schemas.User):
    tasks = db.query(models.Task).filter(current_user.id == models.Task.user_id).all()
    return tasks


def create(request: schemas.TaskBase, db: Session, current_user: schemas.User):
    new_task = models.Task(title=request.title, description=request.description, location=request.location,
                           completed=False, user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    send_notification_others(
        db=db,
        title="Welcome to Personal Task Manager",
        body=f"Hi! {current_user.username} Your task is successfully added",
        current_user=current_user.id
    )
    return new_task


def update(task_id: int, db: Session, completed: bool):
    tasks = db.query(models.Task).filter(task_id == models.Task.id).first()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    tasks.completed = completed
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

# def create(request: schemas.TaskBase, db: Session, current_user: schemas.User):
#     new_task = models.Task(title=request.title, description=request.description, location=request.location, completed=False, user_id=current_user.id)
#     db.add(new_task)
#     db.commit()
#     db.refresh(new_task)
#     user_device = db.query(models.DeviceToken).filter(current_user.id == models.DeviceToken.user_id).first()#order_by(models.DeviceToken.created_at.desc()).first()
#     print(f"filtered data: {user_device}")
#     if user_device:
#         print(f" device token: {user_device.token}")
#         try:
#             send_notification(
#                 title="Welcome to Personal Task Manager",
#                 body=f"Hi! {current_user.username} Your task is successfully added",
#                 token=user_device.token
#             )
#         except Exception as e:
#             print("Notification Error", e)
#     return new_task
