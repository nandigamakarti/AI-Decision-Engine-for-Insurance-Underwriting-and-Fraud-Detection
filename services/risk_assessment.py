"""
Risk Assessment Service - Core business logic for calculating customer risk.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from api.models import (
    CustomerDataInput, RiskAssessmentOutput, RiskFactor, HealthInfo, 
    FinancialInfo, ClaimsHistory
)


class RiskAssessmentService:
    """Service for assessing customer risk based on provided data."""

    def __init__(self):
        """Initialize the risk assessment service."""
        pass

    def assess_risk(self, customer_data: CustomerDataInput) -> RiskAssessmentOutput:
        """
        Assess the risk of a customer based on their data.

        Args:
            customer_data: Complete customer data input

        Returns:
            RiskAssessmentOutput containing risk assessment results
        """
        risk_factors: List[RiskFactor] = []

        # Assess health-related risks
        if customer_data.health_info:
            risk_factors.extend(self._assess_health_risks(customer_data.health_info))

        # Assess financial risks
        if customer_data.financial_info:
            risk_factors.extend(self._assess_financial_risks(customer_data.financial_info))

        # Assess claims history risks
        if customer_data.claims_history:
            risk_factors.extend(self._assess_claims_risks(customer_data.claims_history))

        # Assess personal information risks
        risk_factors.extend(self._assess_personal_risks(customer_data.personal_info))

        # Calculate overall risk score and level
        overall_score = self._calculate_overall_score(risk_factors)
        overall_level = self._determine_risk_level(overall_score)

        # Generate recommendations
        recommendations = self._generate_recommendations(risk_factors, overall_level)

        return RiskAssessmentOutput(
            customer_id=customer_data.customer_id,
            overall_risk_level=overall_level,
            overall_risk_score=overall_score,
            risk_factors=risk_factors,
            recommendations=recommendations,
            assessment_date=datetime.now().isoformat(),
            additional_notes="Risk assessment completed using AI-assisted underwriting engine"
        )

    def _assess_health_risks(self, health_info: HealthInfo) -> List[RiskFactor]:
        """Assess health-related risk factors."""
        factors: List[RiskFactor] = []

        # Smoking assessment
        if health_info.smoker is True:
            factors.append(RiskFactor(
                factor_name="Smoking Status",
                risk_level="HIGH",
                score=75,
                description="Customer is a smoker, which increases health insurance risk significantly"
            ))

        # Health conditions assessment
        if health_info.health_conditions:
            condition_count = len(health_info.health_conditions)
            if condition_count >= 3:
                risk_level = "CRITICAL"
                score = 85
            elif condition_count >= 2:
                risk_level = "HIGH"
                score = 65
            else:
                risk_level = "MEDIUM"
                score = 45

            factors.append(RiskFactor(
                factor_name="Pre-existing Health Conditions",
                risk_level=risk_level,
                score=score,
                description=f"Customer has {condition_count} pre-existing health condition(s): {', '.join(health_info.health_conditions)}"
            ))

        # BMI assessment
        if health_info.bmi is not None:
            if health_info.bmi >= 30:
                risk_level = "HIGH"
                score = 60
                description = f"High BMI ({health_info.bmi:.1f}) indicates obesity, increasing health risks"
            elif health_info.bmi < 18.5:
                risk_level = "MEDIUM"
                score = 40
                description = f"Low BMI ({health_info.bmi:.1f}) may indicate nutritional concerns"
            else:
                risk_level = "LOW"
                score = 20
                description = f"BMI ({health_info.bmi:.1f}) is within normal range"

            factors.append(RiskFactor(
                factor_name="Body Mass Index",
                risk_level=risk_level,
                score=score,
                description=description
            ))

        # Alcohol consumption assessment
        if health_info.alcohol_consumption:
            consumption_lower = health_info.alcohol_consumption.lower()
            if "heavy" in consumption_lower or "daily" in consumption_lower:
                factors.append(RiskFactor(
                    factor_name="Alcohol Consumption",
                    risk_level="HIGH",
                    score=70,
                    description="Heavy alcohol consumption increases health risks"
                ))
            elif "moderate" in consumption_lower or "weekly" in consumption_lower:
                factors.append(RiskFactor(
                    factor_name="Alcohol Consumption",
                    risk_level="MEDIUM",
                    score=40,
                    description="Moderate alcohol consumption presents moderate health risks"
                ))

        return factors

    def _assess_financial_risks(self, financial_info: FinancialInfo) -> List[RiskFactor]:
        """Assess financial-related risk factors."""
        factors: List[RiskFactor] = []

        # Credit score assessment
        if financial_info.credit_score is not None:
            if financial_info.credit_score < 600:
                risk_level = "CRITICAL"
                score = 85
                description = "Very poor credit score indicates high financial risk"
            elif financial_info.credit_score < 700:
                risk_level = "HIGH"
                score = 65
                description = "Poor credit score indicates financial risk"
            elif financial_info.credit_score < 750:
                risk_level = "MEDIUM"
                score = 35
                description = "Fair credit score indicates moderate financial risk"
            else:
                risk_level = "LOW"
                score = 15
                description = "Good credit score indicates low financial risk"

            factors.append(RiskFactor(
                factor_name="Credit Score",
                risk_level=risk_level,
                score=score,
                description=description
            ))

        # Debt-to-income ratio assessment
        if financial_info.annual_income and financial_info.outstanding_debts:
            if financial_info.annual_income > 0:
                debt_ratio = (financial_info.outstanding_debts / financial_info.annual_income) * 100
                
                if debt_ratio > 50:
                    risk_level = "CRITICAL"
                    score = 80
                elif debt_ratio > 30:
                    risk_level = "HIGH"
                    score = 60
                elif debt_ratio > 15:
                    risk_level = "MEDIUM"
                    score = 35
                else:
                    risk_level = "LOW"
                    score = 15

                factors.append(RiskFactor(
                    factor_name="Debt-to-Income Ratio",
                    risk_level=risk_level,
                    score=score,
                    description=f"Debt-to-income ratio of {debt_ratio:.1f}% indicates {'high' if debt_ratio > 50 else 'moderate' if debt_ratio > 30 else 'low'} financial stress"
                ))

        # Employment status assessment
        if financial_info.employment_status:
            status_lower = financial_info.employment_status.lower()
            if "unemployed" in status_lower:
                factors.append(RiskFactor(
                    factor_name="Employment Status",
                    risk_level="HIGH",
                    score=70,
                    description="Currently unemployed, indicating income instability"
                ))
            elif "self-employed" in status_lower:
                factors.append(RiskFactor(
                    factor_name="Employment Status",
                    risk_level="MEDIUM",
                    score=40,
                    description="Self-employed status may indicate income variability"
                ))

        return factors

    def _assess_claims_risks(self, claims_history: ClaimsHistory) -> List[RiskFactor]:
        """Assess claims history related risk factors."""
        factors: List[RiskFactor] = []

        # Total claims assessment
        if claims_history.total_claims is not None:
            if claims_history.total_claims >= 5:
                risk_level = "CRITICAL"
                score = 80
            elif claims_history.total_claims >= 3:
                risk_level = "HIGH"
                score = 65
            elif claims_history.total_claims >= 1:
                risk_level = "MEDIUM"
                score = 40
            else:
                risk_level = "LOW"
                score = 10

            factors.append(RiskFactor(
                factor_name="Claim Frequency",
                risk_level=risk_level,
                score=score,
                description=f"Customer has filed {claims_history.total_claims} claim(s) in the past"
            ))

        # Major claims assessment
        if claims_history.major_claims:
            factors.append(RiskFactor(
                factor_name="Major Claims History",
                risk_level="HIGH",
                score=70,
                description=f"Customer has {len(claims_history.major_claims)} major claim(s): {', '.join(claims_history.major_claims)}"
            ))

        # Claim amount assessment
        if claims_history.claim_amount_total is not None and claims_history.claim_amount_total > 0:
            if claims_history.claim_amount_total > 100000:
                factors.append(RiskFactor(
                    factor_name="Total Claim Amount",
                    risk_level="HIGH",
                    score=75,
                    description=f"High total claim amount of ${claims_history.claim_amount_total:,.2f}"
                ))

        return factors

    def _assess_personal_risks(self, personal_info) -> List[RiskFactor]:
        """Assess personal information related risk factors."""
        factors: List[RiskFactor] = []

        # Age-based risk assessment
        if personal_info.age:
            if personal_info.age < 25:
                factors.append(RiskFactor(
                    factor_name="Age (Young)",
                    risk_level="MEDIUM",
                    score=50,
                    description=f"Customer age {personal_info.age} - statistically higher risk for certain insurance types"
                ))
            elif personal_info.age > 70:
                factors.append(RiskFactor(
                    factor_name="Age (Senior)",
                    risk_level="HIGH",
                    score=60,
                    description=f"Customer age {personal_info.age} - senior age increases health and mortality risks"
                ))
            else:
                factors.append(RiskFactor(
                    factor_name="Age",
                    risk_level="LOW",
                    score=20,
                    description=f"Customer age {personal_info.age} - within optimal age range"
                ))

        return factors

    def _calculate_overall_score(self, risk_factors: List[RiskFactor]) -> float:
        """
        Calculate overall risk score from individual factors.
        Uses weighted average approach.
        """
        if not risk_factors:
            return 20.0  # Base score if no risk factors

        total_score = sum(factor.score for factor in risk_factors)
        average_score = total_score / len(risk_factors)

        # Apply weighting based on risk levels
        weighted_scores = []
        for factor in risk_factors:
            weight = self._get_weight_for_level(factor.risk_level)
            weighted_scores.append(factor.score * weight)

        if weighted_scores:
            overall_score = sum(weighted_scores) / len(weighted_scores)
        else:
            overall_score = average_score

        return min(100.0, max(0.0, overall_score))

    def _get_weight_for_level(self, risk_level: str) -> float:
        """Get weighting multiplier for risk level."""
        weights = {
            "LOW": 0.8,
            "MEDIUM": 1.0,
            "HIGH": 1.2,
            "CRITICAL": 1.4
        }
        return weights.get(risk_level.upper(), 1.0)

    def _determine_risk_level(self, score: float) -> str:
        """Determine overall risk level based on score."""
        if score >= 75:
            return "CRITICAL"
        elif score >= 55:
            return "HIGH"
        elif score >= 35:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_recommendations(self, risk_factors: List[RiskFactor], overall_level: str) -> List[str]:
        """Generate underwriting recommendations based on risk assessment."""
        recommendations = []

        # Group risk factors by level
        critical_factors = [f for f in risk_factors if f.risk_level == "CRITICAL"]
        high_factors = [f for f in risk_factors if f.risk_level == "HIGH"]

        # Generate recommendations based on identified risks
        if critical_factors:
            recommendations.append(f"CRITICAL: Requires underwriting review - {len(critical_factors)} critical risk factor(s) identified")
            for factor in critical_factors:
                recommendations.append(f"- {factor.factor_name}: {factor.description}")

        if high_factors and overall_level in ["HIGH", "CRITICAL"]:
            recommendations.append(f"Request additional medical/financial documentation due to {len(high_factors)} high-risk factor(s)")

        # Lifestyle recommendations
        smoking_factor = next((f for f in risk_factors if "smoking" in f.factor_name.lower()), None)
        if smoking_factor and smoking_factor.risk_level in ["HIGH", "CRITICAL"]:
            recommendations.append("Consider offering smoking cessation programs for premium reduction")

        # Financial recommendations
        debt_factor = next((f for f in risk_factors if "debt" in f.factor_name.lower()), None)
        if debt_factor and debt_factor.risk_level in ["HIGH", "CRITICAL"]:
            recommendations.append("Consider financial stability verification or reduced coverage limits")

        if not recommendations:
            if overall_level == "LOW":
                recommendations.append("Approve application - low risk profile identified")
            elif overall_level == "MEDIUM":
                recommendations.append("Approve with standard terms - moderate risk profile")

        return recommendations
