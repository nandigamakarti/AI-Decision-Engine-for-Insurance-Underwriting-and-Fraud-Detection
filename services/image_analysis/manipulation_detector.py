import io
import numpy as np
from PIL import Image, ImageChops

def detect_manipulation(image_bytes: bytes) -> dict:
    """
    Performs pixel variance and Error Level Analysis (ELA) to detect image manipulation.
    ELA works by saving the image at a known quality and checking difference variances.
    """
    result = {
        "manipulation_detected": False,
        "ela_variance": 0.0,
        "issues": []
    }
    
    try:
        original = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Perform ELA: resave image at quality 90 in memory
        ela_buffer = io.BytesIO()
        original.save(ela_buffer, format="JPEG", quality=90)
        ela_buffer.seek(0)
        resaved = Image.open(ela_buffer)
        
        # Calculate pixel differences
        diff = ImageChops.difference(original, resaved)
        diff_arr = np.array(diff)
        
        # Compute statistical variance of differences
        variance = float(np.var(diff_arr))
        result["ela_variance"] = variance
        
        # If variance is abnormally high, it indicates localized compression discrepancies (edit spots)
        if variance > 45.0:
            result["manipulation_detected"] = True
            result["issues"].append("high_pixel_variance_detected")
        elif variance > 25.0:
            result["issues"].append("minor_compression_artifacts")
            
    except Exception as e:
        # Fallback if numpy/PIL operations fail (e.g. on non-standard formats)
        result["issues"].append(f"manipulation_check_failed: {str(e)}")
        
    return result
