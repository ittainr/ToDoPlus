"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATE
from sqlalchemy.orm import relationship
from database import Base

# TODO: Complete your models
class User(Base):
    __tablename__ = "users"
    
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)
    daily_time = Column("daily_time", INTEGER)
    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"

    id = Column("id", INTEGER, autoincrement=True, primary_key=True)
    task_name = Column("task_name", TEXT, nullable=False)
    due_date = Column("due_date", DATE, nullable=False)
    time_needed = Column("time_needed", INTEGER, nullable=False)
    time_spent = Column("time_spent", INTEGER)
    user_username = Column('user_username', TEXT, ForeignKey('users.username'))
    user = relationship("User", back_populates="tasks")
