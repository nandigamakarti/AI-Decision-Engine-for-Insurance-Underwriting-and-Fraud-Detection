import logging
from fastapi import APIRouter, HTTPException
from api.medical_code_models import (
    MedicalCodeLookupResponse,
    MedicalCodeAnalysisRequest,
    MedicalCodeAnalysisResponse
)
from data.medical_codes import lookup_code, analyze_medical_codes

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/medical-codes", tags=["Medical Codes"])

@router.get(
    "/{code_type}/{code}",
    response_model=MedicalCodeLookupResponse,
    summary="Look Up Medical Code Details",
    description="Query details, descriptions, and risk weight modifiers for specific ICD-10, CPT, NDC, or HCPCS codes."
)
async def get_medical_code_details(code_type: str, code: str) -> MedicalCodeLookupResponse:
    """Lookup medical code metadata from static databases."""
    match = lookup_code(code_type, code)
    if not match:
        raise HTTPException(
            status_code=404,
            detail=f"Medical code '{code}' of type '{code_type}' not found in database."
        )
    return MedicalCodeLookupResponse(**match)

@router.post(
    "/analyze",
    response_model=MedicalCodeAnalysisResponse,
    summary="Batch Analyze Medical Codes",
    description="Evaluates a bundle of diagnosis (ICD-10), procedure (CPT), medication (NDC), and DME (HCPCS) codes to calculate aggregate risk and cost bounds."
)
async def analyze_medical_code_batch(request: MedicalCodeAnalysisRequest) -> MedicalCodeAnalysisResponse:
    """Analyze a batch of diagnostic and procedure codes."""
    try:
        analysis = analyze_medical_codes(
            icd10_codes=request.icd10_codes,
            cpt_codes=request.cpt_codes,
            ndc_codes=request.ndc_codes,
            hcpcs_codes=request.hcpcs_codes
        )
        return MedicalCodeAnalysisResponse(**analysis)
    except Exception as e:
        logger.error(f"Batch analysis route failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Medical codes batch analysis failed: {str(e)}"
        )
