from fastapi import Header, HTTPException, Depends
from app.utils.auth import verify_token
from app.database import get_db
from app.models import User
from sqlalchemy.orm import Session

def get_current_user(authentication : str = Header(None), db : Session = Depends(get_db)):
    print(authentication)
    if not authentication:
        raise HTTPException(status_code=401, detail="Token missing")

    token = authentication.replace("Bearer ", "")

    payload = verify_token(token)

    email = payload["subject"]
    
    user  = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user