import uuid

from sqlalchemy import Column, String, TIMESTAMP, FLOAT, INT, Boolean, Sequence, Integer
from sqlalchemy.sql import func, text
from database.connection import Base, engine
from sqlalchemy.orm import sessionmaker



# Create a session to use the declarative ORM
Session = sessionmaker(bind=engine)
session = Session()

class Logs(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String(50))
    message = Column(String)
    component = Column(String)
    loglevel = Column(String)
    transaction_id = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(String(50))

Base.metadata.create_all(engine)
