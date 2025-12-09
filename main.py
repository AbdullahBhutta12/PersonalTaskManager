from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

import models
import database
from router import task, event, user, authentication, frontend

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecret123")
app.mount("/images", StaticFiles(directory="/home/abdullah-saeed/PycharmProjects/Database_Images/"), name="images")

app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(event.router)
app.include_router(user.router)
app.include_router(frontend.router)

