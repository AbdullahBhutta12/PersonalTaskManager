from typing import List

from pydantic import BaseModel, ConfigDict

class TaskBase(BaseModel):
    title: str
    description: str
    location: str
    completed: bool = False

class Task(TaskBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class EventBase(BaseModel):
    event_name: str
    location: str
    event_date: str
    event_time: str

class Event(EventBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
