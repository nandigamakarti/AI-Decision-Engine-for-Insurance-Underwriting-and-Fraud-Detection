"""Medical risk calculator."""

from typing import List
from data.schemas.medical_schema import MedicalData
from data.schemas.result_schema import RiskCalculationResult
from .utils import get_risk_level


def calculate_medical_risk(data: MedicalData) -> RiskCalculationResult:
    """
    Calculate medical risk score based on conditions, medications, vitals, and family history.
    
    Risk Factors:
    - Pre-existing Conditions: ICD-10 codes with risk weights
    - Current Medications: NDC codes indicating chronic conditions
    - Past Procedures: CPT codes for surgical history
    - Vitals: BMI, blood pressure
    - Family History: Cancer, heart disease, diabetes
    
    Weight in Overall: 30% (HIGHEST - medical is most critical)
    
    Note: This implementation uses basic scoring. Integration with ICD-10/NDC/CPT
    databases from Developer 1 will enhance accuracy.
    
    Args:
        data: MedicalData containing customer medical information
        
    Returns:
        RiskCalculationResult with medical risk assessment
    """
    score = 0
    factors = []
    recommendations = []
    
    # Pre-existing conditions analysis
    if len(data.conditions) > 0:
        for condition in data.conditions:
            # Basic scoring by treatment status
            if condition.treatment_status == "Active":
                score += 20
                factors.append(f"Active condition: {condition.description}")
                recommendations.append(f"Request current treatment details for {condition.description}")
            elif condition.treatment_status == "Controlled":
                score += 10
                factors.append(f"Controlled condition: {condition.description}")
            elif condition.treatment_status == "Resolved":
                score += 3
                factors.append(f"Resolved condition: {condition.description}")
            
            # TODO: Integrate with ICD-10 risk weight database from Dev 1
            # Example: score += ICD10_CODES[condition.icd10_code]["risk_weight"]
        
        # Multiple conditions increase risk
        if len(data.conditions) > 3:
            score += 15
            factors.append(f"Multiple pre-existing conditions ({len(data.conditions)})")
            recommendations.append("Request comprehensive medical history")
    
    # Current medications analysis
    if len(data.current_medications) > 0:
        medication_count = len(data.current_medications)
        
        if medication_count > 5:
            score += 20
            factors.append(f"Multiple medications ({medication_count})")
            recommendations.append("Review medication list for interactions")
        elif medication_count > 3:
            score += 12
            factors.append(f"Several medications ({medication_count})")
        elif medication_count > 0:
            score += 5
            factors.append(f"On medication ({medication_count})")
        
        # TODO: Integrate with NDC medication database from Dev 1
        # for medication in data.current_medications:
        #     score += NDC_CODES[medication.ndc_code]["risk_weight"]
    
    # Past procedures analysis
    if len(data.past_procedures) > 0:
        for procedure in data.past_procedures:
            score += 8
            factors.append(f"Past procedure: {procedure.description}")
        
        if len(data.past_procedures) > 3:
            score += 10
            factors.append(f"Multiple surgical procedures ({len(data.past_procedures)})")
            recommendations.append("Request surgical records and outcomes")
        
        # TODO: Integrate with CPT procedure database from Dev 1
        # for procedure in data.past_procedures:
        #     score += CPT_CODES[procedure.cpt_code]["risk_weight"]
    
    # BMI analysis (Body Mass Index)
    if data.bmi < 18.5:
        score += 20
        factors.append(f"Underweight (BMI: {data.bmi:.1f})")
        recommendations.append("Assess nutritional status and underlying causes")
    elif data.bmi >= 30 and data.bmi < 35:
        score += 20
        factors.append(f"Obese (BMI: {data.bmi:.1f})")
        recommendations.append("Assess obesity-related health risks")
    elif data.bmi >= 35:
        score += 35
        factors.append(f"Severely obese (BMI: {data.bmi:.1f})")
        recommendations.append("CRITICAL: Comprehensive health assessment required")
        recommendations.append("Screen for diabetes, heart disease, sleep apnea")
    elif data.bmi >= 25:
        score += 10
        factors.append(f"Overweight (BMI: {data.bmi:.1f})")
    
    # Blood pressure analysis
    systolic = data.blood_pressure_systolic
    diastolic = data.blood_pressure_diastolic
    
    # Hypertension staging
    if systolic >= 180 or diastolic >= 120:
        score += 40
        factors.append(f"Hypertensive crisis (BP: {systolic}/{diastolic})")
        recommendations.append("CRITICAL: Immediate medical evaluation required")
        recommendations.append("Defer underwriting until BP controlled")
    elif systolic >= 140 or diastolic >= 90:
        score += 25
        factors.append(f"Stage 2 hypertension (BP: {systolic}/{diastolic})")
        recommendations.append("Request treatment plan and medication compliance")
    elif systolic >= 130 or diastolic >= 80:
        score += 15
        factors.append(f"Stage 1 hypertension (BP: {systolic}/{diastolic})")
        recommendations.append("Verify BP monitoring and management")
    elif systolic >= 120:
        score += 8
        factors.append(f"Elevated blood pressure (BP: {systolic}/{diastolic})")
    
    # Hypotension
    if systolic < 90 or diastolic < 60:
        score += 12
        factors.append(f"Low blood pressure (BP: {systolic}/{diastolic})")
        recommendations.append("Assess for underlying causes of hypotension")
    
    # Family history analysis
    family_history_count = 0
    
    if data.family_history_cancer:
        score += 12
        family_history_count += 1
        factors.append("Family history of cancer")
        recommendations.append("Recommend cancer screening appropriate for age")
    
    if data.family_history_heart_disease:
        score += 15
        family_history_count += 1
        factors.append("Family history of heart disease")
        recommendations.append("Recommend cardiac risk assessment")
    
    if data.family_history_diabetes:
        score += 10
        family_history_count += 1
        factors.append("Family history of diabetes")
        recommendations.append("Recommend diabetes screening (HbA1c, fasting glucose)")
    
    # Multiple family history factors compound risk
    if family_history_count >= 2:
        score += 10
        factors.append(f"Multiple family history risk factors ({family_history_count})")
    
    # Cap score at 100
    final_score = min(score, 100)
    
    # Add general recommendations if no specific ones
    if not recommendations:
        recommendations.append("Standard medical risk profile")
        recommendations.append("No additional medical requirements")
    else:
        # Add general medical exam recommendation for high-risk cases
        if final_score >= 50:
            recommendations.insert(0, "Request comprehensive medical examination")
    
    return RiskCalculationResult(
        dimension="medical",
        risk_score=final_score,
        risk_level=get_risk_level(final_score),
        risk_factors=factors,
        weight_in_overall=0.30,  # HIGHEST weight
        recommendations=recommendations
    )
