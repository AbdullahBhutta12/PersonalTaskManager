from pydantic import BaseModel
from datetime import date, time


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
    event_date : date
    event_time: time
