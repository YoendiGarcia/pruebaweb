from sqlalchemy import Column, Integer,String

from database import Base

class Task(Base):

    __tablename__ = "task"

    id = Column(Integer,autoincrement=True,primary_key=True)
    title = Column(String)

