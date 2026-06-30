"""
Data extraction services for risk assessment.

This module provides functions to extract data from database tables
and build data objects for risk calculators.
"""

from .demographic_extractor import extract_demographic_data
from .financial_extractor import extract_financial_data
from .medical_extractor import extract_medical_data
from .regional_extractor import extract_regional_data
from .claims_extractor import extract_claims_data
from .agent_extractor import extract_agent_data
from .product_extractor import extract_product_data

__all__ = [
    "extract_demographic_data",
    "extract_financial_data",
    "extract_medical_data",
    "extract_regional_data",
    "extract_claims_data",
    "extract_agent_data",
    "extract_product_data"
]
