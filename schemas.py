from pydantic import BaseModel, ConfigDict
from datetime import datetime


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
    username: str
    email: str
    password: str


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    profile_image: str | None = None
    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    id: int
    username: str | None = None


# class Login(BaseModel):
#     username: str
#     password: str
#
#
class TokenIn(BaseModel):
    token: str


class Emails(BaseModel):
    email: str


class VerifyEmail(Emails):
    email: str
    verification_code: str
    # expiration_time: datetime
    model_config = ConfigDict(from_attributes=True)
