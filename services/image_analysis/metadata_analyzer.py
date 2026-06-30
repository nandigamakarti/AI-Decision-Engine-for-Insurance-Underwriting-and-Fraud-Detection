import io
import logging
from PIL import Image
from PIL.ExifTags import TAGS

logger = logging.getLogger(__name__)

def analyze_metadata(image_bytes: bytes) -> dict:
    """
    Extracts and analyzes EXIF metadata from raw image bytes.
    Detects editing software signatures, missing EXIF information, and date modifications.
    """
    details = {
        "has_exif": False,
        "editing_software": None,
        "date_modified": None,
        "camera_make": None,
        "camera_model": None,
        "issues": []
    }
    
    try:
        image = Image.open(io.BytesIO(image_bytes))
        exif_data = image._getexif()
        
        if not exif_data:
            details["issues"].append("missing_exif")
            return details
            
        details["has_exif"] = True
        
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            
            if tag_name == "Software":
                details["editing_software"] = str(value)
                details["issues"].append("software_signature_detected")
            elif tag_name == "DateTime" or tag_name == "DateTimeOriginal":
                details["date_modified"] = str(value)
            elif tag_name == "Make":
                details["camera_make"] = str(value)
            elif tag_name == "Model":
                details["camera_model"] = str(value)
                
        # If camera information is completely missing despite EXIF presence, flag it
        if not details["camera_make"] and not details["camera_model"]:
            details["issues"].append("missing_device_metadata")
            
    except Exception as e:
        logger.error(f"Error parsing metadata: {e}")
        details["issues"].append("exif_parsing_failed")
        
    return details
