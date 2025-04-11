from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from note_api.database import get_db
from note_api.models.note import Note
from note_api.models.user import User
from note_api.schemas.note import NoteCreate, NoteOut
from note_api.routers.auth import get_current_user

router = APIRouter(
    prefix='/notes',
    tags=['Notes']
)

def get_user_note_or_404(note_id: int, current_user: User, db: Session) -> Note:
    """
    Допоміжна функція: отримати нотатку, якщо вона існує і належить поточному юзеру
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note or note.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail='Note not found or access denied')
    return note


@router.post('/', response_model=NoteOut)
def create_note(note_input: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Створити нову нотатку
    """
    new_note = Note(title=note_input.title, content=note_input.content, owner_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get('/', response_model=List[NoteOut])
def get_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Отримати всі нотатки поточного користувача
    """
    return db.query(Note).filter(Note.owner_id == current_user.id).all()


@router.get('/{id}', response_model=NoteOut)
def get_note(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Отримати одну нотатку по ID
    """
    return get_user_note_or_404(id, current_user, db)


@router.delete('/{id}')
def delete_note(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Видалити нотатку по ID
    """
    note = get_user_note_or_404(id, current_user, db)
    db.delete(note)
    db.commit()
    return {'message': 'Note deleted'}


@router.put('/{id}', response_model=NoteOut)
def update_note(id: int, note_input: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Оновити нотатку
    """
    note = get_user_note_or_404(id, current_user, db)
    note.title = note_input.title
    note.content = note_input.content
    db.commit()
    db.refresh(note)
    return note
