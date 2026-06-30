"""Combined risk calculator with weighted scoring."""

from typing import List
from data.schemas.demographic_schema import DemographicData
from data.schemas.financial_schema import FinancialData
from data.schemas.medical_schema import MedicalData
from data.schemas.regional_schema import RegionalData
from data.schemas.claims_schema import ClaimsData
from data.schemas.agent_schema import AgentData
from data.schemas.product_schema import ProductData
from data.schemas.result_schema import RiskCalculationResult, CombinedRiskResult
from .demographic_risk import calculate_demographic_risk
from .financial_risk import calculate_financial_risk
from .medical_risk import calculate_medical_risk
from .regional_risk import calculate_regional_risk
from .claims_risk import calculate_claims_risk
from .agent_risk import calculate_agent_risk
from .product_risk import calculate_product_risk
from .utils import (
    get_risk_level,
    extract_top_factors,
    generate_combined_recommendations,
    get_loading_percentage,
    get_underwriting_decision
)


def calculate_combined_risk(
    demographic: DemographicData,
    financial: FinancialData,
    medical: MedicalData,
    regional: RegionalData,
    claims: ClaimsData,
    agent: AgentData,
    product: ProductData
) -> CombinedRiskResult:
    """
    Calculate combined risk score across all dimensions with weighted scoring.
    
    Weighted Risk Calculation:
    - Medical: 30% (highest priority)
    - Financial: 20%
    - Demographic: 15%
    - Claims: 15%
    - Regional: 10%
    - Agent: 5%
    - Product: 5%
    
    Overall Score = Σ (dimension_score × weight)
    
    Underwriting Decision Logic:
    - Score 0-49: ACCEPT (0-10% loading)
    - Score 50-69: REVIEW (25% loading)
    - Score 70-100: DECLINE
    
    Args:
        demographic: Customer demographic data
        financial: Customer financial data
        medical: Customer medical data
        regional: Geographic/regional data
        claims: Claims history data
        agent: Agent/channel data
        product: Product/underwriting data
        
    Returns:
        CombinedRiskResult with overall assessment and underwriting decision
    """
    # Calculate individual dimension risks
    demo_risk = calculate_demographic_risk(demographic)
    fin_risk = calculate_financial_risk(financial)
    med_risk = calculate_medical_risk(medical)
    reg_risk = calculate_regional_risk(regional)
    claims_risk = calculate_claims_risk(claims)
    agent_risk = calculate_agent_risk(agent)
    prod_risk = calculate_product_risk(product)
    
    # Collect all dimension results
    dimension_scores = [
        demo_risk,
        fin_risk,
        med_risk,
        reg_risk,
        claims_risk,
        agent_risk,
        prod_risk
    ]
    
    # Calculate weighted overall score
    overall_score = (
        demo_risk.risk_score * demo_risk.weight_in_overall +
        fin_risk.risk_score * fin_risk.weight_in_overall +
        med_risk.risk_score * med_risk.weight_in_overall +
        reg_risk.risk_score * reg_risk.weight_in_overall +
        claims_risk.risk_score * claims_risk.weight_in_overall +
        agent_risk.risk_score * agent_risk.weight_in_overall +
        prod_risk.risk_score * prod_risk.weight_in_overall
    )
    
    # Determine underwriting decision
    decision = get_underwriting_decision(overall_score)
    
    # Calculate recommended premium loading
    loading = get_loading_percentage(overall_score)
    
    # Extract top risk factors across all dimensions
    top_factors = extract_top_factors(dimension_scores, top_n=5)
    
    # Generate combined recommendations
    recommendations = generate_combined_recommendations(
        overall_score,
        decision,
        dimension_scores
    )
    
    # Add dimension-specific insights
    dimension_insights = []
    for result in dimension_scores:
        if result.risk_level in ["HIGH", "CRITICAL"]:
            dimension_insights.append(
                f"{result.dimension.capitalize()}: {result.risk_level} risk "
                f"(score: {result.risk_score:.1f})"
            )
    
    if dimension_insights:
        recommendations.append("High-risk dimensions: " + ", ".join(dimension_insights))
    
    return CombinedRiskResult(
        customer_id=demographic.customer_id,
        overall_risk_score=round(overall_score, 2),
        overall_risk_level=get_risk_level(overall_score),
        dimension_scores=dimension_scores,
        top_risk_factors=top_factors,
        underwriting_decision=decision,
        recommended_loading=loading,
        recommendations=recommendations
    )
