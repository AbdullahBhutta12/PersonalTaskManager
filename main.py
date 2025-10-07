from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import models
import database
from router import task, event, user, authentication, notification


models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
app.mount("/images", StaticFiles(directory="/home/abdullah-saeed/PycharmProjects/Database_Images/"), name="images")

app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(event.router)
app.include_router(user.router)
app.include_router(notification.router)
