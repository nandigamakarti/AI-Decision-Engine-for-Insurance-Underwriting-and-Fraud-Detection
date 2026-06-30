"""Financial risk calculator."""

from data.schemas.financial_schema import FinancialData
from data.schemas.result_schema import RiskCalculationResult
from .utils import get_risk_level


def calculate_financial_risk(data: FinancialData) -> RiskCalculationResult:
    """
    Calculate financial risk score based on credit, debt, income, and financial history.
    
    Risk Factors:
    - Credit Score: 750+ (LOW), 650-749 (MEDIUM), 550-649 (HIGH), <550 (CRITICAL)
    - Debt-to-Income: <0.3 (LOW), 0.3-0.5 (MEDIUM), 0.5-0.8 (HIGH), >0.8 (CRITICAL)
    - Bankruptcy: Yes (+50), No (0)
    - Income Stability: Stable (0), Variable (+15), Unstable (+30)
    - Late Payments: 0 (0), 1-2 (+15), 3+ (+30)
    
    Weight in Overall: 20%
    
    Args:
        data: FinancialData containing customer financial information
        
    Returns:
        RiskCalculationResult with financial risk assessment
    """
    score = 0
    factors = []
    recommendations = []
    
    # Credit score analysis
    if data.credit_score < 550:
        score += 50
        factors.append(f"Poor credit score ({data.credit_score})")
        recommendations.append("CRITICAL: Request detailed credit report")
        recommendations.append("Consider decline or very high loading")
    elif data.credit_score < 650:
        score += 35
        factors.append(f"Below average credit score ({data.credit_score})")
        recommendations.append("Request credit report and explanation")
        recommendations.append("Apply elevated premium rates")
    elif data.credit_score < 700:
        score += 20
        factors.append(f"Fair credit score ({data.credit_score})")
        recommendations.append("Verify recent credit history")
    elif data.credit_score < 750:
        score += 10
        factors.append(f"Good credit score ({data.credit_score})")
    else:
        factors.append(f"Excellent credit score ({data.credit_score}) (favorable)")
    
    # Debt-to-income ratio
    if data.debt_to_income_ratio > 0.8:
        score += 40
        factors.append(f"Very high debt-to-income ratio ({data.debt_to_income_ratio:.1%})")
        recommendations.append("CRITICAL: Assess payment sustainability")
        recommendations.append("Consider lower coverage amount")
    elif data.debt_to_income_ratio > 0.5:
        score += 25
        factors.append(f"High debt-to-income ratio ({data.debt_to_income_ratio:.1%})")
        recommendations.append("Request detailed debt schedule")
        recommendations.append("Verify income stability")
    elif data.debt_to_income_ratio > 0.3:
        score += 12
        factors.append(f"Moderate debt-to-income ratio ({data.debt_to_income_ratio:.1%})")
    else:
        factors.append(f"Low debt-to-income ratio ({data.debt_to_income_ratio:.1%}) (favorable)")
    
    # Bankruptcy history
    if data.bankruptcy_history:
        if data.years_since_bankruptcy is not None:
            if data.years_since_bankruptcy < 3:
                score += 50
                factors.append(f"Recent bankruptcy ({data.years_since_bankruptcy} years ago)")
                recommendations.append("CRITICAL: Review bankruptcy details")
                recommendations.append("Consider decline or postpone")
            elif data.years_since_bankruptcy < 7:
                score += 30
                factors.append(f"Bankruptcy history ({data.years_since_bankruptcy} years ago)")
                recommendations.append("Request bankruptcy discharge documents")
                recommendations.append("Apply high premium loading")
            else:
                score += 15
                factors.append("Historical bankruptcy (7+ years ago)")
                recommendations.append("Verify financial recovery")
        else:
            score += 40
            factors.append("Bankruptcy history (timeframe unknown)")
            recommendations.append("Request bankruptcy details and timeline")
    else:
        factors.append("No bankruptcy history (favorable)")
    
    # Income stability
    if data.income_stability == "Unstable":
        score += 30
        factors.append("Unstable income")
        recommendations.append("Request 2+ years income documentation")
        recommendations.append("Consider shorter policy term")
    elif data.income_stability == "Variable":
        score += 15
        factors.append("Variable income")
        recommendations.append("Request average income over 3 years")
    else:
        factors.append(f"Stable income (favorable)")
    
    # Employment status
    if data.employment_status == "Unemployed":
        score += 35
        factors.append("Currently unemployed")
        recommendations.append("CRITICAL: Assess income source")
        recommendations.append("Verify ability to pay premiums")
    elif data.employment_status == "Self-Employed":
        score += 10
        factors.append("Self-employed (variable income)")
        recommendations.append("Request business financial statements")
    else:
        factors.append(f"Employed status: {data.employment_status}")
    
    # Late payments
    if data.late_payments_12mo >= 3:
        score += 30
        factors.append(f"Multiple late payments ({data.late_payments_12mo} in last 12 months)")
        recommendations.append("Assess payment discipline")
    elif data.late_payments_12mo > 0:
        score += 15
        factors.append(f"Recent late payments ({data.late_payments_12mo})")
        recommendations.append("Verify reasons for late payments")
    else:
        factors.append("No late payments (favorable)")
    
    # Cap score at 100
    final_score = min(score, 100)
    
    # Add general recommendations if no specific ones
    if not recommendations:
        recommendations.append("Strong financial profile")
        recommendations.append("Standard underwriting process")
    
    return RiskCalculationResult(
        dimension="financial",
        risk_score=final_score,
        risk_level=get_risk_level(final_score),
        risk_factors=factors,
        weight_in_overall=0.20,
        recommendations=recommendations
    )
