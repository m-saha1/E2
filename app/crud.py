from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import HousingData

router = APIRouter()

# Generator to handle opening and closing the database connection per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    # Limit to 100 records so the API doesn't overload and crash
    return db.query(HousingData).limit(100).all()

@router.post("/")
def create(record: dict, db: Session = Depends(get_db)):
    # Converts the incoming JSON dict into a HousingData object and saves it to Postgres
    data = HousingData(**record)
    db.add(data)
    db.commit()
    return {"status": "created"}
