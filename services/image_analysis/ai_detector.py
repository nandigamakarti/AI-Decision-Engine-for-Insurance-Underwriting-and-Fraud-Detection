import io
import numpy as np
from PIL import Image

def detect_ai_generation(image_bytes: bytes) -> dict:
    """
    Analyzes noise patterns and high-frequency pixel artifacts to detect AI-generated images.
    """
    result = {
        "is_ai_generated": False,
        "ai_score": 0.0,
        "issues": []
    }
    
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("L") # convert to grayscale
        img_arr = np.array(img)
        
        # Analyze grid noise by comparing adjacent pixels in high-contrast segments
        diff_h = np.abs(img_arr[:, :-1] - img_arr[:, 1:])
        diff_v = np.abs(img_arr[:-1, :] - img_arr[1:, :])
        
        # AI images tend to have unnaturally uniform high-frequency grids (due to diffusion scaling)
        grid_uniformity_h = np.std(diff_h)
        grid_uniformity_v = np.std(diff_v)
        
        avg_std = (grid_uniformity_h + grid_uniformity_v) / 2
        
        # Diffusion artifacts heuristically produce very specific variance ranges
        # We combine this with pixel intensity distributions
        hist, _ = np.histogram(img_arr, bins=10, density=True)
        extreme_pixels_ratio = hist[0] + hist[-1]
        
        ai_score = 0.1 # Baseline
        
        # If noise uniformity is extremely low (meaning pixel gradients are artificially clean/perfect)
        if avg_std < 5.0:
            ai_score += 0.4
            result["issues"].append("suspiciously_smooth_gradients")
            
        # Extreme contrast histograms typical of synthetic render pipelines
        if extreme_pixels_ratio > 0.45:
            ai_score += 0.35
            result["issues"].append("synthetic_contrast_signature")
            
        result["ai_score"] = min(1.0, max(0.0, ai_score))
        if result["ai_score"] >= 0.70:
            result["is_ai_generated"] = True
            
    except Exception as e:
        result["issues"].append(f"ai_pattern_check_failed: {str(e)}")
        
    return result
