import logging
from services.image_analysis.metadata_analyzer import analyze_metadata
from services.image_analysis.manipulation_detector import detect_manipulation
from services.image_analysis.ai_detector import detect_ai_generation

logger = logging.getLogger(__name__)

def analyze_image(claim_id: str, image_bytes: bytes, image_type: str = "other") -> dict:
    """
    Orchestrates the full image analysis pipeline.
    Combines EXIF metadata analysis, error level compression reviews, and AI noise checks.
    """
    logger.info(f"Analyzing image for claim: {claim_id}, type: {image_type}")
    
    # Run detectors
    metadata_res = analyze_metadata(image_bytes)
    manipulation_res = detect_manipulation(image_bytes)
    ai_res = detect_ai_generation(image_bytes)
    
    # Compile details
    ai_artifacts = ai_res["issues"]
    editing_traces = manipulation_res["issues"]
    metadata_issues = metadata_res["issues"]
    
    # Aggregate triggers to decide suspicion level
    is_ai = ai_res["is_ai_generated"]
    is_manipulated = manipulation_res["manipulation_detected"]
    
    # Calculate confidence score
    confidence_score = max(ai_res["ai_score"], 0.80 if is_manipulated else 0.10)
    
    # Decide suspicion level and recommendation
    suspicion_level = "LOW"
    recommendation = "ACCEPT"
    
    if is_ai:
        suspicion_level = "CRITICAL"
        recommendation = "REJECT"
    elif is_manipulated:
        suspicion_level = "HIGH"
        recommendation = "REVIEW"
    elif len(metadata_issues) > 1 or len(editing_traces) > 0:
        suspicion_level = "MEDIUM"
        recommendation = "REVIEW"
        
    return {
      "claim_id": claim_id,
      "is_ai_generated": is_ai,
      "confidence_score": confidence_score,
      "manipulation_detected": is_manipulated,
      "suspicion_level": suspicion_level,
      "analysis_details": {
        "ai_artifacts": ai_artifacts,
        "editing_traces": editing_traces,
        "metadata_issues": metadata_issues
      },
      "recommendation": recommendation
    }
