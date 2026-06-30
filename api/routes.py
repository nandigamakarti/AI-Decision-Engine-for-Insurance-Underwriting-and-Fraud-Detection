"""
API routes for risk assessment endpoints.
"""

import logging
from fastapi import APIRouter, HTTPException
from api.models import CustomerDataInput, RiskAssessmentOutput
from services.risk_assessment import RiskAssessmentService
from services.ollama_service import ollama_service

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api", tags=["risk-assessment"])

# Initialize service
risk_service = RiskAssessmentService()


@router.post(
    "/risk-assessment",
    response_model=RiskAssessmentOutput,
    summary="Assess Customer Risk",
    description="Accepts comprehensive customer data and returns a detailed AI-generated risk assessment"
)
async def assess_customer_risk(customer_data: CustomerDataInput) -> RiskAssessmentOutput:
    """
    Risk Assessment Endpoint - AI-Powered by Ollama.

    This endpoint accepts detailed customer information including personal, health,
    financial, and claims history data, and uses an Ollama AI model to generate
    a comprehensive risk assessment with structured JSON output.

    **Request Body:**
    - `customer_id` (optional): Unique identifier for the customer
    - `personal_info` (required): Personal information including name, DOB, contact details
    - `health_info` (optional): Health conditions, medications, lifestyle factors
    - `financial_info` (optional): Income, employment, credit score, debts
    - `claims_history` (optional): Previous claims and claim amounts
    - `additional_data` (optional): Any other relevant customer data

    **Response:**
    Returns a RiskAssessmentOutput object containing:
    - `overall_risk_level`: LOW, MEDIUM, HIGH, or CRITICAL (AI-determined)
    - `overall_risk_score`: Numerical score from 0-100 (AI-generated)
    - `risk_factors`: Detailed list of identified risk factors with scores
    - `recommendations`: AI-generated underwriting recommendations
    - `assessment_date`: Timestamp of the assessment
    - `additional_notes`: Additional insights from the AI model

    **Example Request:**
    ```json
    {
        "customer_id": "CUST123",
        "personal_info": {
            "first_name": "John",
            "last_name": "Doe",
            "age": 45,
            "email": "john@example.com"
        },
        "health_info": {
            "smoker": false,
            "bmi": 24.5,
            "health_conditions": ["hypertension"]
        },
        "financial_info": {
            "annual_income": 75000,
            "credit_score": 750,
            "employment_status": "Employed"
        }
    }
    ```

    **Response Example:**
    ```json
    {
        "customer_id": "CUST123",
        "overall_risk_level": "MEDIUM",
        "overall_risk_score": 45.0,
        "risk_factors": [
            {
                "factor_name": "Pre-existing Health Conditions",
                "risk_level": "MEDIUM",
                "score": 45,
                "description": "Customer has hypertension which requires ongoing management"
            }
        ],
        "recommendations": [
            "Request medical report from treating physician",
            "Verify current medication compliance"
        ],
        "assessment_date": "2025-11-20T10:30:00.000000",
        "additional_notes": "Overall profile is favorable with stable employment and good credit"
    }
    ```
    """
    try:
        logger.info(f"Received risk assessment request for customer: {customer_data.customer_id}")
        
        # Check Ollama connectivity first
        if not ollama_service.health_check():
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "Ollama service unavailable",
                    "message": f"Cannot connect to Ollama at {ollama_service.base_url}. "
                               "Make sure Ollama is running with 'ollama serve'",
                    "ollama_url": ollama_service.base_url
                }
            )
        
        # Perform risk assessment using Ollama
        result = risk_service.assess_risk(customer_data)
        
        logger.info(
            f"Risk assessment completed - Customer: {customer_data.customer_id}, "
            f"Risk Level: {result.overall_risk_level}, Score: {result.overall_risk_score}"
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during risk assessment: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Risk assessment failed",
                "message": str(e)
            }
        )


@router.get("/health", summary="Health Check", description="Check if the API is running")
async def health_check() -> dict:
    """
    Health Check Endpoint.

    Returns a simple status message indicating the API is operational.

    **Response:**
    ```json
    {
        "status": "healthy",
        "service": "Risk Assessment Engine"
    }
    ```
    """
    return {
        "status": "healthy",
        "service": "Risk Assessment Engine"
    }
