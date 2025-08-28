from datetime import datetime
from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    content: str = Field(min_length=1, max_length=500)


class NoteOut(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  # Works with SQLAlchemy ORM objects
