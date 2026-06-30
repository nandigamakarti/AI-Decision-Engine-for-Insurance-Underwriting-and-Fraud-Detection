"""
AI-powered risk assessment API routes.

These endpoints use GPT-OSS-20B model for intelligent risk assessment,
working alongside the rule-based calculators.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from data.schemas.result_schema import RiskCalculationResult, CombinedRiskResult
from pydantic import BaseModel, Field

# Import data extractors (reuse from existing system)
from services.data_extraction import (
    extract_demographic_data,
    extract_financial_data,
    extract_medical_data,
    extract_regional_data,
    extract_claims_data,
    extract_agent_data,
    extract_product_data
)

# Import AI risk assessment functions
from services.ai_risk_service import (
    assess_demographic_risk_ai,
    assess_financial_risk_ai,
    assess_medical_risk_ai,
    assess_regional_risk_ai,
    assess_claims_risk_ai,
    assess_agent_risk_ai,
    assess_product_risk_ai
)

router = APIRouter(prefix="/api/ai-risk", tags=["AI Risk Assessment"])


class RiskAssessmentRequest(BaseModel):
    """Request model for AI risk assessment endpoints."""
    proposal_id: str = Field(
        ..., 
        description="Unique proposal identifier from database",
        examples=["PROP001", "PROP002"]
    )


@router.post(
    "/demographic",
    response_model=RiskCalculationResult,
    summary="AI Demographic Risk Assessment",
    description="Calculate demographic risk using GPT-OSS-20B AI model"
)
async def assess_demographic_risk_ai_endpoint(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """
    AI-powered demographic risk assessment.
    
    Uses GPT-OSS-20B model to analyze age, lifestyle, and socioeconomic factors.
    """
    try:
        data = extract_demographic_data(db, request.proposal_id)
        return assess_demographic_risk_ai(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI assessment error: {str(e)}")


@router.post(
    "/financial",
    response_model=RiskCalculationResult,
    summary="AI Financial Risk Assessment",
    description="Calculate financial risk using GPT-OSS-20B AI model"
)
async def assess_financial_risk_ai_endpoint(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """AI-powered financial risk assessment."""
    try:
        data = extract_financial_data(db, request.proposal_id)
        return assess_financial_risk_ai(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI assessment error: {str(e)}")


@router.post(
    "/medical",
    response_model=RiskCalculationResult,
    summary="AI Medical Risk Assessment",
    description="Calculate medical risk using GPT-OSS-20B AI model"
)
async def assess_medical_risk_ai_endpoint(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """AI-powered medical risk assessment."""
    try:
        data = extract_medical_data(db, request.proposal_id)
        return assess_medical_risk_ai(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI assessment error: {str(e)}")


@router.post(
    "/regional",
    response_model=RiskCalculationResult,
    summary="AI Regional Risk Assessment",
    description="Calculate regional risk using GPT-OSS-20B AI model"
)
async def assess_regional_risk_ai_endpoint(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """AI-powered regional risk assessment."""
    try:
        data = extract_regional_data(db, request.proposal_id)
        return assess_regional_risk_ai(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI assessment error: {str(e)}")


@router.post(
    "/claims",
    response_model=RiskCalculationResult,
    summary="AI Claims Risk Assessment",
    description="Calculate claims risk using GPT-OSS-20B AI model"
)
async def assess_claims_risk_ai_endpoint(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """AI-powered claims history risk assessment."""
    try:
        data = extract_claims_data(db, request.proposal_id)
        return assess_claims_risk_ai(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI assessment error: {str(e)}")


@router.post(
    "/agent",
    response_model=RiskCalculationResult,
    summary="AI Agent Risk Assessment",
    description="Calculate agent risk using GPT-OSS-20B AI model"
)
async def assess_agent_risk_ai_endpoint(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """AI-powered agent risk assessment."""
    try:
        data = extract_agent_data(db, request.proposal_id)
        return assess_agent_risk_ai(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI assessment error: {str(e)}")


@router.post(
    "/product",
    response_model=RiskCalculationResult,
    summary="AI Product Risk Assessment",
    description="Calculate product risk using GPT-OSS-20B AI model"
)
async def assess_product_risk_ai_endpoint(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """AI-powered product risk assessment."""
    try:
        data = extract_product_data(db, request.proposal_id)
        return assess_product_risk_ai(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI assessment error: {str(e)}")


@router.post(
    "/combined",
    response_model=CombinedRiskResult,
    summary="AI Combined Risk Assessment",
    description="Calculate combined risk across all dimensions using GPT-OSS-20B AI model"
)
async def assess_combined_risk_ai_endpoint(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> CombinedRiskResult:
    """
    AI-powered combined risk assessment across all 7 dimensions.
    
    Analyzes demographic, financial, medical, regional, claims, agent, and product risks.
    """
    try:
        # Extract all data
        demographic_data = extract_demographic_data(db, request.proposal_id)
        financial_data = extract_financial_data(db, request.proposal_id)
        medical_data = extract_medical_data(db, request.proposal_id)
        regional_data = extract_regional_data(db, request.proposal_id)
        claims_data = extract_claims_data(db, request.proposal_id)
        agent_data = extract_agent_data(db, request.proposal_id)
        product_data = extract_product_data(db, request.proposal_id)
        
        # Get AI assessments for each dimension
        demographic_result = assess_demographic_risk_ai(demographic_data)
        financial_result = assess_financial_risk_ai(financial_data)
        medical_result = assess_medical_risk_ai(medical_data)
        regional_result = assess_regional_risk_ai(regional_data)
        claims_result = assess_claims_risk_ai(claims_data)
        agent_result = assess_agent_risk_ai(agent_data)
        product_result = assess_product_risk_ai(product_data)
        
        # Combine results
        dimension_scores = [
            demographic_result,
            financial_result,
            medical_result,
            regional_result,
            claims_result,
            agent_result,
            product_result
        ]
        
        # Calculate weighted overall score
        overall_score = sum(
            result.risk_score * result.weight_in_overall
            for result in dimension_scores
        )
        
        # Determine overall risk level
        if overall_score < 25:
            overall_level = "LOW"
        elif overall_score < 50:
            overall_level = "MEDIUM"
        elif overall_score < 75:
            overall_level = "HIGH"
        else:
            overall_level = "CRITICAL"
        
        # Collect top risk factors
        all_factors = []
        for result in dimension_scores:
            for factor in result.risk_factors:
                all_factors.append(f"{factor} ({result.dimension.capitalize()})")
        top_factors = all_factors[:5]  # Top 5 risk factors
        
        # Determine underwriting decision
        if overall_level == "CRITICAL" or overall_score > 70:
            decision = "DECLINE"
            loading = 0
            recommendations = ["Decline application due to high risk"]
        elif overall_level == "HIGH":
            decision = "ACCEPT_WITH_LOADING"
            loading = int((overall_score - 50) * 2)  # 2% loading per point above 50
            recommendations = [f"Accept with {loading}% loading", "Request additional medical examination"]
        else:
            decision = "ACCEPT"
            loading = 0
            recommendations = ["Accept at standard rates"]
        
        return CombinedRiskResult(
            customer_id=demographic_data.customer_id,
            overall_risk_score=round(overall_score, 1),
            overall_risk_level=overall_level,
            dimension_scores=dimension_scores,
            top_risk_factors=top_factors,
            underwriting_decision=decision,
            recommended_loading=loading,
            recommendations=recommendations
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI assessment error: {str(e)}")
