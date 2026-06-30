from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class DemographicData(BaseModel):
    """Demographic risk factors"""
    customer_id: str

    # Identity
    first_name: str
    last_name: str
    date_of_birth: date
    age: int = Field(ge=0, le=120)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")

    # Lifestyle
    smoking_status: str = Field(..., pattern="^(Never|Former|Current)$")
    alcohol_consumption: str = Field(..., pattern="^(None|Moderate|Heavy)$")
    exercise_frequency: str = Field(..., pattern="^(Sedentary|Light|Moderate|Active)$")

    # Socioeconomic
    education_level: str = Field(..., pattern="^(High School|Bachelor|Master|Doctorate|Other)$")
    occupation: Optional[str] = None
    marital_status: str = Field(..., pattern="^(Single|Married|Divorced|Widowed)$")

    # Household
    household_size: int = Field(ge=1, le=20)
    dependents: int = Field(ge=0)

    # Geographic (basic)
    zip_code: str
    state: str

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "customer_id": "CUST_001",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1980-05-15",
                "age": 44,
                "gender": "Male",
                "smoking_status": "Never",
                "alcohol_consumption": "Moderate",
                "exercise_frequency": "Moderate",
                "education_level": "Bachelor",
                "occupation": "Software Engineer",
                "marital_status": "Married",
                "household_size": 4,
                "dependents": 2,
                "zip_code": "10001",
                "state": "NY"
            }
        }
