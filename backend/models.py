from sqlalchemy import Column, Integer, String, DateTime, func
import database  # absolute import


class Note(database.Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
