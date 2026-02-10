from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Item
from pydantic import BaseModel
import traceback

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ItemCreate(BaseModel):
    name: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    try:
        return db.query(Item).all()
    except Exception as e:
        traceback.print_exc()
        raise e

@app.post("/items")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        db_item = Item(name=item.name)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        traceback.print_exc()
        raise e
