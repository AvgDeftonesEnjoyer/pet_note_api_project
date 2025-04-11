from fastapi import APIRouter, Depends, HTTPException, status

from note_api.schemas import user
from note_api.models.user import User
from note_api.routers.auth import get_current_user

router = APIRouter()

@router.get('/profile', response_model= user.UserOut)
def get_user(current_user : User = Depends(get_current_user)):
    return current_user

