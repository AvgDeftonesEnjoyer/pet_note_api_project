from sqlalchemy import Column, Integer, String
from note_api.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable= False)
    email = Column(String, unique= True, index = True, nullable = False)
    hashed_password = Column(String, nullable = False)
    
    notes = relationship("Note", back_populates="owner")