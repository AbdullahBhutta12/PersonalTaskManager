from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks

import schemas, database, oauth2
from repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post('/sign_up', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def sign_up(username: str = Form(...),
            email: str = Form(...),
            password: str = Form(...),
            profile_image: UploadFile = File(...),
            db: Session = Depends(database.get_db)):
    return user.create(username, email, password, profile_image, db)


@router.post('/save-device-token')
def save_token(data: schemas.TokenIn, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.save_token(data, db, current_user)


@router.post("/verify-email")
def verify_email(data: schemas.VerifyEmail, db: Session = Depends(database.get_db)):
    return user.verify_email(data, db)


@router.post("/send-verification-code")
def send_code(email: schemas.Emails, db: Session = Depends(database.get_db)):
    return user.send_code(email, db)


@router.get('/profile', response_model=schemas.UserResponse)
def get_user(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_user(db, current_user)

@router.post("/reset-password")
def reset_password(
    data: schemas.ResetPassword,
    db: Session = Depends(database.get_db)
):
    return user.reset_password(data, db)