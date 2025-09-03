from fastapi import FastAPI
from router import task
import models
from database import *

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(task.router)
