from fastapi import HTTPException, status

from sqlalchemy.orm import Session

import schemas, models, helpers


def create(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=helpers.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(user_id: int, db: Session):
    user = db.query(models.User).filter(user_id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user
