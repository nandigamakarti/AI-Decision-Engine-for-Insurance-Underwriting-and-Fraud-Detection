"""
Medical data extractor.

Extracts medical information from database tables:
- ChronicDiseaseDetails: pre-existing conditions
- ProductSubQuestionMapping: medications, surgeries
- MemberDetails: height, weight (for BMI calculation)
"""

from sqlalchemy.orm import Session
from datetime import date, datetime
from db.models import ChronicDiseaseDetails, ProductSubQuestionMapping, MemberDetails, ProposalDetails
from data.schemas.medical_schema import MedicalData, MedicalCondition, Medication, Procedure


def parse_height_weight(height_str: str, weight_str: str) -> tuple[float, float]:
    """
    Parse height and weight strings to numeric values.
    
    Args:
        height_str: Height string (e.g., "175 cm")
        weight_str: Weight string (e.g., "75 kg")
        
    Returns:
        Tuple of (height_cm, weight_kg)
    """
    try:
        # Extract numeric values
        height_cm = float(''.join(filter(lambda x: x.isdigit() or x == '.', height_str or "170")))
        weight_kg = float(''.join(filter(lambda x: x.isdigit() or x == '.', weight_str or "70")))
        
        # Ensure reasonable values
        if height_cm < 50 or height_cm > 250:
            height_cm = 170.0
        if weight_kg < 20 or weight_kg > 300:
            weight_kg = 70.0
            
        return height_cm, weight_kg
    except:
        return 170.0, 70.0  # Default values


def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculate BMI from height and weight."""
    try:
        height_m = height_cm / 100
        if height_m > 0:
            bmi = weight_kg / (height_m ** 2)
            return round(bmi, 1)
        return 22.0
    except:
        return 22.0


def extract_medical_data(db: Session, proposal_id: str) -> MedicalData:
    """
    Extract medical data from database for a given proposal.
    
    Args:
        db: Database session
        proposal_id: Unique proposal identifier
        
    Returns:
        MedicalData object populated from database
        
    Raises:
        ValueError: If proposal not found
    """
    # Get proposal
    proposal = db.query(ProposalDetails).filter(
        ProposalDetails.proposal_num == proposal_id
    ).first()
    
    if not proposal:
        raise ValueError(f"Proposal {proposal_id} not found")
    
    # Get member details for height/weight
    member = db.query(MemberDetails).filter(
        MemberDetails.policy_number == proposal.policy_number
    ).first()
    
    # Get chronic disease details
    chronic = db.query(ChronicDiseaseDetails).filter(
        ChronicDiseaseDetails.proposal_number == proposal_id
    ).first()
    
    # Get questionnaire for medications and surgeries
    questionnaire = db.query(ProductSubQuestionMapping).filter(
        ProductSubQuestionMapping.product_id == proposal.product_id
    ).first()
    
    # Build conditions list (MedicalCondition objects)
    conditions = []
    if chronic:
        if chronic.is_diabetes:
            conditions.append(MedicalCondition(
                icd10_code="E11.9",
                description="Type 2 Diabetes Mellitus" + (f" - {chronic.diabetes_remark}" if chronic.diabetes_remark else ""),
                diagnosed_date=date(2020, 1, 1),  # Default date, not in DB
                treatment_status="Active"
            ))
        if chronic.is_hypertension:
            conditions.append(MedicalCondition(
                icd10_code="I10",
                description="Essential Hypertension",
                diagnosed_date=date(2020, 1, 1),
                treatment_status="Controlled"
            ))
        if chronic.is_asthma:
            conditions.append(MedicalCondition(
                icd10_code="J45.9",
                description="Asthma" + (f" - {chronic.asthma_remark}" if chronic.asthma_remark else ""),
                diagnosed_date=date(2020, 1, 1),
                treatment_status="Active"
            ))
        if chronic.is_hyperlipidemia:
            conditions.append(MedicalCondition(
                icd10_code="E78.5",
                description="Hyperlipidemia",
                diagnosed_date=date(2020, 1, 1),
                treatment_status="Controlled"
            ))
    
    # Build medications list (Medication objects)
    medications = []
    if questionnaire and questionnaire.medicine_details:
        medications.append(Medication(
            ndc_code="00000-0000-00",  # Generic, actual NDC not in DB
            name=questionnaire.medicine_details[:50] if questionnaire.medicine_details else "Medication",
            dosage=questionnaire.medication_type or "As prescribed",
            frequency=questionnaire.duration or "Daily"
        ))
    
    # Build procedures list (Procedure objects)
    procedures = []
    if questionnaire and questionnaire.name_of_surgery:
        procedures.append(Procedure(
            cpt_code="00000",  # Generic, actual CPT not in DB
            description=questionnaire.name_of_surgery,
            procedure_date=datetime.strptime(questionnaire.date_of_diagnosis, "%Y-%m-%d").date() 
                          if questionnaire.date_of_diagnosis else date(2020, 1, 1)
        ))
    
    # Parse height and weight
    height_cm, weight_kg = parse_height_weight(
        member.height if member else None,
        member.weight if member else None
    )
    
    # Calculate BMI
    bmi = calculate_bmi(height_cm, weight_kg)
    
    # Build MedicalData object
    return MedicalData(
        customer_id=f"CUST_{proposal_id}",
        conditions=conditions,
        current_medications=medications,
        past_procedures=procedures,
        height_cm=height_cm,
        weight_kg=weight_kg,
        bmi=bmi,
        blood_pressure_systolic=120,  # Not in DB, use normal default
        blood_pressure_diastolic=80,  # Not in DB, use normal default
        family_history_cancer=False,  # Not in DB, assume false
        family_history_heart_disease=False,  # Not in DB, assume false
        family_history_diabetes=False  # Not in DB, assume false
    )
