from pydantic import BaseModel, ConfigDict

class HousingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    area_code: str
    area_name: str
    year: int
    median_house_price: float
    median_income: float
    affordability_ratio: float
