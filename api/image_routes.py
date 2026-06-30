import base64
import logging
from fastapi import APIRouter, HTTPException
from api.image_models import ImageAnalysisRequest, ImageAnalysisResponse
from services.image_analysis import analyze_image

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Image Analysis"])

@router.post(
    "/image-analysis",
    response_model=ImageAnalysisResponse,
    summary="Analyze Claim Document Image",
    description="Evaluates submitted claim images (PDF/invoice/medical report) to detect AI generation, editing manipulations, or EXIF anomalies."
)
async def analyze_claim_image(request: ImageAnalysisRequest) -> ImageAnalysisResponse:
    """
    Image Analysis API Route.
    Decodes base64 payload and runs EXIF and pixel variance audits.
    """
    try:
        # Decode base64 image data
        try:
            image_bytes = base64.b64decode(request.image_data, validate=True)
        except Exception:
            raise HTTPException(
                status_code=422,
                detail="Invalid base64 encoding for image_data"
            )
            
        # Run detection pipeline
        analysis_result = analyze_image(
            claim_id=request.claim_id,
            image_bytes=image_bytes,
            image_type=request.image_type
        )
        
        return ImageAnalysisResponse(**analysis_result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image analysis route failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Image analysis failed: {str(e)}"
        )
