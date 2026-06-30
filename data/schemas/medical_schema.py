from pydantic import BaseModel, Field
from typing import List
from datetime import date


class MedicalCondition(BaseModel):
    """Medical condition with ICD-10 coding"""
    icd10_code: str
    description: str
    diagnosed_date: date
    treatment_status: str = Field(..., pattern="^(Active|Controlled|Resolved)$")


class Medication(BaseModel):
    """Medication with NDC coding"""
    ndc_code: str
    name: str
    dosage: str
    frequency: str


class Procedure(BaseModel):
    """Medical procedure with CPT coding"""
    cpt_code: str
    description: str
    procedure_date: date


class MedicalData(BaseModel):
    """Pre-existing disease (PED) and medical risk factors"""
    customer_id: str

    # Conditions
    conditions: List[MedicalCondition] = []

    # Medications
    current_medications: List[Medication] = []

    # Procedures
    past_procedures: List[Procedure] = []

    # Vitals
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    bmi: float = Field(ge=10, le=100)
    blood_pressure_systolic: int = Field(ge=60, le=250)
    blood_pressure_diastolic: int = Field(ge=40, le=150)

    # Family History
    family_history_cancer: bool = False
    family_history_heart_disease: bool = False
    family_history_diabetes: bool = False

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "customer_id": "CUST_001",
                "conditions": [
                    {
                        "icd10_code": "I10",
                        "description": "Essential hypertension",
                        "diagnosed_date": "2018-03-15",
                        "treatment_status": "Controlled"
                    }
                ],
                "current_medications": [
                    {
                        "ndc_code": "00093-7169-01",
                        "name": "Lisinopril",
                        "dosage": "10mg",
                        "frequency": "Daily"
                    }
                ],
                "past_procedures": [],
                "height_cm": 178,
                "weight_kg": 82,
                "bmi": 25.9,
                "blood_pressure_systolic": 128,
                "blood_pressure_diastolic": 82,
                "family_history_cancer": False,
                "family_history_heart_disease": True,
                "family_history_diabetes": False
            }
        }
