from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship

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

    task = relationship("Task", back_populates="users")
    event = relationship("Event", back_populates="users")
