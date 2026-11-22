from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
DATABASE_URL = "postgresql://postgres:michalr2007@localhost:5432/fastapidb"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# פונקציה שמספקת session לכל בקשה
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()