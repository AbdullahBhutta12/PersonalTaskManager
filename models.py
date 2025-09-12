# from typing import List

from sqlalchemy import Column, Integer, String, BOOLEAN#, ForeignKey
# from sqlalchemy.orm import relationship

from database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    location = Column(String)
    completed = Column(BOOLEAN, default=False)

    # users: List[User]= relationship("User", back_populates="tasks")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String)
    location = Column(String)
    event_date = Column(String)
    event_time = Column(String)

    # users: List[User]= relationship("User", back_populates="events")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    # task_id: int = Column(Integer, ForeignKey("tasks.id"))
    # tasks: Task= relationship("Task", back_populates="users")
    #
    # event_id: int = Column(Integer ,ForeignKey("events.id"))
    # events: Event = relationship("Event", back_populates="users")