from pydantic import BaseModel,EmailStr, Field

class UserCreate(BaseModel):
    name : str
    job : str
    email : EmailStr # Built-in email verificatio 
    password :str = Field(
        min_length= 6,
        max_length= 30
    )

class UserResponse(BaseModel):
    
    name : str
    job : str
    email : str

    class config:   # Metadata for the class , it is like the "settings" for this class. 
        orm_mode = True  #      It is not called , but the system reads it automatically

class UserLogin(BaseModel):
    email : str
    password : str

class userMini(BaseModel):
    # Used inside the item response to show user
    id : int
    name : str

    class config:
        orm_mode: True
    



class ItemCreate(BaseModel):
    title : str = Field(
        min_length=1,
        max_length= 60
    )

class ItemResponse(BaseModel):
    id : int
    title : str
    owner : userMini

    class config:
        orm_mode: True

class ItemUpdate(BaseModel):
    id : int
    title : str