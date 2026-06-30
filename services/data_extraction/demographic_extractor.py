"""
Demographic data extractor.

Extracts demographic information from database tables:
- MemberDetails: age, gender, marital_status, nature_of_work
- ProductSubQuestionMapping: smoking, alcohol
- LeadDetails: zip_code, state
"""

from sqlalchemy.orm import Session
from datetime import date
from db.models import MemberDetails, ProductSubQuestionMapping, ProposalDetails, LeadDetails
from data.schemas.demographic_schema import DemographicData


def extract_demographic_data(db: Session, proposal_id: str) -> DemographicData:
    """
    Extract demographic data from database for a given proposal.
    
    Args:
        db: Database session
        proposal_id: Unique proposal identifier
        
    Returns:
        DemographicData object populated from database
        
    Raises:
        ValueError: If proposal or required data not found
    """
    # Get proposal to find policy number
    proposal = db.query(ProposalDetails).filter(
        ProposalDetails.proposal_num == proposal_id
    ).first()
    
    if not proposal:
        raise ValueError(f"Proposal {proposal_id} not found")
    
    # Get member details
    member = db.query(MemberDetails).filter(
        MemberDetails.policy_number == proposal.policy_number
    ).first()
    
    if not member:
        raise ValueError(f"No member data found for proposal {proposal_id}")
    
    # Get lifestyle data from questionnaire
    questionnaire = db.query(ProductSubQuestionMapping).filter(
        ProductSubQuestionMapping.product_id == proposal.product_id
    ).first()
    
    # Get lead details for location
    lead = db.query(LeadDetails).filter(
        LeadDetails.lead_id == proposal.lead_id
    ).first()
    
    # Calculate date of birth from age (approximate)
    current_year = date.today().year
    birth_year = current_year - (member.age or 30)
    dob = date(birth_year, 1, 1)
    
    # Map smoking status
    smoking_map = {
        "Never": "Never",
        "Former": "Former", 
        "Current": "Current",
        "No": "Never",
        "Yes": "Current"
    }
    smoking_status = "Never"
    if questionnaire and questionnaire.smoking:
        smoking_status = smoking_map.get(questionnaire.smoking, "Never")
    
    # Map alcohol consumption
    alcohol_map = {
        "None": "None",
        "Occasional": "Moderate",
        "Regular": "Moderate",
        "Heavy": "Heavy",
        "No": "None",
        "Yes": "Moderate"
    }
    alcohol_consumption = "None"
    if questionnaire and questionnaire.alcohol:
        alcohol_consumption = alcohol_map.get(questionnaire.alcohol, "None")
    
    # Build DemographicData object
    return DemographicData(
        customer_id=member.member_id or f"CUST_{proposal_id}",
        first_name="Customer",  # Not in DB, use placeholder
        last_name=proposal_id,  # Use proposal as identifier
        date_of_birth=dob,
        age=member.age or 30,
        gender=member.gender or "Male",
        smoking_status=smoking_status,
        alcohol_consumption=alcohol_consumption,
        exercise_frequency="Moderate",  # Not in DB, use default
        education_level="Bachelor",  # Not in DB, use default
        occupation=member.nature_of_work or "Other",
        marital_status=member.marital_status or "Single",
        household_size=1,  # Not in DB, use default
        dependents=0,  # Not in DB, use default
        zip_code=lead.zip_code if lead else "00000",
        state=lead.state_province if lead else "Unknown"
    )
