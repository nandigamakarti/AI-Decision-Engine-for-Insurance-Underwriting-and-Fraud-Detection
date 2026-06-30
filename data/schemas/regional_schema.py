from pydantic import BaseModel, Field
from typing import Optional


class RegionalData(BaseModel):
    """Geographic and regional risk factors"""
    customer_id: str

    # Location
    zip_code: str
    city: str
    state: str
    county: Optional[str] = None

    # Healthcare Access
    nearest_hospital_km: float = Field(ge=0)
    hospitals_within_25km: int = Field(ge=0)
    specialists_available: bool

    # Environmental
    air_quality_index: int = Field(ge=0, le=500)
    natural_disaster_zone: bool
    disaster_type: Optional[str] = None  # "Hurricane|Earthquake|Flood|None"

    # Socioeconomic
    median_income_area: float = Field(ge=0)
    crime_rate_per_1000: float = Field(ge=0)
    unemployment_rate: float = Field(ge=0, le=100)

    # Cost of Living
    healthcare_cost_index: float = Field(ge=0)  # 100 = national average

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "customer_id": "CUST_001",
                "zip_code": "10001",
                "city": "New York",
                "state": "NY",
                "county": "Manhattan",
                "nearest_hospital_km": 2.5,
                "hospitals_within_25km": 15,
                "specialists_available": True,
                "air_quality_index": 45,
                "natural_disaster_zone": False,
                "median_income_area": 85000,
                "crime_rate_per_1000": 15.2,
                "unemployment_rate": 4.5,
                "healthcare_cost_index": 135
            }
        }
