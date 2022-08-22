from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection string


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Asdfgh.1@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# How the session behaves
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # the model which we extend in the future.

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
