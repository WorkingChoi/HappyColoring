from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Database connection
username = 'coloring'
password = 'happy'
host = 'localhost'
database = 'coloring'

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{username}:{password}@{host}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#engine = create_engine(
#    "postgresql+psycopg://test:testtest@localhost/test",
#    echo=False
#)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
