from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()  #  load all the variables found in .env as environment variables.

Token_key = os.getenv("TOKEN_KEY")   # Used to be just SECRET , now changed for security
Algorithm = os.getenv("ALGORITHM")

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