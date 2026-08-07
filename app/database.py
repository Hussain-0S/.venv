from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Database_URL = "sqlite:///./test.db"

Base = declarative_base()
engine = create_engine(Database_URL)
localSession = sessionmaker(bind=engine)

def get_db():
    db = localSession()

    try :
        yield db
    finally:
        db.close()


