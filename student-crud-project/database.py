from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # .env file load చేయడానికి

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://studentuser:student123@localhost/studentdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,    # Capital F
    autoflush=False,     # Correct spelling
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()