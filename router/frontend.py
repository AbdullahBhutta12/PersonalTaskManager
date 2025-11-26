from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import requests
import database
import schemas
from repository import user
from router import authentication

router = APIRouter(prefix="/auth", tags=["HTML Pages"])
templates = Jinja2Templates(directory="templates")

# Apis for sign-up and log-in


@router.get("/send-code")
def send_code_page(request: Request):
    return templates.TemplateResponse("send_code.html", {"request": request})


@router.post("/send-code-html")
def send_code_html(
        email: str = Form(...),
        db=Depends(database.get_db)
):
    data = schemas.Emails(email=email)
    user.send_code(data, db)

    return RedirectResponse(url="/auth/verify", status_code=303)


@router.get("/verify")
def verify_email_page(request: Request):
    return templates.TemplateResponse("verify_email.html", {"request": request})


@router.post("/verify")
def verify_email_html(
        email: str = Form(...),
        verification_code: str = Form(...),
        db=Depends(database.get_db)
):
    data = schemas.VerifyEmail(email=email, verification_code=verification_code)
    user.verify_email(data, db)

    return RedirectResponse(url="/auth/signup", status_code=303)


@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup")
def signup_action(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    profile_image: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    user.create(
        username=username,
        email=email,
        password=password,
        profile_image=profile_image,
        db=db
    )

    return RedirectResponse(url="/auth/login", status_code=303)



@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_action(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):

    token = authentication.login(
        request={"email": email, "password": password},
        db=db
    )

    return RedirectResponse("/auth/home", status_code=303)


# Apis for home, profile and logout pages




@router.get("/home")
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/profile")
def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@router.get("/logout")
def logout_page(request: Request):
    return templates.TemplateResponse("logout.html", {"request": request})



# Apis for tasks


@router.get("/tasks")
def tasks_page(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return RedirectResponse("/auth/login", status_code=303)

    response = requests.get(
        "http://0.0.0.0:8000/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    tasks = response.json() if response.status_code == 200 else []

    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})


@router.get("/add-task")
def add_task_page(request: Request):
    return templates.TemplateResponse("add_task.html", {"request": request})


@router.post("/add-task")
def add_task(request: Request, title: str = Form(...), description: str = Form(...), location: str = Form(...)):
    token = request.cookies.get("access_token")

    payload = {
        "title": title,
        "description": description,
        "location": location
    }

    requests.post(
        f"http://0.0.0.0:8000/tasks/create_task",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    return RedirectResponse("/auth/tasks", status_code=303)


@router.get("/mark/{task_id}")
def mark_done(task_id: int, request: Request):
    token = request.cookies.get("access_token")

    requests.put(
        f"http://0.0.0.0:8000/tasks/update_task/{task_id}?completed=true",
        headers={"Authorization": f"Bearer {token}"}
    )

    return RedirectResponse("/auth/tasks", status_code=303)


@router.get("/delete/{task_id}")
def delete_task(task_id: int, request: Request):
    token = request.cookies.get("access_token")

    requests.delete(
        f"http://0.0.0.0:8000/tasks/delete_task/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    return RedirectResponse("/auth/tasks", status_code=303)
