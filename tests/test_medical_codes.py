from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_lookup_icd10_success():
    response = client.get("/api/medical-codes/icd10/I10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "I10"
    assert data["code_type"] == "ICD10"
    assert data["description"] == "Essential hypertension"
    assert data["risk_weight"] == 50.0
    assert data["category"] == "cardiovascular"

def test_lookup_cpt_success():
    response = client.get("/api/medical-codes/cpt/33510")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "33510"
    assert data["code_type"] == "CPT"
    assert "bypass" in data["description"].lower()
    assert data["cost_estimate"] == 75000.0

def test_lookup_ndc_success():
    response = client.get("/api/medical-codes/ndc/00004-0008-01")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "00004-0008-01"
    assert data["code_type"] == "NDC"
    assert "warfarin" in data["description"].lower()
    assert data["risk_class"] == "HIGH"

def test_lookup_hcpcs_success():
    response = client.get("/api/medical-codes/hcpcs/E0601")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "E0601"
    assert data["code_type"] == "HCPCS"
    assert "cpap" in data["description"].lower()
    assert data["cost_estimate"] == 800.0

def test_lookup_not_found():
    response = client.get("/api/medical-codes/icd10/NON_EXISTENT_CODE")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_analyze_medical_code_batch_empty():
    payload = {
        "icd10_codes": [],
        "cpt_codes": [],
        "ndc_codes": [],
        "hcpcs_codes": []
    }
    response = client.post("/api/medical-codes/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["overall_medical_risk_score"] == 0.0
    assert data["total_estimated_cost"] == 0.0
    assert len(data["high_risk_factors"]) == 0
    assert "standard medical underwriting conditions" in data["recommendations"][0]

def test_analyze_medical_code_batch_multiple():
    payload = {
        "icd10_codes": ["I10", "E11.9"],  # risk_weights: 50, 65
        "cpt_codes": ["93000"],          # ECG (cost: 150, risk_weight: 5)
        "ndc_codes": ["00004-0008-01"],  # Warfarin (risk_weight: 70, HIGH)
        "hcpcs_codes": ["E0601"]         # CPAP (cost: 800, risk_weight: 40)
    }
    response = client.post("/api/medical-codes/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Let's verify calculation logic:
    # risk_weights = [50 (I10), 65 (E11.9), 5 (93000), 70 (Warfarin), 40 (CPAP)]
    # max_weight = 70
    # others = [50, 65, 5, 40], sum of others = 160
    # others_contrib = 160 * 0.10 = 16
    # overall_score = min(100, 70 + 16) = 86
    assert data["overall_medical_risk_score"] == 86.0
    
    # total_estimated_cost = 150 (93000) + 800 (E0601) = 950
    assert data["total_estimated_cost"] == 950.0
    
    # High risk factors (risk >= 65 for ICD10, >=60 for CPT/NDC, >=50 for HCPCS)
    # E11.9 (65) -> yes
    # Warfarin (70) -> yes
    # I10 (50) -> no
    # 93000 (5) -> no
    # E0601 (40) -> no
    assert len(data["high_risk_factors"]) == 2
    assert any("E11.9" in f for f in data["high_risk_factors"])
    assert any("00004-0008-01" in f for f in data["high_risk_factors"])
    
    # overall_score >= 75 -> decline standard issue, audit, loading
    assert len(data["recommendations"]) == 3
    assert any("decline" in r.lower() for r in data["recommendations"])
