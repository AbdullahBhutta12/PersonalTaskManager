from pydantic import BaseModel, ConfigDict
from typing import List


class Task(BaseModel):
    title: str
    description: str
    location: str
    completed: bool=False
    model_config = ConfigDict(from_attributes=True)


class ShowTask(BaseModel):
    tasks: List[Task]
    model_config = ConfigDict(from_attributes=True)

class UpdateTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)