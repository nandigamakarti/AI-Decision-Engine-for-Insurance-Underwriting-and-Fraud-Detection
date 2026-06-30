"""Claims history risk calculator."""

from data.schemas.claims_schema import ClaimsData
from data.schemas.result_schema import RiskCalculationResult
from .utils import get_risk_level


def calculate_claims_risk(data: ClaimsData) -> RiskCalculationResult:
    """
    Calculate claims history risk score based on frequency, amounts, and fraud indicators.
    
    Risk Factors:
    - Claim Frequency: Number and trend of claims
    - Claim Amounts: Total, average, and highest claims
    - Fraud Indicators: Suspicious patterns, fraud score
    - Recent Activity: Claims in last 12 and 36 months
    
    Weight in Overall: 15%
    
    Args:
        data: ClaimsData containing customer claims history
        
    Returns:
        RiskCalculationResult with claims risk assessment
    """
    score = 0
    factors = []
    recommendations = []
    
    # Total claims count (historical frequency)
    if data.total_claims_count > 15:
        score += 30
        factors.append(f"Very high claim frequency ({data.total_claims_count} total claims)")
        recommendations.append("Investigate claim patterns and causes")
    elif data.total_claims_count > 10:
        score += 20
        factors.append(f"High claim frequency ({data.total_claims_count} total claims)")
        recommendations.append("Review claim history in detail")
    elif data.total_claims_count > 5:
        score += 10
        factors.append(f"Moderate claim frequency ({data.total_claims_count} total claims)")
    
    # Recent claims activity (last 12 months)
    if data.claims_last_12mo > 5:
        score += 35
        factors.append(f"Very high recent claim activity ({data.claims_last_12mo} in last 12 months)")
        recommendations.append("CRITICAL: Assess current health/risk status")
    elif data.claims_last_12mo > 3:
        score += 25
        factors.append(f"High recent claim activity ({data.claims_last_12mo} in last 12 months)")
        recommendations.append("Request recent medical examination")
    elif data.claims_last_12mo > 1:
        score += 12
        factors.append(f"Multiple recent claims ({data.claims_last_12mo} in last 12 months)")
    
    # Claims in last 36 months (medium-term trend)
    if data.claims_last_36mo > 10:
        score += 20
        factors.append(f"High 3-year claim activity ({data.claims_last_36mo} claims)")
    elif data.claims_last_36mo > 6:
        score += 12
        factors.append(f"Elevated 3-year claim activity ({data.claims_last_36mo} claims)")
    
    # Claim frequency trend
    if data.claim_frequency_trend == "Increasing":
        score += 25
        factors.append("Increasing claim frequency trend")
        recommendations.append("Assess underlying health deterioration")
        recommendations.append("Consider higher premium loading")
    elif data.claim_frequency_trend == "Stable":
        score += 5
        factors.append("Stable claim frequency")
    # Decreasing trend is positive, no points added
    
    # Average claim amount (high averages indicate serious conditions)
    if data.average_claim_amount > 10000:
        score += 20
        factors.append(f"High average claim amount (${data.average_claim_amount:,.0f})")
        recommendations.append("Review nature of high-cost claims")
    elif data.average_claim_amount > 5000:
        score += 12
        factors.append(f"Elevated average claim amount (${data.average_claim_amount:,.0f})")
    elif data.average_claim_amount > 2500:
        score += 6
    
    # Highest single claim (catastrophic event indicator)
    if data.highest_single_claim > 50000:
        score += 25
        factors.append(f"Very high single claim (${data.highest_single_claim:,.0f})")
        recommendations.append("Investigate circumstances of highest claim")
    elif data.highest_single_claim > 25000:
        score += 15
        factors.append(f"High single claim (${data.highest_single_claim:,.0f})")
    elif data.highest_single_claim > 10000:
        score += 8
        factors.append(f"Significant single claim (${data.highest_single_claim:,.0f})")
    
    # Total claims amount (cumulative financial impact)
    if data.total_claims_amount > 100000:
        score += 20
        factors.append(f"Very high total claims (${data.total_claims_amount:,.0f})")
    elif data.total_claims_amount > 50000:
        score += 12
        factors.append(f"High total claims (${data.total_claims_amount:,.0f})")
    elif data.total_claims_amount > 25000:
        score += 6
    
    # Fraud indicators (CRITICAL)
    if data.suspicious_patterns_detected:
        score += 40
        factors.append("Suspicious claim patterns detected")
        recommendations.append("CRITICAL: Conduct fraud investigation")
        recommendations.append("Review all claims for authenticity")
    
    # Fraud score
    if data.fraud_score > 70:
        score += 50
        factors.append(f"High fraud risk score ({data.fraud_score})")
        recommendations.append("CRITICAL: Escalate to fraud investigation unit")
        recommendations.append("Consider decline pending investigation")
    elif data.fraud_score > 50:
        score += 30
        factors.append(f"Elevated fraud risk score ({data.fraud_score})")
        recommendations.append("Enhanced claim verification required")
    elif data.fraud_score > 30:
        score += 15
        factors.append(f"Moderate fraud risk score ({data.fraud_score})")
        recommendations.append("Monitor claims closely")
    
    # Analyze recent claims for patterns
    if len(data.recent_claims) > 0:
        # Check for denied claims
        denied_claims = [c for c in data.recent_claims if c.status == "Denied"]
        if len(denied_claims) > 2:
            score += 15
            factors.append(f"Multiple denied claims ({len(denied_claims)})")
            recommendations.append("Review reasons for claim denials")
        
        # Check for pending claims
        pending_claims = [c for c in data.recent_claims if c.status == "Pending"]
        if len(pending_claims) > 3:
            score += 10
            factors.append(f"Multiple pending claims ({len(pending_claims)})")
    
    # Cap score at 100
    final_score = min(score, 100)
    
    # Add general recommendations if no specific ones
    if not recommendations:
        if data.total_claims_count == 0:
            recommendations.append("No claims history - favorable indicator")
        else:
            recommendations.append("Standard claims risk profile")
            recommendations.append("No additional claims-related requirements")
    
    return RiskCalculationResult(
        dimension="claims",
        risk_score=final_score,
        risk_level=get_risk_level(final_score),
        risk_factors=factors,
        weight_in_overall=0.15,
        recommendations=recommendations
    )
