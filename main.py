from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
import os
import models
import database
from router import task, event, user, authentication, frontend

models.Base.metadata.create_all(bind=database.engine)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

os.makedirs(IMAGES_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="supersecret123")

app.mount(
    "/images",
    StaticFiles(directory=IMAGES_DIR),
    name="images"
)
# app.mount("/images", StaticFiles(directory="/home/abdullah-saeed/PycharmProjects/Database_Images/"), name="images")

app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(event.router)
app.include_router(user.router)
app.include_router(frontend.router)


@app.middleware("http")
async def no_cache_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/")
def root():
    return RedirectResponse("/auth/home")
