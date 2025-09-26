from fastapi import FastAPI

import models
import database
from router import task, event, user, authentication, image


models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(event.router)
app.include_router(user.router)
app.include_router(image.router)
