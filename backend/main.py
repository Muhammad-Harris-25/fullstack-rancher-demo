# backend/main.py
import asyncio
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

import crud, schemas
from database import Base, engine, SessionLocal

app = FastAPI(title="Notes API")

# Request-scoped DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables on startup, with retries (don’t crash the app)
@app.on_event("startup")
async def on_startup():
    for i in range(30):  # ~60s total
        try:
            with engine.begin() as conn:
                Base.metadata.create_all(bind=conn)
            print("✅ DB ready; tables ensured.")
            return
        except Exception as e:
            print(f"DB not ready ({i+1}/30): {e}")
            await asyncio.sleep(2)
    print("⚠️ DB still not reachable; readiness will remain 503 until it is.")

# Readiness: only OK when DB responds
@app.get("/api/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "db_unavailable", "detail": str(e)})

@app.get("/api/notes", response_model=list[schemas.NoteOut])
def get_notes(db: Session = Depends(get_db)):
    return crud.list_notes(db)

@app.post("/api/notes", response_model=schemas.NoteOut)
def create_note(payload: schemas.NoteCreate, db: Session = Depends(get_db)):
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="content required")
    return crud.create_note(db, payload.content.strip())
