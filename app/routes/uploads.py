from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
import os
from app.dependancies.auth import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session
from app.services import files_services
from app.models import User

#   Secure file extension and type
#   Limit file size
#   Secure fileName a little not fully cuz fck you


router = APIRouter(prefix="/uploads", tags=["Uploads"])

@router.post("/")
def uploadFile(display_name : str, file : UploadFile = File(...), current_user :User =  Depends(get_current_user), db : Session = Depends(get_db)):
    return files_services.uploadFile(file, display_name=display_name, owner_id=current_user.id, db= db)


@router.get("/")
def returnFile(fileID : int, current_owner : User = Depends(get_current_user), db : Session = Depends(get_db)):
    return files_services.returnFile(file_ID= fileID, owner_id= current_owner.id, db = db)


# DELETE LATER
@router.get("/Testing purpose")
def get_all(current_user : User = Depends(get_current_user)):
    return current_user.files


@router.put("/")
def updateFile(fileID : int, newName : str, current_owner : User = Depends(get_current_user), db : Session = Depends(get_db)):
    return files_services.updateName(file_id= fileID, display_name=newName, owner_id= current_owner.id, db = db)


@router.delete("/")
def removeFile(file_id : int, current_user :User = Depends(get_current_user), db: Session = Depends(get_db)):
    return files_services.removeFile(file_id= file_id, owner_id=current_user.id, db=db)