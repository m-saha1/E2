from sqlalchemy import Column, Integer, String
from app.database import Base

class HousingData(Base):
    __tablename__ = "housing_data"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(String)
    geography = Column(String)
    year = Column(Integer)
    value = Column(Integer)

