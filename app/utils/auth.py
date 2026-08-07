from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi import HTTPException
import os


Token_key = "secret"
Algorithm = "HS256"

def create_token(data : dict):
    to_encode = data.copy()

    expiration = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp" : expiration})  # adding expiratio date to the token
    
    return jwt.encode(to_encode,key= Token_key , algorithm= Algorithm)  # creating the Token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, Token_key, algorithms=[Algorithm])
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")