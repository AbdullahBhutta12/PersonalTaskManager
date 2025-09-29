from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
import uuid, os, shutil
import models, helpers ,schemas

IMAGEDIR = "/home/abdullah-saeed/PycharmProjects/Database_Images/"


# def create(request: schemas.UserBase, db: Session):
#     new_user = models.User(username=request.username, email=request.email, password=helpers.bcrypt(request.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


async def create(username: str, email: str, password: str, profile_image: UploadFile, db: Session):

    os.makedirs(IMAGEDIR, exist_ok=True)
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(IMAGEDIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(profile_image.file, buffer)


    new_user = models.User(username=username, email=email, password=helpers.bcrypt(password), profile_image=filepath)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(user_id: int, db: Session):
    user = db.query(models.User).filter(user_id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user


def users(db: Session):
    user = db.query(models.User).all()
    return user
