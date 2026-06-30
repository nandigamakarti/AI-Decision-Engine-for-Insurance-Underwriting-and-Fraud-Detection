from pydantic import BaseModel, Field
from typing import List
from datetime import date


class Claim(BaseModel):
    """Individual claim record"""
    claim_id: str
    claim_date: date
    claim_type: str  # "Medical|Dental|Vision|Other"
    claim_amount: float
    approved_amount: float
    status: str  # "Approved|Denied|Pending"


class ClaimsData(BaseModel):
    """Claims history risk factors"""
    customer_id: str

    # Claims History
    total_claims_count: int = Field(ge=0)
    claims_last_12mo: int = Field(ge=0)
    claims_last_36mo: int = Field(ge=0)

    # Financial Impact
    total_claims_amount: float = Field(ge=0)
    average_claim_amount: float = Field(ge=0)
    highest_single_claim: float = Field(ge=0)

    # Patterns
    claim_frequency_trend: str = Field(..., pattern="^(Increasing|Stable|Decreasing)$")

    # Detailed Claims
    recent_claims: List[Claim] = []

    # Fraud Indicators
    suspicious_patterns_detected: bool = False
    fraud_score: float = Field(ge=0, le=100)

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "customer_id": "CUST_001",
                "total_claims_count": 8,
                "claims_last_12mo": 2,
                "claims_last_36mo": 5,
                "total_claims_amount": 15000,
                "average_claim_amount": 1875,
                "highest_single_claim": 5000,
                "claim_frequency_trend": "Stable",
                "recent_claims": [
                    {
                        "claim_id": "CLM_001",
                        "claim_date": "2024-08-15",
                        "claim_type": "Medical",
                        "claim_amount": 2500,
                        "approved_amount": 2200,
                        "status": "Approved"
                    }
                ],
                "suspicious_patterns_detected": False,
                "fraud_score": 12
            }
        }
