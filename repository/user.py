from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
import uuid, os, shutil, random
from datetime import datetime, timedelta

import models, helpers, schemas
from repository import device_token

IMAGEDIR = "/home/abdullah-saeed/PycharmProjects/Database_Images/"
BASE_URL = "http://192.168.0.181:8000/images/"


def create(username: str, email: str, password: str, profile_image: UploadFile, db: Session):
    os.makedirs(IMAGEDIR, exist_ok=True)
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(IMAGEDIR, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(profile_image.file, buffer)
    image_url = BASE_URL + filename

    existing_user = db.query(models.Emails.is_verified).filter(email == models.Emails.email).first()

    if existing_user:
        new_user = models.User(
            username=username,
            email=email,
            password=helpers.bcrypt(password),
            profile_image=image_url,
            is_verified=existing_user.is_verified
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    else:
        raise HTTPException(status_code=400, detail="This email is not verified!")

    return new_user


def save_token(data: schemas.TokenIn, db: Session, current_user: schemas.User):
    if not data.token:
        raise HTTPException(status_code=400, detail="Token required")
    device_token.save_token(db, current_user.id, data.token)
    return {"result": "Token saved"}


def verify_email(data: schemas.VerifyEmail, db: Session):
    user = db.query(models.Emails).filter(data.email == models.Emails.email).order_by(
        models.Emails.expiration_time.desc()).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    if datetime.now() > user.expiration_time:
        del user
        raise HTTPException(status_code=400, detail="Verification code expired.")

    if user.verification_code != data.verification_code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    user.is_verified = True
    user.verification_code = None
    db.commit()
    return {"message": "Email verified successfully!"}


def send_code(data: schemas.Emails, db: Session):
    verification_code = str(random.randint(100000, 999999))
    expiration_time = datetime.now() + timedelta(minutes=2)
    new_code = models.Emails(email=data.email, verification_code=verification_code, expiration_time=expiration_time)
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    helpers.send_verification_email(data.email, verification_code)
    return f"A verification code is sent to your email {data.email}"

# def create(username: str, email: str, password: str, profile_image: UploadFile, db: Session):
#     os.makedirs(IMAGEDIR, exist_ok=True)
#     filename = f"{uuid.uuid4()}.jpg"
#     filepath = os.path.join(IMAGEDIR, filename)
#     with open(filepath, "wb") as buffer:
#         shutil.copyfileobj(profile_image.file, buffer)
#     image_url = BASE_URL + filename
#
#     new_user = models.User(username=username, email=email, password=helpers.bcrypt(password), profile_image=image_url)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#
#     return new_user
