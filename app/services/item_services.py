from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Item, User


def create_item(title, owner_id, db: Session):

    db_item = Item(title = title, owner_id = owner_id)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def update_item(oldItem_ID, newItem, owner_id, db : Session):
    db_item = db.query(Item).filter(Item.id == oldItem_ID).first()

    if (db_item.owner_id != owner_id) :
        raise HTTPException(status_code= 403, detail="Not allowed")
    if not db_item : 
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.title = newItem

    db.commit()
    db.refresh(db_item)

    return db_item


def delete_item(itemID, owner_id, db :Session):
    db_item = db.query(Item).filter(Item.id == itemID).first()

    if (db_item.owner_id != owner_id) :
        raise HTTPException(status_code= 403, detail="Not allowed")
    if not db_item : 
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()

    return "Item deleted"