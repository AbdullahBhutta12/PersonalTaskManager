from fastapi import FastAPI

import models
import database
from router import task, event

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.include_router(task.router)
app.include_router(event.router)
