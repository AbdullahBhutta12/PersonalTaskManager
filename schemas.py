from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: str
    location: str
    completed: bool=False

class Event(BaseModel):
    id: int
    event_name: str
    location: str
    event_date : str
    event_time: str


class CreateUser(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str

