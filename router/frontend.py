from fastapi import APIRouter, Request, Form, Depends, UploadFile, File, Response, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import requests
import database
import schemas
from repository import user

router = APIRouter(prefix="/auth", tags=["HTML Pages"])
templates = Jinja2Templates(directory="templates")

# Apis for sign-up and log-in

@router.get("/send-code")
def send_code_page(request: Request):
    return templates.TemplateResponse("send_code.html", {"request": request})


@router.post("/send-code-html")
async def send_code_html(
        request: Request,
        email: str = Form(...),
        db=Depends(database.get_db)
):

    data = schemas.Emails(email=email)
    user.send_code(data, db)

    return templates.TemplateResponse(
        "verify_email.html",
        {"request": request, "email": email}
    )

# @router.get("/verify")
# def verify_email_page(request: Request, email: str = None):
#     return templates.TemplateResponse(
#         "verify_email.html",
#         {"request": request, "email": email, "error": None}
#     )
@router.get("/verify")
def verify_email_page(request: Request, email: str = ""):
    return templates.TemplateResponse("verify_email.html", {"request": request, "email": email})

@router.post("/verify")
def verify_email_html(
        request: Request,
        email: str = Form(...),
        verification_code: str = Form(...),
        db=Depends(database.get_db)
):
    data = schemas.VerifyEmail(email=email, verification_code=verification_code)

    try:
        user.verify_email(data, db)
        return RedirectResponse(url="/auth/signup", status_code=303)

    except HTTPException as e:
        return templates.TemplateResponse(
            "verify_email.html",
            {
                "request": request,
                "email": email,
                "error": e.detail
            }
        )

#
#
# @router.post("/verify")
# def verify_email_html(
#         request: Request,
#         email: str = Form(...),
#         otp: str = Form(...),
#         db=Depends(database.get_db)
# ):
#     data = schemas.VerifyEmail(email=email, verification_code=otp)
#     user.verify_email(data, db)
#
#     return RedirectResponse(url="/auth/signup", status_code=303)


# @router.get("/signup")
# def signup_page(request: Request):
#     return templates.TemplateResponse("signup.html", {"request": request})
@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse(
        "signup.html",
        {"request": request, "error": None}
    )


@router.post("/signup")
def signup_action(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    profile_image: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    try:
        user.create(
            username=username,
            email=email,
            password=password,
            profile_image=profile_image,
            db=db
        )

        return RedirectResponse(url="/auth/login", status_code=303)

    except HTTPException as e:
        # SAME signup page par error
        return templates.TemplateResponse(
            "signup.html",
            {
                "request": request,
                "error": e.detail
            }
        )



@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_action(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):

    payload = {
        "username": email,     # IMPORTANT
        "password": password
    }

    response = requests.post(
        "http://0.0.0.0:8000/login",
        data=payload
    )

    if response.status_code != 200:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid email or password"},
            status_code=400
        )

    token = response.json().get("access_token")

    redirect = RedirectResponse("/auth/dashboard", status_code=303)
    redirect.set_cookie(key="access_token", value=token)

    return redirect


# Apis for home, profile and logout pages




@router.get("/home")
def home_page(request: Request):
    if "access_token" not in request.cookies:   # <- copy this
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/dashboard")
def dashboard(request: Request):
    if "access_token" not in request.cookies:   # <- copy this
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get('/profile')
def profile_page(request: Request):
    if "access_token" not in request.cookies:   # <- copy this
        return RedirectResponse(url="/auth/login")
    token = request.cookies.get("access_token")
    response = requests.get(
        "http://0.0.0.0:8000/user/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    profile = response.json()
    return templates.TemplateResponse("profile.html", {"request": request, "profile": profile})


@router.get("/logout")
def logout(request: Request):
    request.session.clear()

    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie("access_token")

    return response

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
    if not token:
        return RedirectResponse("/auth/login", status_code=303)

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
    if not token:
        return RedirectResponse("/auth/login", status_code=303)

    requests.put(
        f"http://0.0.0.0:8000/tasks/update_task/{task_id}?completed=true",
        headers={"Authorization": f"Bearer {token}"}
    )

    return RedirectResponse("/auth/tasks", status_code=303)


@router.get("/delete/{task_id}")
def delete_task(task_id: int, request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login", status_code=303)

    requests.delete(
        f"http://0.0.0.0:8000/tasks/delete_task/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    return RedirectResponse("/auth/tasks", status_code=303)



# APIS for Events



@router.get("/events")
def events_page(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login", status_code=303)

    response = requests.get(
        "http://0.0.0.0:8000/events/",
        headers={"Authorization": f"Bearer {token}"}
    )

    events = response.json() if response.status_code == 200 else []

    return templates.TemplateResponse("events.html", {"request": request, "events": events})


@router.get("/add-event")
def add_event_page(request: Request):
    return templates.TemplateResponse("add_event.html", {"request": request})


@router.post("/add-event")
def add_event(
    request: Request,
    event_name: str = Form(...),
    location: str = Form(...),
    event_date: str = Form(...),
    event_time: str = Form(...)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login", status_code=303)

    payload = {
        "event_name": event_name,
        "location": location,
        "event_date": event_date,
        "event_time": event_time
    }

    requests.post(
        "http://0.0.0.0:8000/events/create_event",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    return RedirectResponse("/auth/events", status_code=303)


@router.get("/edit-event/{event_id}")
def edit_event_page(event_id: int, request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login", status_code=303)

    response = requests.get(
        "http://0.0.0.0:8000/events/",
        headers={"Authorization": f"Bearer {token}"}
    )

    events = response.json()

    event = next((ev for ev in events if ev["id"] == event_id), None)

    return templates.TemplateResponse("edit_event.html", {"request": request, "event": event})


@router.post("/edit-event/{event_id}")
def edit_event(
    event_id: int,
    request: Request,
    event_name: str = Form(...),
    location: str = Form(...),
    event_date: str = Form(...),
    event_time: str = Form(...)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login", status_code=303)

    payload = {
        "event_name": event_name,
        "location": location,
        "event_date": event_date,
        "event_time": event_time
    }

    requests.put(
        f"http://0.0.0.0:8000/events/update_event/{event_id}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    return RedirectResponse("/auth/events", status_code=303)


@router.get("/delete-event/{event_id}")
def delete_event(event_id: int, request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login", status_code=303)

    requests.delete(
        f"http://0.0.0.0:8000/events/delete_event/{event_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    return RedirectResponse("/auth/events", status_code=303)