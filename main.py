from fastapi import FastAPI

import models
import database
from router import task, event, user

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
app.include_router(task.router)
app.include_router(event.router)
