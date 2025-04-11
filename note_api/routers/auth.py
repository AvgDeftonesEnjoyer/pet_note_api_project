from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from note_api import models
from note_api.schemas import user
from note_api.database import get_db
from note_api.models.user import User

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = 'super_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES))
    to_encode['exp'] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/register', response_model=user.UserOut)
async def register_user(new_user: user.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == new_user.username).first():
        raise HTTPException(status_code=400, detail='Username already taken')
    if db.query(User).filter(User.email == new_user.email).first():
        raise HTTPException(status_code=400, detail='Email already taken')

    hashed_password = get_password_hash(new_user.password)
    new_user_obj = User(username=new_user.username, email=new_user.email, hashed_password=hashed_password)

    db.add(new_user_obj)
    db.commit()
    db.refresh(new_user_obj)

    return new_user_obj

@router.post('/login')
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_obj = db.query(User).filter(User.username == form_data.username).first()
    if not user_obj:
        raise HTTPException(status_code=400, detail='User not registered')

    if not verify_password(form_data.password, user_obj.hashed_password):
        raise HTTPException(status_code=400, detail='Wrong password')

    token = create_access_token(data={'sub': user_obj.username})
    return {'access_token': token, 'token_type': 'bearer'}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get('sub')
    except JWTError:
        raise HTTPException(status_code=401, detail='Token error')

    if not username:
        raise HTTPException(status_code=401, detail='Invalid credentials')

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail='User not found')

    return user