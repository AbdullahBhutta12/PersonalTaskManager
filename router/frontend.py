from fastapi import APIRouter, Request, Form, Depends, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
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
        "username": email,  # IMPORTANT
        "password": password
    }

    response = requests.post(
        "http://localhost:8000/login",
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


# Forgot password
@router.get("/forgot-password")
def forgot_password_page(request: Request):
    return templates.TemplateResponse(
        "forgot_password.html",
        {"request": request}
    )


@router.post("/forgot-password")
def forgot_password_action(
        request: Request,
        email: str = Form(...)
):
    try:
        r = requests.post(
            "http://localhost:8000/user/send-verification-code",
            json={"email": email},
            timeout=5
        )
    except Exception:
        return templates.TemplateResponse(
            "forgot_password.html",
            {
                "request": request,
                "error": "Server error. Please try again."
            }
        )

    if r.status_code != 200:
        return templates.TemplateResponse(
            "forgot_password.html",
            {
                "request": request,
                "error": r.json().get("detail", "OTP not sent")
            }
        )

    # save email in session
    request.session["reset_email"] = email
    return RedirectResponse("/auth/verify-reset-otp", status_code=303)


# Verify OTP
@router.get("/verify-reset-otp")
def verify_reset_otp_page(request: Request):
    email = request.session.get("reset_email")

    if not email:
        return RedirectResponse("/auth/forgot-password", status_code=303)

    return templates.TemplateResponse(
        "verify_reset_otp.html",
        {
            "request": request,
            "email": email
        }
    )


@router.post("/verify-reset-otp")
def verify_reset_otp_action(
        request: Request,
        otp: str = Form(...)
):
    email = request.session.get("reset_email")

    if not email:
        return RedirectResponse("/auth/forgot-password", status_code=303)

    try:
        r = requests.post(
            "http://localhost:8000/user/verify-email",
            json={
                "email": email,
                "verification_code": otp
            },
            timeout=5
        )
    except Exception:
        return templates.TemplateResponse(
            "verify_reset_otp.html",
            {
                "request": request,
                "email": email,
                "error": "Server error. Try again."
            }
        )

    if r.status_code != 200:
        return templates.TemplateResponse(
            "verify_reset_otp.html",
            {
                "request": request,
                "email": email,
                "error": r.json().get("detail", "Invalid OTP")
            }
        )

    # OTP verified
    request.session["reset_verified"] = True
    return RedirectResponse("/auth/reset-password", status_code=303)


# Reset password
@router.get("/reset-password")
def reset_password_page(request: Request):
    if not request.session.get("reset_verified"):
        return RedirectResponse("/auth/forgot-password", status_code=303)

    return templates.TemplateResponse(
        "reset_password.html",
        {"request": request}
    )


@router.post("/reset-password")
def reset_password_action(
        request: Request,
        new_password: str = Form(...)
):
    email = request.session.get("reset_email")

    if not email:
        return RedirectResponse("/auth/forgot-password", status_code=303)

    try:
        r = requests.post(
            "http://localhost:8000/user/reset-password",
            json={
                "email": email,
                "new_password": new_password
            },
            timeout=5
        )
    except Exception:
        return templates.TemplateResponse(
            "reset_password.html",
            {
                "request": request,
                "error": "Server error. Try again."
            }
        )

    if r.status_code != 200:
        return templates.TemplateResponse(
            "reset_password.html",
            {
                "request": request,
                "error": r.json().get("detail", "Password reset failed")
            }
        )

    # cleanup session
    request.session.pop("reset_email", None)
    request.session.pop("reset_verified", None)

    return RedirectResponse("/auth/login", status_code=303)


# Apis for home, profile and logout pages


@router.get("/home")
def home_page(request: Request):
    if "access_token" not in request.cookies:  # <- copy this
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/dashboard")
def dashboard(request: Request):
    if "access_token" not in request.cookies:  # <- copy this
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get('/profile')
def profile_page(request: Request):
    if "access_token" not in request.cookies:  # <- copy this
        return RedirectResponse(url="/auth/login")
    token = request.cookies.get("access_token")
    response = requests.get(
        "http://localhost:8000/user/profile",
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
        "http://localhost:8000/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    tasks = response.json() if response.status_code == 200 else []

    pending_tasks = [t for t in tasks if not t["completed"]]
    completed_tasks = [t for t in tasks if t["completed"]]

    return templates.TemplateResponse(
        "tasks.html",
        {
            "request": request,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks
        }
    )


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
        f"http://localhost:8000/tasks/create_task",
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
        f"http://localhost:8000/tasks/update_task/{task_id}?completed=true",
        headers={"Authorization": f"Bearer {token}"}
    )

    return RedirectResponse("/auth/tasks", status_code=303)


@router.get("/delete/{task_id}")
def delete_task(task_id: int, request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login", status_code=303)

    requests.delete(
        f"http://localhost:8000/tasks/delete_task/{task_id}",
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
        "http://localhost:8000/events/",
        headers={"Authorization": f"Bearer {token}"}
    )

    events = response.json() if response.status_code == 200 else []

    today = datetime.today().date()

    upcoming_events = []
    past_events = []

    for event in events:
        try:
            event_date = datetime.strptime(event["event_date"], "%Y-%m-%d").date()
        except:
            continue

        if event_date >= today:
            upcoming_events.append(event)
        else:
            past_events.append(event)

    return templates.TemplateResponse(
        "events.html",
        {
            "request": request,
            "upcoming_events": upcoming_events,
            "past_events": past_events
        }
    )


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
        "http://localhost:8000/events/create_event",
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
        "http://localhost:8000/events/",
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
        f"http://localhost:8000/events/update_event/{event_id}",
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
        f"http://localhost:8000/events/delete_event/{event_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    return RedirectResponse("/auth/events", status_code=303)
