from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from note_api.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False, index=True, nullable= False)
    content = Column(String, unique= False, index = True, nullable = True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates='notes')