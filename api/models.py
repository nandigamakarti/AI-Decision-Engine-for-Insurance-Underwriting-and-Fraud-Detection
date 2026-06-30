"""
Pydantic models for API request and response validation.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    """Personal information of the insurance customer."""
    first_name: str = Field(..., description="First name of the customer")
    last_name: str = Field(..., description="Last name of the customer")
    date_of_birth: Optional[str] = Field(None, description="Date of birth (YYYY-MM-DD)")
    age: Optional[int] = Field(None, description="Age of the customer")
    gender: Optional[str] = Field(None, description="Gender of the customer")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")


class HealthInfo(BaseModel):
    """Health-related information of the customer."""
    health_conditions: Optional[List[str]] = Field(None, description="List of existing health conditions")
    medications: Optional[List[str]] = Field(None, description="List of current medications")
    medical_history: Optional[str] = Field(None, description="Detailed medical history")
    smoker: Optional[bool] = Field(None, description="Whether the customer is a smoker")
    alcohol_consumption: Optional[str] = Field(None, description="Alcohol consumption frequency/level")
    exercise_frequency: Optional[str] = Field(None, description="Exercise frequency")
    bmi: Optional[float] = Field(None, description="Body Mass Index")


class FinancialInfo(BaseModel):
    """Financial information of the customer."""
    annual_income: Optional[float] = Field(None, description="Annual income")
    employment_status: Optional[str] = Field(None, description="Employment status")
    occupation: Optional[str] = Field(None, description="Occupation/job title")
    credit_score: Optional[int] = Field(None, description="Credit score")
    outstanding_debts: Optional[float] = Field(None, description="Total outstanding debts")
    assets: Optional[float] = Field(None, description="Total assets value")


class ClaimsHistory(BaseModel):
    """Previous claims history of the customer."""
    total_claims: Optional[int] = Field(None, description="Total number of claims")
    major_claims: Optional[List[str]] = Field(None, description="List of major claims")
    claim_frequency: Optional[str] = Field(None, description="Frequency of claims")
    last_claim_date: Optional[str] = Field(None, description="Date of last claim")
    claim_amount_total: Optional[float] = Field(None, description="Total claim amount")


class CustomerDataInput(BaseModel):
    """Complete customer data input for risk assessment."""
    customer_id: Optional[str] = Field(None, description="Unique customer identifier")
    personal_info: PersonalInfo = Field(..., description="Customer personal information")
    health_info: Optional[HealthInfo] = Field(None, description="Customer health information")
    financial_info: Optional[FinancialInfo] = Field(None, description="Customer financial information")
    claims_history: Optional[ClaimsHistory] = Field(None, description="Customer claims history")
    additional_data: Optional[Dict[str, Any]] = Field(None, description="Additional custom fields")


class RiskFactor(BaseModel):
    """Individual risk factor."""
    factor_name: str = Field(..., description="Name of the risk factor")
    risk_level: str = Field(..., description="Risk level: LOW, MEDIUM, HIGH, CRITICAL")
    score: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    description: str = Field(..., description="Description of the risk factor")


class RiskAssessmentOutput(BaseModel):
    """Risk assessment output."""
    customer_id: Optional[str] = Field(None, description="Customer identifier")
    overall_risk_level: str = Field(..., description="Overall risk level: LOW, MEDIUM, HIGH, CRITICAL")
    overall_risk_score: float = Field(..., ge=0, le=100, description="Overall risk score (0-100)")
    risk_factors: List[RiskFactor] = Field(..., description="List of identified risk factors")
    recommendations: Optional[List[str]] = Field(None, description="Underwriting recommendations")
    assessment_date: str = Field(..., description="Date of assessment")
    additional_notes: Optional[str] = Field(None, description="Additional notes from the assessment")
