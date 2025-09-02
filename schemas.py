from pydantic import BaseModel


class Task(BaseModel):
    title: str
    location: str

class UpdateTask(BaseModel):
    title: str
    location: str
    completed: bool