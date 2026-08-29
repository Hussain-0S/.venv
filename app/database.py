from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  #  load all the variables found in .env as environment variables.

Database_URL = os.getenv("DATABASE_URL")

Base = declarative_base()
engine = create_engine(Database_URL)
localSession = sessionmaker(bind=engine)

def get_db():
    db = localSession()

    try :
        yield db
    finally:
        db.close()


