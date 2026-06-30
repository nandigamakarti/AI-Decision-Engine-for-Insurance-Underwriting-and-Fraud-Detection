"""
Regional data extractor.

Extracts regional/geographic information from database tables:
- LeadDetails: city, state, zip_code, zone
- HospitalMaster: network hospitals proximity
- BlackListedHospitals: blacklisted hospitals proximity
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import LeadDetails, HospitalMaster, BlackListedHospitals, ProposalDetails
from data.schemas.regional_schema import RegionalData


def extract_regional_data(db: Session, proposal_id: str) -> RegionalData:
    """
    Extract regional data from database for a given proposal.
    
    Args:
        db: Database session
        proposal_id: Unique proposal identifier
        
    Returns:
        RegionalData object populated from database
        
    Raises:
        ValueError: If proposal not found
    """
    # Get proposal
    proposal = db.query(ProposalDetails).filter(
        ProposalDetails.proposal_num == proposal_id
    ).first()
    
    if not proposal:
        raise ValueError(f"Proposal {proposal_id} not found")
    
    # Get lead details
    lead = db.query(LeadDetails).filter(
        LeadDetails.lead_id == proposal.lead_id
    ).first()
    
    if not lead:
        raise ValueError(f"No lead data found for proposal {proposal_id}")
    
    # Count network hospitals in the same pincode
    network_hospitals = db.query(func.count(HospitalMaster.id)).filter(
        HospitalMaster.pincode == lead.zip_code
    ).scalar() or 0
    
    # Count blacklisted hospitals in the same pincode
    blacklisted_hospitals = db.query(func.count(BlackListedHospitals.id)).filter(
        BlackListedHospitals.pincode == int(lead.zip_code) if lead.zip_code.isdigit() else 0
    ).scalar() or 0
    
    # Calculate hospital distance (estimate based on availability)
    nearest_hospital_km = 5.0 if network_hospitals > 0 else 20.0
    
    # Count hospitals within 25km (estimate based on total in pincode)
    hospitals_within_25km = network_hospitals
    
    # Determine healthcare access quality
    if network_hospitals >= 3:
        healthcare_access_quality = "Excellent"
        specialists_available = True
    elif network_hospitals >= 1:
        healthcare_access_quality = "Good"
        specialists_available = True
    else:
        healthcare_access_quality = "Limited"
        specialists_available = False
    
    # Map zone to natural disaster zone (boolean)
    high_risk_zones = ["East", "South"]
    natural_disaster_zone = lead.zone in high_risk_zones if lead.zone else False
    
    # Build RegionalData object with all required fields
    return RegionalData(
        customer_id=f"CUST_{proposal_id}",
        zip_code=lead.zip_code or "00000",
        city=lead.city or "Unknown",
        state=lead.state_province or "Unknown",
        nearest_hospital_km=nearest_hospital_km,
        hospitals_within_25km=hospitals_within_25km,
        specialists_available=specialists_available,
        healthcare_access_quality=healthcare_access_quality,
        air_quality_index=50,  # Not in DB, use moderate default
        natural_disaster_zone=natural_disaster_zone,
        crime_rate_per_1000=30.0,  # Not in DB, use low default
        median_income_area=50000.0,  # Not in DB, use default
        unemployment_rate=5.0,  # Not in DB, use default
        healthcare_cost_index=100  # Not in DB, use baseline
    )
