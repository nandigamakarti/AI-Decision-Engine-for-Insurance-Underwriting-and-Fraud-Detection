"""
Financial data extractor.

Extracts financial information from database tables:
- ProposalDetails: annual_income
- KYCDetails: risk_level (maps to credit score), kyc_status
- PaymentDetails: payment_status, payment history
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import ProposalDetails, KYCDetails, PaymentDetails
from data.schemas.financial_schema import FinancialData


def extract_financial_data(db: Session, proposal_id: str) -> FinancialData:
    """
    Extract financial data from database for a given proposal.
    
    Args:
        db: Database session
        proposal_id: Unique proposal identifier
        
    Returns:
        FinancialData object populated from database
        
    Raises:
        ValueError: If proposal not found
    """
    # Get proposal details
    proposal = db.query(ProposalDetails).filter(
        ProposalDetails.proposal_num == proposal_id
    ).first()
    
    if not proposal:
        raise ValueError(f"Proposal {proposal_id} not found")
    
    # Get KYC details
    kyc = db.query(KYCDetails).filter(
        KYCDetails.proposal_num == proposal_id
    ).first()
    
    # Get payment details
    payments = db.query(PaymentDetails).filter(
        PaymentDetails.proposal_id == proposal_id
    ).all()
    
    # Map KYC risk level to credit score
    credit_score_map = {
        "Low": 750,
        "Medium": 650,
        "High": 550
    }
    credit_score = 700  # Default
    if kyc and kyc.risk_level:
        credit_score = credit_score_map.get(kyc.risk_level, 700)
    
    # Determine income stability based on nature of work
    income_stability = "Stable"  # Default assumption
    
    # Map employment status
    employment_status = "Employed"  # Default
    
    # Calculate debt-to-income ratio (estimate)
    annual_income = float(proposal.annual_income) if proposal.annual_income else 1000000.0
    sum_insured = float(proposal.sum_insured) if proposal.sum_insured else 500000.0
    
    # Estimate total debt as 30% of sum insured
    total_debt = sum_insured * 0.3
    debt_to_income_ratio = total_debt / annual_income if annual_income > 0 else 0.5
    
    # Calculate liquid assets (estimate as 10% of annual income)
    liquid_assets = annual_income * 0.1
    total_assets = annual_income * 2  # Rough estimate
    
    # Check for late payments
    late_payments = 0
    if payments:
        late_payments = sum(1 for p in payments if p.payment_status == "Failed")
    
    # Build FinancialData object
    return FinancialData(
        customer_id=f"CUST_{proposal_id}",
        annual_income=annual_income,
        income_stability=income_stability,
        employment_status=employment_status,
        years_employed=5,  # Not in DB, use default
        credit_score=credit_score,
        credit_history_length=10,  # Not in DB, use default
        total_debt=total_debt,
        debt_to_income_ratio=min(debt_to_income_ratio, 10.0),  # Cap at 10
        mortgage_status="Own",  # Not in DB, use default
        liquid_assets=liquid_assets,
        total_assets=total_assets,
        bankruptcy_history=False,  # Not in DB, assume false
        years_since_bankruptcy=None,
        late_payments_12mo=late_payments
    )
