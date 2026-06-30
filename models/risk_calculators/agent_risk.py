"""Agent/distribution channel risk calculator."""

from data.schemas.agent_schema import AgentData
from data.schemas.result_schema import RiskCalculationResult
from .utils import get_risk_level


def calculate_agent_risk(data: AgentData) -> RiskCalculationResult:
    """
    Calculate agent/channel risk score based on performance, compliance, and fraud history.
    
    Risk Factors:
    - Compliance: Violations, complaints
    - Performance: Lapse rate, experience
    - Fraud: Investigations, confirmed cases
    - Channel: Distribution channel type
    
    Weight in Overall: 5%
    
    Args:
        data: AgentData containing agent performance and compliance information
        
    Returns:
        RiskCalculationResult with agent risk assessment
    """
    score = 0
    factors = []
    recommendations = []
    
    # Compliance violations
    if data.compliance_violations > 5:
        score += 30
        factors.append(f"Multiple compliance violations ({data.compliance_violations})")
        recommendations.append("Escalate to compliance review")
        recommendations.append("Review all policies from this agent")
    elif data.compliance_violations > 2:
        score += 20
        factors.append(f"Compliance violations present ({data.compliance_violations})")
        recommendations.append("Monitor agent compliance closely")
    elif data.compliance_violations > 0:
        score += 10
        factors.append(f"Minor compliance violations ({data.compliance_violations})")
    
    # Active complaints
    if data.active_complaints > 3:
        score += 25
        factors.append(f"Multiple active complaints ({data.active_complaints})")
        recommendations.append("Investigate complaint patterns")
    elif data.active_complaints > 0:
        score += 12
        factors.append(f"Active complaints ({data.active_complaints})")
        recommendations.append("Review complaint details")
    
    # Fraud history (CRITICAL)
    if data.fraud_confirmed_cases > 0:
        score += 50
        factors.append(f"Confirmed fraud cases ({data.fraud_confirmed_cases})")
        recommendations.append("CRITICAL: Review all policies from this agent")
        recommendations.append("Consider agent suspension")
    elif data.fraud_investigations > 0:
        score += 20
        factors.append(f"Fraud investigations ({data.fraud_investigations})")
        recommendations.append("Monitor agent activity closely")
    
    # Lapse rate (policy retention indicator)
    if data.lapse_rate > 20:
        score += 20
        factors.append(f"High lapse rate ({data.lapse_rate}%)")
        recommendations.append("Review agent's sales practices")
        recommendations.append("Assess policy suitability")
    elif data.lapse_rate > 15:
        score += 12
        factors.append(f"Elevated lapse rate ({data.lapse_rate}%)")
        recommendations.append("Monitor policy retention")
    elif data.lapse_rate > 10:
        score += 6
        factors.append(f"Moderate lapse rate ({data.lapse_rate}%)")
    
    # Years licensed (experience factor)
    if data.years_licensed < 2:
        score += 15
        factors.append(f"Limited experience ({data.years_licensed} years)")
        recommendations.append("Apply new agent guidelines")
    elif data.years_licensed < 5:
        score += 8
        factors.append(f"Moderate experience ({data.years_licensed} years)")
    # Experienced agents (5+ years) get no penalty
    
    # Distribution channel risk
    if data.distribution_channel == "Online":
        score += 10
        factors.append("Online channel (limited verification)")
        recommendations.append("Enhanced verification recommended")
    elif data.distribution_channel == "Direct":
        score += 5
        factors.append("Direct channel")
    # Broker and Captive channels are standard, no additional risk
    
    # Agent risk score (composite metric)
    if data.agent_risk_score > 70:
        score += 25
        factors.append(f"High agent risk score ({data.agent_risk_score})")
        recommendations.append("Enhanced due diligence required")
    elif data.agent_risk_score > 50:
        score += 15
        factors.append(f"Elevated agent risk score ({data.agent_risk_score})")
    elif data.agent_risk_score > 30:
        score += 8
        factors.append(f"Moderate agent risk score ({data.agent_risk_score})")
    
    # Performance metrics
    if data.total_policies_sold > 0:
        # Very low sales might indicate inexperience
        if data.total_policies_sold < 10:
            score += 10
            factors.append("Limited sales history")
        
        # Check recent activity
        if data.policies_sold_12mo == 0 and data.total_policies_sold > 0:
            score += 15
            factors.append("No recent sales activity")
            recommendations.append("Verify agent active status")
    
    # Cap score at 100
    final_score = min(score, 100)
    
    # Add general recommendations if no specific ones
    if not recommendations:
        recommendations.append("Standard agent risk profile")
        recommendations.append("No additional agent-related requirements")
    
    return RiskCalculationResult(
        dimension="agent",
        risk_score=final_score,
        risk_level=get_risk_level(final_score),
        risk_factors=factors,
        weight_in_overall=0.05,
        recommendations=recommendations
    )
