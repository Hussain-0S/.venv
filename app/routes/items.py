from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependancies.auth import get_current_user
from app.models import Item, User
from app.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.services import item_services

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model= ItemResponse)
def createItem(item : ItemCreate, current_user  = Depends(get_current_user), db : Session = Depends(get_db)):
    return item_services.create_item(item.title, current_user.id, db)

@router.get("/",response_model= list[ItemResponse])
def get_items(current_user :User = Depends(get_current_user), db : Session = Depends(get_db)):
    return current_user.items  # Using relationships
   # return db.query(Item).filter(Item.owner_id == current_user.id).all()

@router.put("/", response_model= ItemResponse)
def update_item(item : ItemUpdate, current_user = Depends(get_current_user), db : Session = Depends(get_db)):
    return item_services.update_item(item.id, item.title, current_user.id, db)

@router.delete("/")
def delete_item(id : int, current_user = Depends(get_current_user), db : Session = Depends(get_db)):
    return item_services.delete_item(id, current_user.id, db)