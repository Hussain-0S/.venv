from fastapi import UploadFile , HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.models import File
import os
from pathlib import Path

chunk_size = 1024 * 1024   #1 MB
MAX_SIZE = 10 * 1024 * 1024 #10 MB

allowed_Extensions = ['.jpg', '.png', '.jpeg', '.pdf']
allowed_types = [
    "image/png",
    "image/jpeg",
    "image/jpg",
    "application/pdf"
]


def uploadFile(file : UploadFile , display_name : str,  owner_id : int , db: Session):

    physical_filename = Path(file.filename).name
    file_path = f'app/uploads/{physical_filename}'
    total_size = 0
    

    # Validate File Type
    file_extension = os.path.splitext(file.filename)[1].lower()

    if (file_extension not in allowed_Extensions) and (file.content_type not in allowed_types):
        raise HTTPException(
            status_code=409,
            detail= "File Type not allowed"
        )


    try :
        with open(
            file_path,
            'wb'
        ) as buffer :

            print(MAX_SIZE)

            while chunk := file.file.read(chunk_size):

                total_size += len(chunk)

                # Validate file size
                if (total_size > MAX_SIZE):
                    raise HTTPException (
                        status_code= 400,
                        detail= "File size is too large"
                    )

                buffer.write(chunk)

            db_file = File(file_name = display_name, file_path = file_path, owner_id = owner_id)

            db.add(db_file)
            db.commit()
            db.refresh(db_file)

            return db_file

    except Exception:
        db.rollback()

        if os.path.exists(file_path):
            os.remove(file_path)

        raise



""" 
find file in db
check if owner is same
return file
 """
def returnFile(file_ID : int, owner_id : int, db : Session):

    # Find file
    file_db = db.query(File).filter(File.id == file_ID).first()

    # Check if file exists
    if not file_db :
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    # Match with onwer
    if (file_db.owner_id != owner_id):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )


    # Chueck if physicalf file exists
    if not os.path.exists(file_db.file_path) :
        raise HTTPException(
            status_code=404,
            detail="Physical file not found"
        )

    # Return the file
    extension  = Path(file_db.file_path).suffix
    download_name  = f'{file_db.file_name}{extension}'

    return FileResponse(
        path = file_db.file_path,
        filename = download_name
    )


    # DELETE ALL DB data related to saved files and refresh


def removeFile(file_id :int, owner_id :int, db :Session):

    db_file = db.query(File).filter(File.id == file_id).first()

    #Validate File record
    if not db_file :
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    #Validate ownership
    if (db_file.owner_id != owner_id):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )


    #Save file Path
    file_path = db_file.file_path

    #Delete File record
    try :

        db.delete(db_file)
        db.commit()

    except Exception :
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Could not delete file record"
        )


    #Delete physical file
    if os.path.exists(file_path):

        try :
            os.remove(file_path)

        except Exception :
            raise HTTPException(
                status_code=500,
                detail="File record deleted but physical file could not be deleted"
            )

    return {"message" : "File Deleted"}

def updateName(file_id : int, display_name : str,  owner_id : int , db: Session):

    file_db = db.query(File).filter(File.id == file_id).first()

    if not file_db :
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

    if (file_db.owner_id != owner_id):
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    file_db.file_name = display_name

    db.commit()
    db.refresh(file_db)

    return {"File Updated"}

