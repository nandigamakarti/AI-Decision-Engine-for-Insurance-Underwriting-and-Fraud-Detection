"""Utility functions for risk calculators."""

from typing import List


def get_risk_level(score: float) -> str:
    """
    Convert numerical risk score to categorical risk level.
    
    Risk Level Thresholds:
    - LOW: 0-29
    - MEDIUM: 30-49
    - HIGH: 50-69
    - CRITICAL: 70-100
    
    Args:
        score: Risk score from 0-100
        
    Returns:
        Risk level as string (LOW, MEDIUM, HIGH, CRITICAL)
    """
    if score < 30:
        return "LOW"
    elif score < 50:
        return "MEDIUM"
    elif score < 70:
        return "HIGH"
    else:
        return "CRITICAL"


def extract_top_factors(dimension_results: List, top_n: int = 5) -> List[str]:
    """
    Extract top N risk factors across all dimensions.
    
    Args:
        dimension_results: List of RiskCalculationResult objects
        top_n: Number of top factors to extract (default: 5)
        
    Returns:
        List of top risk factors with dimension labels
    """
    all_factors = []
    
    for result in dimension_results:
        # Add dimension label to each factor
        for factor in result.risk_factors:
            all_factors.append(f"{factor} ({result.dimension.capitalize()})")
    
    # Return top N factors (or all if less than N)
    return all_factors[:top_n]


def generate_combined_recommendations(
    overall_score: float,
    decision: str,
    dimension_results: List
) -> List[str]:
    """
    Generate combined recommendations based on overall assessment.
    
    Args:
        overall_score: Overall risk score (0-100)
        decision: Underwriting decision (ACCEPT/REVIEW/DECLINE)
        dimension_results: List of individual dimension results
        
    Returns:
        List of combined recommendations
    """
    recommendations = []
    
    # Decision-based recommendations
    if decision == "ACCEPT":
        loading = get_loading_percentage(overall_score)
        if loading > 0:
            recommendations.append(f"Accept with {loading}% premium loading")
        else:
            recommendations.append("Accept at standard rates")
    elif decision == "REVIEW":
        recommendations.append("Refer to senior underwriter for manual review")
        recommendations.append("Request additional documentation")
    else:  # DECLINE
        recommendations.append("Decline application - risk exceeds acceptable thresholds")
        recommendations.append("Provide decline reason to applicant")
    
    # Add high-risk dimension recommendations
    high_risk_dims = [r for r in dimension_results if r.risk_level in ["HIGH", "CRITICAL"]]
    if high_risk_dims:
        for result in high_risk_dims:
            recommendations.append(f"Address {result.dimension} risk factors (score: {result.risk_score:.0f})")
    
    return recommendations


def get_loading_percentage(overall_score: float) -> float:
    """
    Calculate premium loading percentage based on overall risk score.
    
    Loading Tiers:
    - 0-29 (LOW): 0%
    - 30-49 (MEDIUM): 10%
    - 50-69 (REVIEW): 25%
    - 70-100 (DECLINE): 0% (declined, no loading)
    
    Args:
        overall_score: Overall risk score (0-100)
        
    Returns:
        Premium loading percentage
    """
    if overall_score < 30:
        return 0.0
    elif overall_score < 50:
        return 10.0
    elif overall_score < 70:
        return 25.0
    else:
        return 0.0  # Declined applications have no loading


def get_underwriting_decision(overall_score: float) -> str:
    """
    Determine underwriting decision based on overall risk score.
    
    Decision Thresholds:
    - 0-49: ACCEPT
    - 50-69: REVIEW (manual underwriting required)
    - 70-100: DECLINE
    
    Args:
        overall_score: Overall risk score (0-100)
        
    Returns:
        Underwriting decision (ACCEPT, REVIEW, DECLINE)
    """
    if overall_score < 50:
        return "ACCEPT"
    elif overall_score < 70:
        return "REVIEW"
    else:
        return "DECLINE"
