from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ImageAnalysisRequest(BaseModel):
    claim_id: str = Field(..., description="Unique claim identifier", examples=["CLM_12345"])
    image_data: str = Field(..., description="Base64 encoded string of image bytes", examples=["iVBORw0KGgo..."])
    image_type: str = Field(..., description="Type of image uploaded", examples=["medical_report", "invoice", "damage_photo", "other"])

class AnalysisDetails(BaseModel):
    ai_artifacts: List[str] = []
    editing_traces: List[str] = []
    metadata_issues: List[str] = []

class ImageAnalysisResponse(BaseModel):
    claim_id: str
    is_ai_generated: bool
    confidence_score: float
    manipulation_detected: bool
    suspicion_level: str = Field(..., description="LOW|MEDIUM|HIGH|CRITICAL")
    analysis_details: AnalysisDetails
    recommendation: str = Field(..., description="ACCEPT|REVIEW|REJECT")
