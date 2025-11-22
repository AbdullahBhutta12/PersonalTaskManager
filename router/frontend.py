from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import database
import schemas
from repository import user

router = APIRouter(
    prefix="/auth",
    tags=["HTML Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/send-code")
def send_code_page(request: Request):
    return templates.TemplateResponse("send_code.html", {"request": request})


@router.get("/verify")
def verify_page(request: Request):
    return templates.TemplateResponse("verify_email.html", {"request": request})


@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/send-code")
def send_code_action(
        request: Request,
        email: str = Form(...),
        db: Session = Depends(database.get_db)
):
    user.send_code(schemas.Emails(email=email), db)

    return RedirectResponse(url="/auth/verify", status_code=303)


@router.post("/verify")
def verify_action(
        request: Request,
        email: str = Form(...),
        code: str = Form(...),
        db: Session = Depends(database.get_db)
):
    data = schemas.VerifyEmail(email=email, code=code)
    result = user.verify_email(data, db)

    if not result["verified"]:
        return templates.TemplateResponse(
            "verify_email.html",
            {"request": request, "error": "Invalid code"}
        )

    return RedirectResponse(url="/auth/signup", status_code=303)


@router.post("/signup")
def signup_action(
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        profile_image: UploadFile = File(...),
        db: Session = Depends(database.get_db),
):
    user.create(username, email, password, profile_image, db)
    return RedirectResponse(url="/auth/send-code", status_code=303)