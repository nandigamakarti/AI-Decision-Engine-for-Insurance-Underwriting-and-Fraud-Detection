"""Product/underwriting risk calculator."""

from data.schemas.product_schema import ProductData
from data.schemas.result_schema import RiskCalculationResult
from .utils import get_risk_level


def calculate_product_risk(data: ProductData) -> RiskCalculationResult:
    """
    Calculate product/underwriting risk score based on coverage, pricing, and underwriting.
    
    Risk Factors:
    - Coverage Adequacy: Sum assured to income ratio
    - Affordability: Affordability score
    - Underwriting: Class, loading percentage
    - Pricing: Loss ratio, profit margin
    
    Weight in Overall: 5%
    
    Args:
        data: ProductData containing product and underwriting information
        
    Returns:
        RiskCalculationResult with product risk assessment
    """
    score = 0
    factors = []
    recommendations = []
    
    # Sum assured to income ratio (over-insurance risk)
    if data.sum_assured_to_income_ratio > 15:
        score += 35
        factors.append(f"Very high coverage ratio ({data.sum_assured_to_income_ratio:.1f}x income)")
        recommendations.append("CRITICAL: Investigate insurance need justification")
        recommendations.append("Assess potential moral hazard")
    elif data.sum_assured_to_income_ratio > 10:
        score += 25
        factors.append(f"High coverage ratio ({data.sum_assured_to_income_ratio:.1f}x income)")
        recommendations.append("Request detailed needs analysis")
        recommendations.append("Verify income documentation")
    elif data.sum_assured_to_income_ratio > 7:
        score += 15
        factors.append(f"Elevated coverage ratio ({data.sum_assured_to_income_ratio:.1f}x income)")
        recommendations.append("Verify coverage justification")
    elif data.sum_assured_to_income_ratio > 5:
        score += 8
        factors.append(f"Moderate coverage ratio ({data.sum_assured_to_income_ratio:.1f}x income)")
    else:
        factors.append(f"Appropriate coverage ratio ({data.sum_assured_to_income_ratio:.1f}x income) (favorable)")
    
    # Affordability score (ability to pay premiums)
    if data.affordability_score < 40:
        score += 30
        factors.append(f"Poor affordability ({data.affordability_score}/100)")
        recommendations.append("CRITICAL: Assess premium payment sustainability")
        recommendations.append("Consider lower coverage amount")
    elif data.affordability_score < 60:
        score += 20
        factors.append(f"Below average affordability ({data.affordability_score}/100)")
        recommendations.append("Verify income stability")
    elif data.affordability_score < 75:
        score += 10
        factors.append(f"Moderate affordability ({data.affordability_score}/100)")
    else:
        factors.append(f"Good affordability ({data.affordability_score}/100) (favorable)")
    
    # Underwriting class
    if data.underwriting_class == "Declined":
        score += 50
        factors.append("Previously declined underwriting class")
        recommendations.append("CRITICAL: Review decline reasons")
        recommendations.append("Consider decline or postpone")
    elif data.underwriting_class == "Substandard":
        score += 25
        factors.append("Substandard underwriting class")
        recommendations.append("Apply appropriate loading")
        recommendations.append("Review medical/financial reasons")
    elif data.underwriting_class == "Standard":
        score += 5
        factors.append("Standard underwriting class")
    else:
        factors.append("Preferred underwriting class (favorable)")
    
    # Loading percentage (existing risk premium)
    if data.loading_percentage > 100:
        score += 30
        factors.append(f"Very high loading ({data.loading_percentage}%)")
        recommendations.append("Review justification for high loading")
    elif data.loading_percentage > 50:
        score += 20
        factors.append(f"High loading ({data.loading_percentage}%)")
    elif data.loading_percentage > 25:
        score += 10
        factors.append(f"Moderate loading ({data.loading_percentage}%)")
    elif data.loading_percentage > 0:
        factors.append(f"Minimal loading ({data.loading_percentage}%)")
    else:
        factors.append("No loading applied (favorable)")
    
    # Loss ratio expected (profitability indicator)
    if data.loss_ratio_expected > 90:
        score += 25
        factors.append(f"Very high loss ratio ({data.loss_ratio_expected}%)")
        recommendations.append("Review pricing adequacy")
        recommendations.append("Consider premium adjustment")
    elif data.loss_ratio_expected > 80:
        score += 15
        factors.append(f"High loss ratio ({data.loss_ratio_expected}%)")
        recommendations.append("Monitor claims experience")
    elif data.loss_ratio_expected > 70:
        score += 8
        factors.append(f"Elevated loss ratio ({data.loss_ratio_expected}%)")
    else:
        factors.append(f"Acceptable loss ratio ({data.loss_ratio_expected}%)")
    
    # Profit margin (sustainability indicator)
    if data.profit_margin < 5:
        score += 20
        factors.append(f"Low profit margin ({data.profit_margin}%)")
        recommendations.append("Review pricing structure")
    elif data.profit_margin < 10:
        score += 10
        factors.append(f"Below target profit margin ({data.profit_margin}%)")
    else:
        factors.append(f"Healthy profit margin ({data.profit_margin}%)")
    
    # Policy term (longer terms have more uncertainty)
    if data.policy_term_years > 30:
        score += 15
        factors.append(f"Very long policy term ({data.policy_term_years} years)")
        recommendations.append("Consider term-specific risk factors")
    elif data.policy_term_years > 20:
        score += 8
        factors.append(f"Long policy term ({data.policy_term_years} years)")
    else:
        factors.append(f"Policy term: {data.policy_term_years} years")
    
    # Exclusions (if many exclusions, indicates higher base risk)
    if len(data.exclusions) > 5:
        score += 15
        factors.append(f"Multiple exclusions ({len(data.exclusions)})")
        recommendations.append("Review exclusion justifications")
    elif len(data.exclusions) > 2:
        score += 8
        factors.append(f"Several exclusions ({len(data.exclusions)})")
    elif len(data.exclusions) > 0:
        factors.append(f"{len(data.exclusions)} exclusion(s)")
    else:
        factors.append("No exclusions (favorable)")
    
    # Product type specific risks
    factors.append(f"Product type: {data.product_type}")
    if data.product_type == "Whole Life":
        score += 5
    elif data.product_type == "Critical Illness":
        score += 10
    
    # Cap score at 100
    final_score = min(score, 100)
    
    # Add general recommendations if no specific ones
    if not recommendations:
        recommendations.append("Standard product risk profile")
        recommendations.append("No additional product-related requirements")
    
    return RiskCalculationResult(
        dimension="product",
        risk_score=final_score,
        risk_level=get_risk_level(final_score),
        risk_factors=factors,
        weight_in_overall=0.05,
        recommendations=recommendations
    )
