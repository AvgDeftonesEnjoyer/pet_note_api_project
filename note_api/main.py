from fastapi import FastAPI
from note_api.database import Base, engine
from note_api.routers import auth, notes, user

app = FastAPI()

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)

@app.get('/')
async def root():
    return {'message': 'Note api is running'}
