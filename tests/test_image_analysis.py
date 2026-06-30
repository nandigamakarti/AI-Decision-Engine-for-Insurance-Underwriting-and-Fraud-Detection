import base64
import io
from PIL import Image
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def generate_test_image_base64():
    # Helper to generate a valid minimal JPEG image encoded in base64
    img = Image.new("RGB", (10, 10), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    return base64.b64encode(byte_im).decode("utf-8")

def test_analyze_image_success():
    image_base64 = generate_test_image_base64()
    payload = {
        "claim_id": "CLM_12345",
        "image_data": image_base64,
        "image_type": "medical_report"
    }
    
    response = client.post("/api/image-analysis", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["claim_id"] == "CLM_12345"
    assert "is_ai_generated" in data
    assert "confidence_score" in data
    assert "manipulation_detected" in data
    assert data["suspicion_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert "analysis_details" in data
    assert "recommendation" in data
    assert data["recommendation"] in ["ACCEPT", "REVIEW", "REJECT"]

def test_analyze_image_invalid_base64():
    payload = {
        "claim_id": "CLM_54321",
        "image_data": "invalid-base64-content!#@",
        "image_type": "invoice"
    }
    response = client.post("/api/image-analysis", json=payload)
    # The route catches decoding errors and returns 422
    assert response.status_code == 422
    assert "detail" in response.json()

def test_analyze_image_invalid_image_bytes():
    # This string is valid base64 but does not represent a valid image file.
    # The detector handles this gracefully by flagging parsing issues in `analysis_details`.
    non_image_base64 = base64.b64encode(b"not an image file").decode("utf-8")
    payload = {
        "claim_id": "CLM_67890",
        "image_data": non_image_base64,
        "image_type": "other"
    }
    
    response = client.post("/api/image-analysis", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["claim_id"] == "CLM_67890"
    # Should flag issues due to parsing failure
    issues = data["analysis_details"]["metadata_issues"]
    assert "exif_parsing_failed" in issues
