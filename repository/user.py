from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
import uuid, os, shutil
import models, helpers, schemas
from router.notification import send_notification

IMAGEDIR = "/home/abdullah-saeed/PycharmProjects/Database_Images/"
BASE_URL = "http://0.0.0.0:8000/images/"

def create(username: str, email: str, password: str, profile_image: UploadFile, db: Session):
    os.makedirs(IMAGEDIR, exist_ok=True)
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(IMAGEDIR, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(profile_image.file, buffer)
    image_url = BASE_URL + filename

    new_user = models.User(username=username, email=email, password=helpers.bcrypt(password), profile_image=image_url)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # device_token = ""
    #
    # send_notification(
    #     title="Welcome to Personal Task Manager",
    #     body=f"Hi! {username} Your account is successfully created",
    #     token=device_token
    # )

    return {"Username":new_user.username, "Email": new_user.email, "Image url": image_url}


# def get_user(db: Session, current_user: schemas.User):
#     user = db.query(models.User).filter(current_user.id == models.User.id).first()
#     return user
#
#
# def users(db: Session):
#     user = db.query(models.User).all()
#     return user
