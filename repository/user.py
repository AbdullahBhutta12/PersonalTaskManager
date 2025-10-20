from fastapi import UploadFile
from sqlalchemy.orm import Session
import uuid, os, shutil
import models, helpers

IMAGEDIR = "/home/abdullah-saeed/PycharmProjects/Database_Images/"
BASE_URL = "http://192.168.0.181:8000/images/"


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

    return new_user
