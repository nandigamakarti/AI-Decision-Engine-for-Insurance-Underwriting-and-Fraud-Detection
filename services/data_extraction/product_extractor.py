"""
Product data extractor.

Extracts product/underwriting information from database tables:
- ProductDetails: product features, waiting periods
- ProposalDetails: sum insured, annual income
- PortabilityDetails: portability information
"""

from sqlalchemy.orm import Session
from db.models import ProductDetails, ProposalDetails, PortabilityDetails
from data.schemas.product_schema import ProductData


def extract_product_data(db: Session, proposal_id: str) -> ProductData:
    """
    Extract product data from database for a given proposal.
    
    Args:
        db: Database session
        proposal_id: Unique proposal identifier
        
    Returns:
        ProductData object populated from database
        
    Raises:
        ValueError: If proposal or product not found
    """
    # Get proposal
    proposal = db.query(ProposalDetails).filter(
        ProposalDetails.proposal_num == proposal_id
    ).first()
    
    if not proposal:
        raise ValueError(f"Proposal {proposal_id} not found")
    
    # Get product details
    product = db.query(ProductDetails).filter(
        ProductDetails.product_id == proposal.product_id
    ).first()
    
    if not product:
        raise ValueError(f"Product {proposal.product_id} not found")
    
    # Get portability details
    portability = db.query(PortabilityDetails).filter(
        PortabilityDetails.proposal_num == proposal_id
    ).first()
    
    # Calculate sum assured to income ratio
    sum_insured = float(proposal.sum_insured) if proposal.sum_insured else 500000.0
    annual_income = float(proposal.annual_income) if proposal.annual_income else 1000000.0
    sum_assured_to_income_ratio = sum_insured / annual_income if annual_income > 0 else 0.5
    
    # Calculate premium (estimate as 2-3% of sum insured)
    estimated_premium = sum_insured * 0.025
    
    # Calculate affordability score (0-100, higher is better)
    affordability_score = 100
    if annual_income > 0:
        premium_to_income = (estimated_premium / annual_income) * 100
        if premium_to_income > 5:
            affordability_score = 50
        elif premium_to_income > 3:
            affordability_score = 70
        elif premium_to_income > 2:
            affordability_score = 85
    
    # Determine underwriting class
    underwriting_class = "Standard"
    if sum_assured_to_income_ratio > 10:
        underwriting_class = "Declined"
    elif sum_assured_to_income_ratio > 5:
        underwriting_class = "Substandard"
    elif sum_assured_to_income_ratio < 1:
        underwriting_class = "Preferred"
    
    # Determine product type from product name
    # Schema allows: "Term Life|Whole Life|Health|Critical Illness|Disability"
    product_type = "Health"  # Default
    if product and product.product_name:
        product_name_lower = product.product_name.lower()
        if "term" in product_name_lower and "life" in product_name_lower:
            product_type = "Term Life"
        elif "whole" in product_name_lower and "life" in product_name_lower:
            product_type = "Whole Life"
        elif "critical" in product_name_lower or "illness" in product_name_lower:
            product_type = "Critical Illness"
        elif "disability" in product_name_lower:
            product_type = "Disability"
        elif "health" in product_name_lower:
            product_type = "Health"
        else:
            product_type = "Health"  # Default to Health for insurance
    
    # Get policy term from product details or estimate
    policy_term_years = 1  # Default for health insurance
    if product and hasattr(product, 'policy_term'):
        policy_term_years = product.policy_term or 1
    
    # Calculate loading percentage based on underwriting class
    loading_map = {
        "Preferred": 0.0,
        "Standard": 0.0,
        "Substandard": 25.0,
        "Declined": 50.0
    }
    loading_percentage = loading_map.get(underwriting_class, 0.0)
    
    # Estimate loss ratio (product-level)
    loss_ratio_expected = 65.0  # Industry average for health insurance
    
    # Estimate profit margin
    profit_margin = 15.0  # Default
    if loading_percentage > 0:
        profit_margin = 20.0  # Higher margin for substandard risks
    
    # Build ProductData object
    return ProductData(
        customer_id=f"CUST_{proposal_id}",
        product_name=product.product_name if product else "Unknown Product",
        product_type=product_type,
        coverage_amount=sum_insured,
        premium_amount=estimated_premium,
        policy_term_years=policy_term_years,
        sum_assured=sum_insured,
        annual_income=annual_income,
        sum_assured_to_income_ratio=sum_assured_to_income_ratio,
        affordability_score=affordability_score,
        underwriting_class=underwriting_class,
        loading_percentage=loading_percentage,
        loss_ratio_expected=loss_ratio_expected,
        loss_ratio_percentage=loss_ratio_expected,  # Same as loss_ratio_expected
        profit_margin=profit_margin,
        profit_margin_percentage=profit_margin  # Same as profit_margin
    )
