import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

TESTING = os.getenv('TESTING')

DB_URL = f"{os.getenv('DB_URL')}_test" if TESTING else os.getenv('DB_URL')

engine = sqlalchemy.create_engine(DB_URL)
database = databases.Database(DB_URL)
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()