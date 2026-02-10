from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Item
import traceback

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    try:
        items = db.query(Item).all()
        return items
    except Exception as e:
        traceback.print_exc()   # <-- THIS IS THE KEY
        return {"error": str(e)}
