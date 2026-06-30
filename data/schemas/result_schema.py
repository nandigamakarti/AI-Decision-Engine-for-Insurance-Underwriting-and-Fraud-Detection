from pydantic import BaseModel, Field
from typing import List


class RiskCalculationResult(BaseModel):
    """Standardized result for individual risk dimension calculations."""
    
    dimension: str = Field(..., description="Risk dimension name (demographic, financial, etc.)")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score from 0-100")
    risk_level: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$", description="Risk level category")
    risk_factors: List[str] = Field(default=[], description="List of identified risk factors")
    weight_in_overall: float = Field(..., ge=0, le=1, description="Weight in combined risk calculation")
    recommendations: List[str] = Field(default=[], description="Underwriting recommendations")
    
    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "dimension": "demographic",
                "risk_score": 35.0,
                "risk_level": "MEDIUM",
                "risk_factors": [
                    "Age 45 (elevated risk)",
                    "Former smoker"
                ],
                "weight_in_overall": 0.15,
                "recommendations": [
                    "Request health questionnaire",
                    "Verify smoking cessation date"
                ]
            }
        }


class CombinedRiskResult(BaseModel):
    """Combined risk assessment result across all dimensions."""
    
    customer_id: str = Field(..., description="Customer identifier")
    overall_risk_score: float = Field(..., ge=0, le=100, description="Weighted overall risk score")
    overall_risk_level: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$", description="Overall risk level")
    dimension_scores: List[RiskCalculationResult] = Field(..., description="Individual dimension risk scores")
    top_risk_factors: List[str] = Field(..., description="Top risk factors across all dimensions")
    underwriting_decision: str = Field(..., pattern="^(ACCEPT|REVIEW|DECLINE)$", description="Underwriting decision")
    recommended_loading: float = Field(..., ge=0, description="Recommended premium loading percentage")
    recommendations: List[str] = Field(default=[], description="Combined recommendations")
    
    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "customer_id": "CUST_001",
                "overall_risk_score": 42.5,
                "overall_risk_level": "MEDIUM",
                "dimension_scores": [],  # Would contain all 7 RiskCalculationResult objects
                "top_risk_factors": [
                    "Age 45 (elevated risk) (Demographic)",
                    "Moderate debt-to-income ratio (40.0%) (Financial)",
                    "Overweight (BMI: 26.5) (Medical)"
                ],
                "underwriting_decision": "ACCEPT",
                "recommended_loading": 10.0,
                "recommendations": [
                    "Accept with 10.0% premium loading",
                    "Request comprehensive health questionnaire"
                ]
            }
        }
