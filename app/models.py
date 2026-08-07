from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import engine, Base
from sqlalchemy.orm import  relationship



class User(Base): # Inhereted from the Base class to create a mapping between User and database
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String)
    job = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship("Item", back_populates="owner")
    files = relationship("File", back_populates="owner")
    


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    owner_id = Column(Integer, ForeignKey ("users.id"))
    owner = relationship("User", back_populates="items")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    file_path = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="files")



Base.metadata.create_all(bind = engine) 