from database import Base
from sqlalchemy import Column, Integer, String, BOOLEAN

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    location = Column(String)
    completed = Column(BOOLEAN, default=False)
