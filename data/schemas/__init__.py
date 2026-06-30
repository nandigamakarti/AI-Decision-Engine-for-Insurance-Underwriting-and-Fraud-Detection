"""
Risk Assessment Engine - Data Schemas

This module contains all Pydantic models for the 7 risk dimensions:
1. Demographic Risk
2. Financial Risk
3. Medical/PED Risk
4. Regional Risk
5. Claims History Risk
6. Agent/Channel Risk
7. Product/Underwriting Risk
"""

from data.schemas.demographic_schema import DemographicData
from data.schemas.financial_schema import FinancialData
from data.schemas.medical_schema import (
    MedicalData,
    MedicalCondition,
    Medication,
    Procedure,
)
from data.schemas.regional_schema import RegionalData
from data.schemas.claims_schema import ClaimsData, Claim
from data.schemas.agent_schema import AgentData
from data.schemas.product_schema import ProductData

__all__ = [
    "DemographicData",
    "FinancialData",
    "MedicalData",
    "MedicalCondition",
    "Medication",
    "Procedure",
    "RegionalData",
    "ClaimsData",
    "Claim",
    "AgentData",
    "ProductData",
]
