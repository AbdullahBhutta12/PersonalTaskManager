from http.client import HTTPException

from fastapi import APIRouter, Depends, status, File, UploadFile, Form

import schemas, database, oauth2
from repository import user
from repository import device_token

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post('/sign_up', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def sign_up(username: str = Form(...),
            email: str = Form(...),
            password: str = Form(...),
            profile_image: UploadFile = File(...),
            device_token: str = Form(None),
            db: Session = Depends(database.get_db)):
    return user.create(username, email, password, profile_image, db, device_token)

# @router.post('/save-device-token')
# def save_token(data: schemas.TokenIn, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     if not data.token:
#         raise HTTPException(status_code=400, detail="Token required")
#     device_token.save_token(db, current_user.id, data.token, platform=data.platform)
#     return {"result": "Token saved"}