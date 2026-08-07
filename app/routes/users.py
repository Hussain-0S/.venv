from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas import UserCreate, UserResponse, UserLogin
from app.models import User
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils.security import password_hash, password_verify
from app.utils.auth import create_token
from app.dependancies.auth import get_current_user

router = APIRouter()


@router.get("/users", response_model= list[UserResponse])
def GetUsers(db : Session = Depends(get_db)): # Get all users
    return db.query(User).all()


@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    
    return current_user


@router.get("/users/{user_id}", response_model= UserResponse)
def GetUser(user_id : int, db : Session = Depends(get_db)):  # Get user by ID
    user = db.query(User).filter(User.id == user_id).first()

    if not user : raise HTTPException(status_code= 404, detail = "User not found")

    return user



@router.post("/register",status_code= status.HTTP_201_CREATED)
def register(user : UserCreate, db: Session = Depends(get_db)): # Create a new user in the database

    hashed_pwd = password_hash(user.password)
    

    db_user = User(name = user.name , job = user.job, email= user.email , password = hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return (db_user)


@router.post("/login")
def login(user : UserLogin, db : Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not password_verify(user.password, db_user.password) : 
        raise HTTPException(status_code=401, detail="Credantials failed")
    
    user_Token = create_token({"subject": db_user.email})

    return {"access_token" : user_Token}
    


@router.put("/users/{user_id}")
def UpdateUser (updatedUser : UserCreate, user_id : int, db : Session = Depends(get_db)): # Update existing user

    user = db.query(User).filter(User.id == user_id).first()

    if not user: raise HTTPException(satatus_code=404 , detail = "User not found")

    user.name = updatedUser.name
    user.job = updatedUser.job

    db.commit()
    db.refresh(user)

    return user

@router.delete("/users/{user_id}")
def DeleteUser(user_id : int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user : raise HTTPException(status_code= 404, detail = "User not found")

    db.delete(user)
    db.commit()

    return "User deleted"