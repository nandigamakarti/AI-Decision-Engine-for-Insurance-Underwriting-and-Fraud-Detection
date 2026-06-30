"""Demographic risk calculator."""

from data.schemas.demographic_schema import DemographicData
from data.schemas.result_schema import RiskCalculationResult
from .utils import get_risk_level


def calculate_demographic_risk(data: DemographicData) -> RiskCalculationResult:
    """
    Calculate demographic risk score based on age, lifestyle, and socioeconomic factors.
    
    Risk Factors:
    - Age: 18-30 (LOW), 31-50 (MEDIUM), 51-70 (HIGH), 70+ (CRITICAL)
    - Smoking: Never (0), Former (+15), Current (+40)
    - Alcohol: None (0), Moderate (+5), Heavy (+20)
    - Exercise: Active (0), Moderate (+5), Light (+10), Sedentary (+15)
    
    Weight in Overall: 15%
    
    Args:
        data: DemographicData containing customer demographic information
        
    Returns:
        RiskCalculationResult with demographic risk assessment
    """
    score = 0
    factors = []
    recommendations = []
    
    # Age scoring
    if data.age < 30:
        score += 10
        factors.append(f"Age {data.age} (low risk)")
    elif data.age < 50:
        score += 25
        factors.append(f"Age {data.age} (moderate risk)")
    elif data.age < 70:
        score += 50
        factors.append(f"Age {data.age} (elevated risk)")
        recommendations.append("Request comprehensive health questionnaire")
    else:
        score += 70
        factors.append(f"Advanced age ({data.age})")
        recommendations.append("Request comprehensive medical examination")
        recommendations.append("Consider age-specific underwriting guidelines")
    
    # Smoking status
    if data.smoking_status == "Current":
        score += 40
        factors.append("Current smoker")
        recommendations.append("Strongly recommend smoking cessation program")
        recommendations.append("Apply smoker premium rates")
    elif data.smoking_status == "Former":
        score += 15
        factors.append("Former smoker")
        recommendations.append("Verify smoking cessation date and duration")
    else:
        factors.append("Non-smoker (favorable)")
    
    # Alcohol consumption
    if data.alcohol_consumption == "Heavy":
        score += 20
        factors.append("Heavy alcohol consumption")
        recommendations.append("Assess alcohol-related health risks")
    elif data.alcohol_consumption == "Moderate":
        score += 5
        factors.append("Moderate alcohol consumption")
    else:
        factors.append("No/minimal alcohol consumption (favorable)")
    
    # Exercise frequency
    if data.exercise_frequency == "Sedentary":
        score += 15
        factors.append("Sedentary lifestyle")
        recommendations.append("Recommend lifestyle modification counseling")
    elif data.exercise_frequency == "Light":
        score += 10
        factors.append("Limited physical activity")
    elif data.exercise_frequency == "Moderate":
        score += 5
        factors.append("Moderate physical activity")
    else:
        factors.append("Active lifestyle (favorable)")
    
    # Cap score at 100
    final_score = min(score, 100)
    
    # Add general recommendations if no specific ones
    if not recommendations:
        recommendations.append("Standard demographic risk profile")
        recommendations.append("No additional demographic-related requirements")
    
    return RiskCalculationResult(
        dimension="demographic",
        risk_score=final_score,
        risk_level=get_risk_level(final_score),
        risk_factors=factors,
        weight_in_overall=0.15,
        recommendations=recommendations
    )
