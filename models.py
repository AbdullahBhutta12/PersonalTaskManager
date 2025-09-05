from sqlalchemy import Column, Integer, String, BOOLEAN, Date, Time

from database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    location = Column(String)
    completed = Column(BOOLEAN, default=False)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String)
    location = Column(String)
    event_date = Column(Date)
    event_time = Column(Time)
