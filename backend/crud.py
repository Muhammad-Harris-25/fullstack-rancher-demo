from typing import List
from sqlalchemy.orm import Session
import models  # absolute import; not "from . import models"


def create_note(db: Session, content: str) -> models.Note:
    """Create and return a new Note."""
    note = models.Note(content=content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def list_notes(db: Session) -> List[models.Note]:
    """Return notes ordered by newest first."""
    return db.query(models.Note).order_by(models.Note.id.desc()).all()
