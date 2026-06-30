"""
Claims data extractor.

Extracts claims history information from database tables:
- ClaimDetails: claims frequency, amounts, status
- BlackListedHospitals: fraud indicators
- MemberDetails: member linkage
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from db.models import ClaimDetails, BlackListedHospitals, MemberDetails, ProposalDetails
from data.schemas.claims_schema import ClaimsData


def extract_claims_data(db: Session, proposal_id: str) -> ClaimsData:
    """
    Extract claims data from database for a given proposal.
    
    Args:
        db: Database session
        proposal_id: Unique proposal identifier
        
    Returns:
        ClaimsData object populated from database
        
    Raises:
        ValueError: If proposal not found
    """
    # Get proposal
    proposal = db.query(ProposalDetails).filter(
        ProposalDetails.proposal_num == proposal_id
    ).first()
    
    if not proposal:
        raise ValueError(f"Proposal {proposal_id} not found")
    
    # Get member details
    member = db.query(MemberDetails).filter(
        MemberDetails.policy_number == proposal.policy_number
    ).first()
    
    # Get all claims for this member
    claims = []
    if member:
        claims = db.query(ClaimDetails).filter(
            ClaimDetails.member_id == member.member_id
        ).all()
    
    # Calculate claims metrics
    total_claims = len(claims)
    total_claims_amount = sum(float(c.claimed_amount or 0) for c in claims)
    average_claim_amount = total_claims_amount / total_claims if total_claims > 0 else 0
    highest_claim_amount = max((float(c.claimed_amount or 0) for c in claims), default=0)
    
    # Calculate claims in last 12 and 36 months
    now = datetime.now()
    twelve_months_ago = now - timedelta(days=365)
    thirty_six_months_ago = now - timedelta(days=365 * 3)
    
    claims_last_12mo = sum(
        1 for c in claims 
        if c.reported_date_time and c.reported_date_time >= twelve_months_ago
    )
    
    claims_last_36mo = sum(
        1 for c in claims 
        if c.reported_date_time and c.reported_date_time >= thirty_six_months_ago
    )
    
    # Determine claim frequency trend
    if claims_last_12mo > claims_last_36mo / 3:
        claim_frequency_trend = "Increasing"
    elif claims_last_12mo < claims_last_36mo / 4:
        claim_frequency_trend = "Decreasing"
    else:
        claim_frequency_trend = "Stable"
    
    # Build recent claims list (last 5 claims)
    from data.schemas.claims_schema import Claim
    recent_claims = []
    for claim in sorted(claims, key=lambda x: x.reported_date_time or datetime.min, reverse=True)[:5]:
        recent_claims.append(Claim(
            claim_id=claim.claim_number or "UNKNOWN",
            claim_date=claim.reported_date_time.date() if claim.reported_date_time else date.today(),
            claim_type=claim.claim_type or "Medical",
            claim_amount=float(claim.claimed_amount or 0),
            approved_amount=float(claim.approved_amount or 0),
            status=claim.claim_status or "Pending"
        ))
    
    # Check for blacklisted hospitals
    blacklisted_hospital_involved = False
    for claim in claims:
        if claim.hospital_name:
            blacklisted = db.query(BlackListedHospitals).filter(
                BlackListedHospitals.name_of_hospital.ilike(f"%{claim.hospital_name}%")
            ).first()
            if blacklisted:
                blacklisted_hospital_involved = True
                break
    
    # Calculate fraud score (0-100)
    fraud_score = 0
    if blacklisted_hospital_involved:
        fraud_score += 50
    if claims_last_12mo > 3:
        fraud_score += 20
    if any(c.claim_status == "Rejected" and "fraud" in (c.rejection_reason or "").lower() for c in claims):
        fraud_score += 30
    
    fraud_score = min(fraud_score, 100)
    
    # Build ClaimsData object
    return ClaimsData(
        customer_id=f"CUST_{proposal_id}",
        total_claims_count=total_claims,
        claims_last_12mo=claims_last_12mo,
        claims_last_36mo=claims_last_36mo,
        total_claims_amount=total_claims_amount,
        average_claim_amount=average_claim_amount,
        highest_single_claim=highest_claim_amount,
        claim_frequency_trend=claim_frequency_trend,
        recent_claims=recent_claims,
        suspicious_patterns_detected=blacklisted_hospital_involved,
        fraud_score=fraud_score
    )
