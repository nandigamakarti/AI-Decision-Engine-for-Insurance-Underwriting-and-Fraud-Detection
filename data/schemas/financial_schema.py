from pydantic import BaseModel, Field
from typing import Optional


class FinancialData(BaseModel):
    """Financial risk factors"""
    customer_id: str

    # Income
    annual_income: float = Field(ge=0)
    income_stability: str = Field(..., pattern="^(Stable|Variable|Unstable)$")
    employment_status: str = Field(..., pattern="^(Employed|Self-Employed|Unemployed|Retired)$")
    years_employed: Optional[int] = Field(None, ge=0)

    # Credit
    credit_score: int = Field(ge=300, le=850)
    credit_history_length: int = Field(ge=0, description="Years")

    # Debt
    total_debt: float = Field(ge=0)
    debt_to_income_ratio: float = Field(ge=0, le=10)  # Ratio
    mortgage_status: str = Field(..., pattern="^(Own|Rent|Mortgage)$")

    # Assets
    liquid_assets: float = Field(ge=0)
    total_assets: float = Field(ge=0)

    # Financial History
    bankruptcy_history: bool = False
    years_since_bankruptcy: Optional[int] = None
    late_payments_12mo: int = Field(ge=0)

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "customer_id": "CUST_001",
                "annual_income": 125000,
                "income_stability": "Stable",
                "employment_status": "Employed",
                "years_employed": 10,
                "credit_score": 750,
                "credit_history_length": 15,
                "total_debt": 50000,
                "debt_to_income_ratio": 0.4,
                "mortgage_status": "Mortgage",
                "liquid_assets": 25000,
                "total_assets": 300000,
                "bankruptcy_history": False,
                "late_payments_12mo": 0
            }
        }
