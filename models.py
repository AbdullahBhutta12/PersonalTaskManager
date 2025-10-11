from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    location = Column(String)
    completed = Column(BOOLEAN, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="task")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String)
    location = Column(String)
    event_date = Column(String)
    event_time = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="event")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    profile_image = Column(String)

    task = relationship("Task", back_populates="users")
    event = relationship("Event", back_populates="users")
    device_tokens = relationship("DeviceToken", back_populates="users")

class DeviceToken(Base):
    __tablename__ = "device_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True)
    # platform = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="device_tokens")#, cascade="all, delete-orphan, single_parent=True")
