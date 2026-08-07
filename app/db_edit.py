from sqlalchemy import text
from database import engine

with engine.connect() as connection:
    connection.execute(text("DROP TABLE uploads"))
    connection.commit()