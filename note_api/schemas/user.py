from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username : str
    email : str
    password : str
    
class UserLogin(BaseModel):
    username : str
    password : str
    
class UserOut(BaseModel):
    id : int
    username: str
    email : EmailStr
    
    class config:
        orm_mode = True