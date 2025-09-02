from pydantic import BaseModel


class Task(BaseModel):
    title: str
    location: str

# class UpdateTask(BaseModel):
#     name: str
#     location: str
#     completed: bool
#
# class TaskResponse(BaseModel):
#     id: int
#     name: str
#     location: str
#     completed: bool