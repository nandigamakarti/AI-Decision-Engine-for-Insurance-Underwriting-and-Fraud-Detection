"""
AI-powered risk assessment service using GPT-OSS-20B model.

This module provides AI-based risk assessment functions that parallel
the rule-based calculators, using the Ollama service for inference.
"""

import json
import logging
from typing import Dict, Any

from data.schemas.demographic_schema import DemographicData
from data.schemas.financial_schema import FinancialData
from data.schemas.medical_schema import MedicalData
from data.schemas.regional_schema import RegionalData
from data.schemas.claims_schema import ClaimsData
from data.schemas.agent_schema import AgentData
from data.schemas.product_schema import ProductData
from data.schemas.result_schema import RiskCalculationResult
from services.ollama_service import ollama_service

logger = logging.getLogger(__name__)


def assess_demographic_risk_ai(data: DemographicData) -> RiskCalculationResult:
    """
    AI-powered demographic risk assessment using GPT-OSS-20B.
    
    Args:
        data: DemographicData containing customer demographic information
        
    Returns:
        RiskCalculationResult with AI-generated risk assessment
    """
    prompt = f"""You are an expert insurance underwriter. Analyze the demographic data and provide a risk assessment.

CUSTOMER DATA:
- Age: {data.age}
- Gender: {data.gender}
- Smoking Status: {data.smoking_status}
- Alcohol Consumption: {data.alcohol_consumption}
- Exercise Frequency: {data.exercise_frequency}
- Occupation: {data.occupation}
- Marital Status: {data.marital_status}

ASSESSMENT CRITERIA:
- Age Risk: 18-30 (LOW), 31-50 (MEDIUM), 51-70 (HIGH), 70+ (CRITICAL)
- Smoking: Never (0 points), Former (+15), Current (+40)
- Alcohol: None (0), Moderate (+5), Heavy (+20)
- Exercise: Active (0), Moderate (+5), Light (+10), Sedentary (+15)

IMPORTANT: You MUST include at least 3-5 risk factors showing what you assessed.
Examples: "Age {data.age} (low/moderate/high risk)", "Non-smoker (favorable)", "Active lifestyle (favorable)"

Provide a JSON response with:
{{
  "risk_score": <0-100>,
  "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "risk_factors": ["factor1", "factor2", "factor3"],
  "recommendations": ["rec1", "rec2"]
}}

CRITICAL: risk_factors array MUST have at least 3 items. Return ONLY valid JSON."""

    response = ollama_service._call_ollama(prompt)
    parsed = _parse_ai_response(response)
    
    return RiskCalculationResult(
        dimension="demographic",
        risk_score=parsed["risk_score"],
        risk_level=parsed["risk_level"],
        risk_factors=parsed["risk_factors"],
        weight_in_overall=0.15,
        recommendations=parsed["recommendations"]
    )


def assess_financial_risk_ai(data: FinancialData) -> RiskCalculationResult:
    """AI-powered financial risk assessment."""
    prompt = f"""You are an expert insurance underwriter. Analyze the financial data and provide a risk assessment.

CUSTOMER DATA:
- Credit Score: {data.credit_score}
- Annual Income: ${data.annual_income:,.2f}
- Debt-to-Income Ratio: {data.debt_to_income_ratio:.1%}
- Employment Status: {data.employment_status}
- Income Stability: {data.income_stability}
- Bankruptcy History: {data.bankruptcy_history}
- Late Payments (12mo): {data.late_payments_12mo}

ASSESSMENT CRITERIA:
- Credit Score: 750+ (LOW), 650-749 (MEDIUM), 550-649 (HIGH), <550 (CRITICAL)
- Debt-to-Income: <0.3 (LOW), 0.3-0.5 (MEDIUM), 0.5-0.8 (HIGH), >0.8 (CRITICAL)
- Bankruptcy: Recent (<3yr) is CRITICAL, 3-7yr is HIGH, >7yr is MEDIUM

IMPORTANT: You MUST include at least 3-5 risk factors showing what you assessed, even if favorable.
Examples of risk factors to include:
- "Credit score {data.credit_score} (excellent/good/fair/poor)"
- "Debt-to-income ratio {data.debt_to_income_ratio:.1%} (low/moderate/high)"
- "No bankruptcy history (favorable)" or "Bankruptcy {data.years_since_bankruptcy} years ago"
- "Stable/Variable/Unstable income"
- "Employment status: {data.employment_status}"
- "No late payments (favorable)" or "Late payments: {data.late_payments_12mo}"

Provide a JSON response with:
{{
  "risk_score": <0-100>,
  "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "risk_factors": ["factor1", "factor2", "factor3", "factor4"],
  "recommendations": ["rec1", "rec2"]
}}

CRITICAL: risk_factors array MUST have at least 3 items. Return ONLY valid JSON."""

    response = ollama_service._call_ollama(prompt)
    parsed = _parse_ai_response(response)
    
    return RiskCalculationResult(
        dimension="financial",
        risk_score=parsed["risk_score"],
        risk_level=parsed["risk_level"],
        risk_factors=parsed["risk_factors"],
        weight_in_overall=0.20,
        recommendations=parsed["recommendations"]
    )


def assess_medical_risk_ai(data: MedicalData) -> RiskCalculationResult:
    """AI-powered medical risk assessment."""
    conditions_str = ", ".join([f"{c.description} ({c.icd10_code})" for c in data.conditions]) if data.conditions else "None"
    medications_str = ", ".join([m.name for m in data.current_medications]) if data.current_medications else "None"
    
    prompt = f"""You are an expert insurance underwriter. Analyze the medical data and provide a risk assessment.

CUSTOMER DATA:
- Height: {data.height_cm} cm
- Weight: {data.weight_kg} kg
- BMI: {data.bmi}
- Blood Pressure: {data.blood_pressure_systolic}/{data.blood_pressure_diastolic}
- Pre-existing Conditions: {conditions_str}
- Current Medications: {medications_str}
- Family History - Cancer: {data.family_history_cancer}
- Family History - Heart Disease: {data.family_history_heart_disease}
- Family History - Diabetes: {data.family_history_diabetes}

ASSESSMENT CRITERIA:
- BMI: <18.5 or >30 increases risk
- Blood Pressure: >140/90 is HIGH risk
- Pre-existing conditions significantly increase risk
- Multiple medications indicate chronic conditions

IMPORTANT: You MUST include at least 3-5 risk factors.
Examples: "BMI {data.bmi} (normal/overweight)", "BP {data.blood_pressure_systolic}/{data.blood_pressure_diastolic}", "No pre-existing conditions (favorable)"

Provide a JSON response with:
{{
  "risk_score": <0-100>,
  "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "risk_factors": ["factor1", "factor2", "factor3"],
  "recommendations": ["rec1", "rec2"]
}}

CRITICAL: risk_factors array MUST have at least 3 items. Return ONLY valid JSON."""

    response = ollama_service._call_ollama(prompt)
    parsed = _parse_ai_response(response)
    
    return RiskCalculationResult(
        dimension="medical",
        risk_score=parsed["risk_score"],
        risk_level=parsed["risk_level"],
        risk_factors=parsed["risk_factors"],
        weight_in_overall=0.30,
        recommendations=parsed["recommendations"]
    )


def assess_regional_risk_ai(data: RegionalData) -> RiskCalculationResult:
    """AI-powered regional risk assessment."""
    prompt = f"""You are an expert insurance underwriter. Analyze the regional data and provide a risk assessment.

CUSTOMER DATA:
- Location: {data.city}, {data.state} ({data.zip_code})
- Nearest Hospital: {data.nearest_hospital_km} km
- Hospitals within 25km: {data.hospitals_within_25km}
- Specialists Available: {data.specialists_available}
- Air Quality Index: {data.air_quality_index}
- Natural Disaster Zone: {data.natural_disaster_zone}
- Crime Rate: {data.crime_rate_per_1000} per 1000
- Median Income: ${data.median_income_area:,.2f}
- Unemployment Rate: {data.unemployment_rate}%

ASSESSMENT CRITERIA:
- Healthcare access: More hospitals = lower risk
- Air quality: >100 AQI is concerning
- Natural disaster zones increase risk
- High crime rates increase risk

IMPORTANT: You MUST include at least 3-5 risk factors.
Examples: "Good hospital access ({data.hospitals_within_25km} hospitals)", "Air quality: {data.air_quality_index} AQI", "Crime rate: {data.crime_rate_per_1000} per 1000"

Provide a JSON response with:
{{
  "risk_score": <0-100>,
  "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "risk_factors": ["factor1", "factor2", "factor3"],
  "recommendations": ["rec1", "rec2"]
}}

CRITICAL: risk_factors array MUST have at least 3 items. Return ONLY valid JSON."""

    response = ollama_service._call_ollama(prompt)
    parsed = _parse_ai_response(response)
    
    return RiskCalculationResult(
        dimension="regional",
        risk_score=parsed["risk_score"],
        risk_level=parsed["risk_level"],
        risk_factors=parsed["risk_factors"],
        weight_in_overall=0.10,
        recommendations=parsed["recommendations"]
    )


def assess_claims_risk_ai(data: ClaimsData) -> RiskCalculationResult:
    """AI-powered claims history risk assessment."""
    prompt = f"""You are an expert insurance underwriter. Analyze the claims history and provide a risk assessment.

CUSTOMER DATA:
- Total Claims: {data.total_claims_count}
- Claims Last 12 Months: {data.claims_last_12mo}
- Claims Last 36 Months: {data.claims_last_36mo}
- Total Claims Amount: ${data.total_claims_amount:,.2f}
- Average Claim Amount: ${data.average_claim_amount:,.2f}
- Highest Single Claim: ${data.highest_single_claim:,.2f}
- Claim Frequency Trend: {data.claim_frequency_trend}
- Suspicious Patterns: {data.suspicious_patterns_detected}
- Fraud Score: {data.fraud_score}/100

ASSESSMENT CRITERIA:
- Frequent claims (>3 per year) increase risk
- High claim amounts indicate severity
- Increasing trend is concerning
- Fraud indicators are CRITICAL

IMPORTANT: You MUST include at least 3-5 risk factors.
Examples: "Total claims: {data.total_claims_count}", "Claims trend: {data.claim_frequency_trend}", "Average claim: ${data.average_claim_amount:,.0f}"

Provide a JSON response with:
{{
  "risk_score": <0-100>,
  "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "risk_factors": ["factor1", "factor2", "factor3"],
  "recommendations": ["rec1", "rec2"]
}}

CRITICAL: risk_factors array MUST have at least 3 items. Return ONLY valid JSON."""

    response = ollama_service._call_ollama(prompt)
    parsed = _parse_ai_response(response)
    
    return RiskCalculationResult(
        dimension="claims",
        risk_score=parsed["risk_score"],
        risk_level=parsed["risk_level"],
        risk_factors=parsed["risk_factors"],
        weight_in_overall=0.15,
        recommendations=parsed["recommendations"]
    )


def assess_agent_risk_ai(data: AgentData) -> RiskCalculationResult:
    """AI-powered agent risk assessment."""
    prompt = f"""You are an expert insurance underwriter. Analyze the agent data and provide a risk assessment.

AGENT DATA:
- Agent ID: {data.agent_id}
- Years Licensed: {data.years_licensed}
- Total Policies Sold: {data.total_policies_sold}
- Policies Sold (12mo): {data.policies_sold_12mo}
- Lapse Rate: {data.lapse_rate}%
- Distribution Channel: {data.distribution_channel}
- Compliance Violations: {data.compliance_violations}
- Active Complaints: {data.active_complaints}
- Fraud Investigations: {data.fraud_investigations}
- Confirmed Fraud Cases: {data.fraud_confirmed_cases}
- Agent Risk Score: {data.agent_risk_score}/100

ASSESSMENT CRITERIA:
- High lapse rate (>15%) indicates poor quality
- Compliance violations are serious
- Fraud cases are CRITICAL
- New agents (<2 years) have higher risk

IMPORTANT: You MUST include at least 3-5 risk factors.
Examples: "Years licensed: {data.years_licensed}", "Lapse rate: {data.lapse_rate}%", "Channel: {data.distribution_channel}", "No compliance violations (favorable)"

Provide a JSON response with:
{{
  "risk_score": <0-100>,
  "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "risk_factors": ["factor1", "factor2", "factor3"],
  "recommendations": ["rec1", "rec2"]
}}

CRITICAL: risk_factors array MUST have at least 3 items. Return ONLY valid JSON."""

    response = ollama_service._call_ollama(prompt)
    parsed = _parse_ai_response(response)
    
    return RiskCalculationResult(
        dimension="agent",
        risk_score=parsed["risk_score"],
        risk_level=parsed["risk_level"],
        risk_factors=parsed["risk_factors"],
        weight_in_overall=0.05,
        recommendations=parsed["recommendations"]
    )


def assess_product_risk_ai(data: ProductData) -> RiskCalculationResult:
    """AI-powered product risk assessment."""
    prompt = f"""You are an expert insurance underwriter. Analyze the product data and provide a risk assessment.

PRODUCT DATA:
- Product Type: {data.product_type}
- Coverage Amount: ${data.coverage_amount:,.2f}
- Premium Amount: ${data.premium_amount:,.2f}
- Policy Term: {data.policy_term_years} years
- Underwriting Class: {data.underwriting_class}
- Loading Percentage: {data.loading_percentage}%
- Sum Assured to Income Ratio: {data.sum_assured_to_income_ratio:.1f}x
- Affordability Score: {data.affordability_score}/100
- Loss Ratio Expected: {data.loss_ratio_expected}%
- Profit Margin: {data.profit_margin}%

ASSESSMENT CRITERIA:
- Over-insurance (>10x income) is HIGH risk
- Poor affordability (<60) indicates payment risk
- Substandard/Declined class increases risk
- High loading (>50%) indicates existing issues

IMPORTANT: You MUST include at least 3-5 risk factors.
Examples: "Coverage ratio: {data.sum_assured_to_income_ratio:.1f}x income", "Affordability: {data.affordability_score}/100", "Underwriting class: {data.underwriting_class}"

Provide a JSON response with:
{{
  "risk_score": <0-100>,
  "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "risk_factors": ["factor1", "factor2", "factor3"],
  "recommendations": ["rec1", "rec2"]
}}

CRITICAL: risk_factors array MUST have at least 3 items. Return ONLY valid JSON."""

    response = ollama_service._call_ollama(prompt)
    parsed = _parse_ai_response(response)
    
    return RiskCalculationResult(
        dimension="product",
        risk_score=parsed["risk_score"],
        risk_level=parsed["risk_level"],
        risk_factors=parsed["risk_factors"],
        weight_in_overall=0.05,
        recommendations=parsed["recommendations"]
    )


def _parse_ai_response(response_text: str) -> Dict[str, Any]:
    """
    Parse AI response and extract JSON.
    
    Args:
        response_text: Raw response from Ollama
        
    Returns:
        Parsed dictionary with risk assessment data
    """
    try:
        # Extract JSON from response
        json_str = ollama_service._extract_json(response_text)
        parsed = json.loads(json_str)
        
        # Validate required fields
        if "risk_score" not in parsed:
            parsed["risk_score"] = 50
        if "risk_level" not in parsed:
            parsed["risk_level"] = "MEDIUM"
        if "risk_factors" not in parsed or not parsed["risk_factors"]:
            # If risk_factors is missing or empty, add a default
            parsed["risk_factors"] = ["AI assessment completed - see recommendations for details"]
        if "recommendations" not in parsed:
            parsed["recommendations"] = []
            
        # Ensure risk_level is uppercase
        parsed["risk_level"] = parsed["risk_level"].upper()
        
        return parsed
        
    except Exception as e:
        logger.error(f"Failed to parse AI response: {e}")
        logger.error(f"Response text: {response_text}")
        # Return default values on error
        return {
            "risk_score": 50,
            "risk_level": "MEDIUM",
            "risk_factors": ["AI parsing error - using default assessment"],
            "recommendations": ["Manual review recommended due to AI processing error"]
        }
