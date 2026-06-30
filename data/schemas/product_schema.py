from pydantic import BaseModel, Field
from typing import List


class ProductData(BaseModel):
    """Product and underwriting risk factors"""
    customer_id: str

    # Product Details
    product_type: str = Field(..., pattern="^(Term Life|Whole Life|Health|Critical Illness|Disability)$")
    coverage_amount: float = Field(gt=0)
    premium_amount: float = Field(gt=0)
    policy_term_years: int = Field(ge=1, le=100)

    # Underwriting
    underwriting_class: str = Field(..., pattern="^(Preferred|Standard|Substandard|Declined)$")
    loading_percentage: float = Field(ge=0, le=500)  # Extra premium %
    exclusions: List[str] = []

    # Pricing Adequacy
    loss_ratio_expected: float = Field(ge=0, le=200)
    profit_margin: float = Field(ge=-100, le=100)

    # Risk Indicators
    sum_assured_to_income_ratio: float = Field(ge=0)
    affordability_score: float = Field(ge=0, le=100)

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "customer_id": "CUST_001",
                "product_type": "Term Life",
                "coverage_amount": 500000,
                "premium_amount": 850,
                "policy_term_years": 20,
                "underwriting_class": "Standard",
                "loading_percentage": 0,
                "exclusions": [],
                "loss_ratio_expected": 65,
                "profit_margin": 15,
                "sum_assured_to_income_ratio": 4.0,
                "affordability_score": 75
            }
        }
