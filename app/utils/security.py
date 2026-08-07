from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def password_hash(password : str):
    return pwd.hash(password)

def password_verify(password, hashed):
    return pwd.verify(secret= password, hash= hashed)


