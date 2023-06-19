from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")

engine = create_engine(f'sqlite:///{SQLALCHEMY_DATABASE_URL}',connect_args={'check_same_thread': False})



# Enable the PostGIS extension
# engine.execute("CREATE EXTENSION IF NOT EXISTS postgis")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
