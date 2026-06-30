"""Regional risk calculator."""

from data.schemas.regional_schema import RegionalData
from data.schemas.result_schema import RiskCalculationResult
from .utils import get_risk_level


def calculate_regional_risk(data: RegionalData) -> RiskCalculationResult:
    """
    Calculate regional risk score based on location, healthcare access, and environmental factors.
    
    Risk Factors:
    - Healthcare Access: Hospital distance, specialist availability
    - Environmental: Air quality, natural disasters
    - Socioeconomic: Crime rate, unemployment
    - Cost of Living: Healthcare cost index
    
    Weight in Overall: 10%
    
    Args:
        data: RegionalData containing geographic and regional information
        
    Returns:
        RiskCalculationResult with regional risk assessment
    """
    score = 0
    factors = []
    recommendations = []
    
    # Healthcare access scoring
    if data.nearest_hospital_km > 50:
        score += 25
        factors.append(f"Limited healthcare access (nearest hospital {data.nearest_hospital_km}km)")
        recommendations.append("Consider telemedicine options")
    elif data.nearest_hospital_km > 25:
        score += 15
        factors.append("Moderate healthcare access")
    
    if data.hospitals_within_25km < 2:
        score += 10
        factors.append("Limited hospital options in area")
    
    if not data.specialists_available:
        score += 15
        factors.append("Limited specialist availability")
        recommendations.append("May require travel for specialized care")
    
    # Environmental factors
    if data.air_quality_index > 150:
        score += 20
        factors.append(f"Poor air quality (AQI: {data.air_quality_index})")
        recommendations.append("Assess respiratory health risks")
    elif data.air_quality_index > 100:
        score += 10
        factors.append(f"Moderate air quality (AQI: {data.air_quality_index})")
    
    if data.natural_disaster_zone:
        score += 15
        factors.append("Located in natural disaster zone")
        if data.disaster_type:
            factors.append(f"Disaster type: {data.disaster_type}")
        recommendations.append("Verify disaster preparedness")
    
    # Socioeconomic indicators
    if data.crime_rate_per_1000 > 30:
        score += 15
        factors.append(f"High crime rate ({data.crime_rate_per_1000} per 1000)")
        recommendations.append("Consider personal safety risks")
    elif data.crime_rate_per_1000 > 20:
        score += 8
        factors.append(f"Elevated crime rate ({data.crime_rate_per_1000} per 1000)")
    
    if data.unemployment_rate > 10:
        score += 12
        factors.append(f"High unemployment rate ({data.unemployment_rate}%)")
    elif data.unemployment_rate > 7:
        score += 6
        factors.append(f"Elevated unemployment rate ({data.unemployment_rate}%)")
    
    # Healthcare cost index
    if data.healthcare_cost_index > 150:
        score += 10
        factors.append(f"High healthcare costs (index: {data.healthcare_cost_index})")
        recommendations.append("Consider cost impact on affordability")
    elif data.healthcare_cost_index > 125:
        score += 5
        factors.append(f"Above average healthcare costs (index: {data.healthcare_cost_index})")
    
    # Cap score at 100
    final_score = min(score, 100)
    
    # Add general recommendations if no specific ones
    if not recommendations:
        recommendations.append("Favorable regional risk profile")
        recommendations.append("No additional regional-related requirements")
    
    return RiskCalculationResult(
        dimension="regional",
        risk_score=final_score,
        risk_level=get_risk_level(final_score),
        risk_factors=factors,
        weight_in_overall=0.10,
        recommendations=recommendations
    )
