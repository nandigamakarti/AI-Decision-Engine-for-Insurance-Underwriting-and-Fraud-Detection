"""Risk assessment API routes - Database-driven version."""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from db import get_db
from data.schemas.result_schema import RiskCalculationResult, CombinedRiskResult
from models.risk_calculators.demographic_risk import calculate_demographic_risk
from models.risk_calculators.financial_risk import calculate_financial_risk
from models.risk_calculators.medical_risk import calculate_medical_risk
from models.risk_calculators.regional_risk import calculate_regional_risk
from models.risk_calculators.claims_risk import calculate_claims_risk
from models.risk_calculators.agent_risk import calculate_agent_risk
from models.risk_calculators.product_risk import calculate_product_risk
from models.risk_calculators.combined_risk import calculate_combined_risk

from services.data_extraction import (
    extract_demographic_data,
    extract_financial_data,
    extract_medical_data,
    extract_regional_data,
    extract_claims_data,
    extract_agent_data,
    extract_product_data
)

router = APIRouter(prefix="/api/risk", tags=["Risk Assessment"])


class RiskAssessmentRequest(BaseModel):
    """Request model for risk assessment endpoints."""
    proposal_id: str = Field(
        ..., 
        description="Unique proposal identifier from database",
        examples=["PROP001", "PROP002", "PROP2024001"]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "proposal_id": "PROP001"
            },
            "description": "To get available proposal IDs, call GET /api/proposals/ids first"
        }


@router.post(
    "/demographic",
    response_model=RiskCalculationResult,
    summary="Assess Demographic Risk",
    description="Calculate risk score based on age, lifestyle, and socioeconomic factors from database"
)
async def assess_demographic_risk(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """
    Assess demographic risk factors from database.
    
    **Weight:** 15% in overall risk calculation
    
    **Data Sources:**
    - MemberDetails: age, gender, marital_status
    - ProductSubQuestionMapping: smoking, alcohol
    - LeadDetails: location
    
    **Returns:** Risk score (0-100), risk level, factors, and recommendations
    """
    try:
        data = extract_demographic_data(db, request.proposal_id)
        return calculate_demographic_risk(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating demographic risk: {str(e)}")


@router.post(
    "/financial",
    response_model=RiskCalculationResult,
    summary="Assess Financial Risk",
    description="Calculate risk score based on credit, debt, income, and financial history from database"
)
async def assess_financial_risk(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """
    Assess financial risk factors from database.
    
    **Weight:** 20% in overall risk calculation
    
    **Data Sources:**
    - ProposalDetails: annual_income, sum_insured
    - KYCDetails: risk_level (maps to credit score)
    - PaymentDetails: payment history
    
    **Returns:** Risk score (0-100), risk level, factors, and recommendations
    """
    try:
        data = extract_financial_data(db, request.proposal_id)
        return calculate_financial_risk(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating financial risk: {str(e)}")


@router.post(
    "/medical",
    response_model=RiskCalculationResult,
    summary="Assess Medical Risk",
    description="Calculate risk score based on conditions, medications, vitals from database"
)
async def assess_medical_risk(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """
    Assess medical risk factors from database.
    
    **Weight:** 30% in overall risk calculation (HIGHEST)
    
    **Data Sources:**
    - ChronicDiseaseDetails: pre-existing conditions
    - ProductSubQuestionMapping: medications, surgeries
    - MemberDetails: height, weight (for BMI)
    
    **Returns:** Risk score (0-100), risk level, factors, and recommendations
    """
    try:
        data = extract_medical_data(db, request.proposal_id)
        return calculate_medical_risk(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating medical risk: {str(e)}")


@router.post(
    "/regional",
    response_model=RiskCalculationResult,
    summary="Assess Regional Risk",
    description="Calculate risk score based on location, healthcare access from database"
)
async def assess_regional_risk(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """
    Assess regional/geographic risk factors from database.
    
    **Weight:** 10% in overall risk calculation
    
    **Data Sources:**
    - LeadDetails: city, state, zone
    - HospitalMaster: network hospitals proximity
    - BlackListedHospitals: fraud risk
    
    **Returns:** Risk score (0-100), risk level, factors, and recommendations
    """
    try:
        data = extract_regional_data(db, request.proposal_id)
        return calculate_regional_risk(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating regional risk: {str(e)}")


@router.post(
    "/claims",
    response_model=RiskCalculationResult,
    summary="Assess Claims History Risk",
    description="Calculate risk score based on claims frequency, amounts, and fraud indicators from database"
)
async def assess_claims_risk(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """
    Assess claims history risk factors from database.
    
    **Weight:** 15% in overall risk calculation
    
    **Data Sources:**
    - ClaimDetails: claims history
    - BlackListedHospitals: fraud detection
    
    **Returns:** Risk score (0-100), risk level, factors, and recommendations
    """
    try:
        data = extract_claims_data(db, request.proposal_id)
        return calculate_claims_risk(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating claims risk: {str(e)}")


@router.post(
    "/agent",
    response_model=RiskCalculationResult,
    summary="Assess Agent/Channel Risk",
    description="Calculate risk score based on agent performance, compliance from database"
)
async def assess_agent_risk(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """
    Assess agent/distribution channel risk factors from database.
    
    **Weight:** 5% in overall risk calculation
    
    **Data Sources:**
    - AgentDetails: agent profile
    - AgentRiskScores: pre-calculated metrics
    - AnnualClubPerformance: performance indicators
    
    **Returns:** Risk score (0-100), risk level, factors, and recommendations
    """
    try:
        data = extract_agent_data(db, request.proposal_id)
        return calculate_agent_risk(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating agent risk: {str(e)}")


@router.post(
    "/product",
    response_model=RiskCalculationResult,
    summary="Assess Product/Underwriting Risk",
    description="Calculate risk score based on coverage, pricing from database"
)
async def assess_product_risk(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> RiskCalculationResult:
    """
    Assess product/underwriting risk factors from database.
    
    **Weight:** 5% in overall risk calculation
    
    **Data Sources:**
    - ProductDetails: product features
    - ProposalDetails: sum insured, income
    - PortabilityDetails: portability info
    
    **Returns:** Risk score (0-100), risk level, factors, and recommendations
    """
    try:
        data = extract_product_data(db, request.proposal_id)
        return calculate_product_risk(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating product risk: {str(e)}")


@router.post(
    "/combined",
    response_model=CombinedRiskResult,
    summary="Assess Combined Risk Across All Dimensions",
    description="Calculate weighted overall risk score from database and generate underwriting decision"
)
async def assess_combined_risk(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
) -> CombinedRiskResult:
    """
    Assess combined risk across all 7 dimensions with weighted scoring from database.
    
    **Weighted Formula:**
    - Medical: 30% (highest)
    - Financial: 20%
    - Demographic: 15%
    - Claims: 15%
    - Regional: 10%
    - Agent: 5%
    - Product: 5%
    
    **Underwriting Decision:**
    - 0-49: ACCEPT (0-10% loading)
    - 50-69: REVIEW (25% loading)
    - 70-100: DECLINE
    
    **Returns:** Overall score, decision, loading %, top risk factors, and recommendations
    """
    try:
        # Extract all 7 dimensions from database
        demographic = extract_demographic_data(db, request.proposal_id)
        financial = extract_financial_data(db, request.proposal_id)
        medical = extract_medical_data(db, request.proposal_id)
        regional = extract_regional_data(db, request.proposal_id)
        claims = extract_claims_data(db, request.proposal_id)
        agent = extract_agent_data(db, request.proposal_id)
        product = extract_product_data(db, request.proposal_id)
        
        # Calculate combined risk
        return calculate_combined_risk(
            demographic=demographic,
            financial=financial,
            medical=medical,
            regional=regional,
            claims=claims,
            agent=agent,
            product=product
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating combined risk: {str(e)}")
