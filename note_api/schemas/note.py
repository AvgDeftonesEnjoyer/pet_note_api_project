from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    title : str
    content : str
    
class NoteOut(BaseModel):
    id: int
    title : str
    content: str
    created_at: datetime
    owner_id : int
    
    class Config:
        orm_mode = True