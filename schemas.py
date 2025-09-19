from typing import List

from pydantic import BaseModel, ConfigDict


class Task(BaseModel):
    id: int
    title: str
    description: str
    location: str
    completed: bool = False
    model_config = ConfigDict(from_attributes=True)


class Event(BaseModel):
    id: int
    event_name: str
    location: str
    event_date: str
    event_time: str
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


# class ShowUser(BaseModel):
#     name: str
#     email: str
#     tasks: List[Task]
#     events: List[Event]
#     model_config = ConfigDict(from_attributes=True)
#
# class ShowTask(BaseModel):
#     name: str
#     email: str
#     tasks: List[Task]
#     model_config = ConfigDict(from_attributes=True)
#
# class ShowEvent(BaseModel):
#     name: str
#     email: str
#     events: List[Event]
#     model_config = ConfigDict(from_attributes=True)

class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
