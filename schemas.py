from pydantic import BaseModel, ConfigDict
from typing import List

class Task(BaseModel):
    title: str
    location: str

class ShowTask(BaseModel):
    tasks: List[Task]
    model_config = ConfigDict(from_attributes=True)
