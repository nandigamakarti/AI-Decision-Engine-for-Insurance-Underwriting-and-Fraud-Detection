"""
Helper endpoint to fetch available proposal IDs from database.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from db import get_db
from db.models import (
    ProposalDetails, MemberDetails, KYCDetails, ClaimDetails,
    AgentDetails, ProductDetails, LeadDetails, ChronicDiseaseDetails,
    AgentRiskScores, AnnualClubPerformance
)
from services.data_extraction.regional_extractor import extract_regional_data

router = APIRouter(prefix="/api/proposals", tags=["Proposals"])


class ProposalDetailedSummary(BaseModel):
    """Detailed summary of a proposal showing available data."""
    proposal_num: str
    policy_number: Optional[str] = None
    agent_code: Optional[str] = None
    product_id: Optional[int] = None
    sum_insured: Optional[float] = None
    annual_income: Optional[float] = None
    
    # Data availability indicators
    has_member_data: bool = False
    member_age: Optional[int] = None
    member_gender: Optional[str] = None
    
    has_kyc_data: bool = False
    kyc_status: Optional[str] = None
    
    has_claims_data: bool = False
    claims_count: int = 0
    
    has_agent_data: bool = False
    agent_category: Optional[str] = None
    
    has_product_data: bool = False
    product_name: Optional[str] = None
    
    has_lead_data: bool = False
    lead_city: Optional[str] = None
    lead_state: Optional[str] = None
    
    has_chronic_disease_data: bool = False
    
    class Config:
        from_attributes = True


@router.get(
    "/",
    response_model=List[ProposalDetailedSummary],
    summary="List All Proposals with Data Details",
    description="Get detailed list of all proposals showing what data is available for each"
)
async def list_proposals(db: Session = Depends(get_db)) -> List[ProposalDetailedSummary]:
    """
    Retrieve all proposals with detailed information about available data.
    
    This endpoint shows you what data exists for each proposal, making it easier
    to select a proposal for testing risk assessment APIs.
    
    Returns:
        List of detailed proposal summaries with data availability indicators
    """
    proposals = db.query(ProposalDetails).limit(100).all()
    
    result = []
    for proposal in proposals:
        # Check member data
        member = db.query(MemberDetails).filter(
            MemberDetails.policy_number == proposal.policy_number
        ).first()
        
        # Check KYC data
        kyc = db.query(KYCDetails).filter(
            KYCDetails.proposal_num == proposal.proposal_num
        ).first()
        
        # Check claims data
        claims_count = 0
        if member:
            claims_count = db.query(ClaimDetails).filter(
                ClaimDetails.member_id == member.member_id
            ).count()
        
        # Check agent data
        agent = None
        if proposal.agent_code:
            agent = db.query(AgentDetails).filter(
                AgentDetails.agent_code == proposal.agent_code
            ).first()
        
        # Check product data
        product = None
        if proposal.product_id:
            product = db.query(ProductDetails).filter(
                ProductDetails.product_id == proposal.product_id
            ).first()
        
        # Check lead data
        lead = None
        if proposal.lead_id:
            lead = db.query(LeadDetails).filter(
                LeadDetails.lead_id == proposal.lead_id
            ).first()
        
        # Check chronic disease data
        chronic = db.query(ChronicDiseaseDetails).filter(
            ChronicDiseaseDetails.proposal_number == proposal.proposal_num
        ).first()
        
        # Build summary
        summary = ProposalDetailedSummary(
            proposal_num=proposal.proposal_num,
            policy_number=proposal.policy_number,
            agent_code=proposal.agent_code,
            product_id=proposal.product_id,
            sum_insured=float(proposal.sum_insured) if proposal.sum_insured else None,
            annual_income=float(proposal.annual_income) if proposal.annual_income else None,
            
            has_member_data=member is not None,
            member_age=member.age if member else None,
            member_gender=member.gender if member else None,
            
            has_kyc_data=kyc is not None,
            kyc_status=kyc.kyc_status if kyc else None,
            
            has_claims_data=claims_count > 0,
            claims_count=claims_count,
            
            has_agent_data=agent is not None,
            agent_category=agent.agent_category if agent else None,
            
            has_product_data=product is not None,
            product_name=product.product_name if product else None,
            
            has_lead_data=lead is not None,
            lead_city=lead.city if lead else None,
            lead_state=lead.state_province if lead else None,
            
            has_chronic_disease_data=chronic is not None
        )
        
        result.append(summary)
    
    return result


@router.get(
    "/{proposal_num}",
    summary="Get Complete Proposal Data",
    description="Retrieve all data for a specific proposal that will be used in risk assessment"
)
async def get_proposal_data(proposal_num: str, db: Session = Depends(get_db)):
    """
    Get complete data for a specific proposal.
    
    This endpoint shows you ALL the data that will be extracted and used
    when you call the risk assessment APIs with this proposal_num.
    
    Args:
        proposal_num: The proposal number (e.g., "PROP001")
        
    Returns:
        Complete proposal data including all related tables
    """
    # Get proposal
    proposal = db.query(ProposalDetails).filter(
        ProposalDetails.proposal_num == proposal_num
    ).first()
    
    if not proposal:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_num} not found")
    
    # Get all related data
    member = db.query(MemberDetails).filter(
        MemberDetails.policy_number == proposal.policy_number
    ).first()
    
    kyc = db.query(KYCDetails).filter(
        KYCDetails.proposal_num == proposal_num
    ).first()
    
    product = None
    if proposal.product_id:
        product = db.query(ProductDetails).filter(
            ProductDetails.product_id == proposal.product_id
        ).first()
    
    agent = None
    agent_risk = None
    agent_perf = None
    if proposal.agent_code:
        agent = db.query(AgentDetails).filter(
            AgentDetails.agent_code == proposal.agent_code
        ).first()
        agent_risk = db.query(AgentRiskScores).filter(
            AgentRiskScores.agent_code == proposal.agent_code
        ).first()
        agent_perf = db.query(AnnualClubPerformance).filter(
            AnnualClubPerformance.agent_code == proposal.agent_code
        ).first()
    
    lead = None
    if proposal.lead_id:
        lead = db.query(LeadDetails).filter(
            LeadDetails.lead_id == proposal.lead_id
        ).first()
    
    chronic = db.query(ChronicDiseaseDetails).filter(
        ChronicDiseaseDetails.proposal_number == proposal_num
    ).first()
    
    claims = []
    if member:
        claims = db.query(ClaimDetails).filter(
            ClaimDetails.member_id == member.member_id
        ).all()
        
    regional_data = None
    try:
        regional_data = extract_regional_data(db, proposal_num)
    except Exception:
        pass
    
    # Build comprehensive response
    return {
        "proposal_num": proposal_num,
        "status": "found",
        
        "proposal_details": {
            "proposal_num": proposal.proposal_num,
            "policy_number": proposal.policy_number,
            "lead_id": proposal.lead_id,
            "agent_code": proposal.agent_code,
            "product_id": proposal.product_id,
            "annual_income": float(proposal.annual_income) if proposal.annual_income else None,
            "sum_insured": float(proposal.sum_insured) if proposal.sum_insured else None,
            "proposer_pan": proposal.proposer_pan,
            "created_date": proposal.created_date.isoformat() if proposal.created_date else None
        } if proposal else None,
        
        "member_details": {
            "member_id": member.member_id,
            "age": member.age,
            "gender": member.gender,
            "height": member.height,
            "weight": member.weight,
            "nature_of_work": member.nature_of_work,
            "marital_status": member.marital_status
        } if member else None,
        
        "kyc_details": {
            "risk_level": kyc.risk_level,
            "aml_check": kyc.aml_check,
            "kyc_status": kyc.kyc_status,
            "face_match": kyc.if_face_match
        } if kyc else None,
        
        "product_details": {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "product_code": product.product_code,
            "pre_existing_waiting_period": product.pre_existing_waiting_period,
            "co_pay_percentage": product.co_pay_percentage,
            "key_features": product.key_features
        } if product else None,
        
        "agent_details": {
            "agent_code": agent.agent_code,
            "agent_category": agent.agent_category,
            "channel": agent.channel,
            "created_on": agent.created_on.isoformat() if agent.created_on else None,
            "loss_ratio": f"{agent_risk.loss_ratio}%" if agent_risk and agent_risk.loss_ratio is not None else (agent_perf.loss_ratio if agent_perf else "0.0%"),
            "lapse_rate": f"{agent_risk.lapse_rate}%" if agent_risk and agent_risk.lapse_rate is not None else "0.0%",
            "vintage_years": int(agent_risk.vintage_years) if agent_risk and agent_risk.vintage_years is not None else 5,
            "compliance_flags": ["High Lapse Warning", "Questionable PED reporting logs"] if (agent_risk and agent_risk.lapse_rate and agent_risk.lapse_rate > 20) else []
        } if agent else None,
        
        "lead_details": {
            "lead_id": lead.lead_id,
            "city": lead.city,
            "state": lead.state_province,
            "zip_code": lead.zip_code,
            "zone": lead.zone
        } if lead else None,
        
        "chronic_disease_details": {
            "is_diabetes": chronic.is_diabetes,
            "diabetes_remark": chronic.diabetes_remark,
            "is_hypertension": chronic.is_hypertension,
            "is_asthma": chronic.is_asthma,
            "asthma_remark": chronic.asthma_remark,
            "is_hyperlipidemia": chronic.is_hyperlipidemia
        } if chronic else None,
        
        "regional_details": {
            "hospitalDistance": float(regional_data.nearest_hospital_km) if regional_data else 5.0,
            "aqi": int(regional_data.air_quality_index) if regional_data else 50,
            "naturalDisasters": "High Risk Zone" if regional_data and regional_data.natural_disaster_zone else "Low Index",
            "crimeRate": f"{regional_data.crime_rate_per_1000}/1000" if regional_data else "Low"
        } if regional_data else None,
        
        "claims_history": [
            {
                "claim_number": claim.claim_number,
                "claimed_amount": float(claim.claimed_amount) if claim.claimed_amount else None,
                "approved_amount": float(claim.approved_amount) if claim.approved_amount else None,
                "claim_status": claim.claim_status,
                "hospital_name": claim.hospital_name,
                "claim_type": claim.claim_type,
                "reported_date": claim.reported_date_time.isoformat() if claim.reported_date_time else None
            }
            for claim in claims
        ] if claims else [],
        
        "data_completeness": {
            "has_proposal": proposal is not None,
            "has_member": member is not None,
            "has_kyc": kyc is not None,
            "has_product": product is not None,
            "has_agent": agent is not None,
            "has_lead": lead is not None,
            "has_chronic_disease": chronic is not None,
            "has_claims": len(claims) > 0,
            "claims_count": len(claims)
        },
        
        "usage_instructions": {
            "message": f"Use this proposal_num in risk assessment APIs",
            "example_request": {
                "proposal_id": proposal_num
            }
        }
    }

