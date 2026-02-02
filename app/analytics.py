from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app.models import HousingData

router = APIRouter()

# Uses the same generator as crud.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/average-price")
def average_price(db: Session = Depends(get_db)): # Changed from SessionLocal to get_db
    result = db.query(func.avg(HousingData.value)).scalar()
    return {"average_value": result or 0}

