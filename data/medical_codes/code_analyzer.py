import logging
from typing import List, Dict, Any

from data.medical_codes.icd10_codes import ICD10_CODES
from data.medical_codes.cpt_codes import CPT_CODES
from data.medical_codes.ndc_codes import NDC_CODES
from data.medical_codes.hcpcs_codes import HCPCS_CODES

logger = logging.getLogger(__name__)

def lookup_code(code_type: str, code: str) -> Dict[str, Any] | None:
    """
    Looks up a medical code in the respective database.
    Supports case-insensitive matching and fuzzy checking.
    """
    code_type = code_type.lower()
    code = code.strip()
    
    if code_type in ("icd10", "icd-10"):
        # Match directly or case-insensitive
        match = ICD10_CODES.get(code) or next((v for k, v in ICD10_CODES.items() if k.lower() == code.lower()), None)
        if match:
            return {"code": code, "code_type": "ICD10", **match}
            
    elif code_type in ("cpt", "cpt-4"):
        match = CPT_CODES.get(code)
        if match:
            return {"code": code, "code_type": "CPT", **match}
            
    elif code_type in ("ndc", "ndc-med"):
        match = NDC_CODES.get(code)
        if match:
            return {"code": code, "code_type": "NDC", **match}
            
    elif code_type in ("hcpcs", "hcpcs-dme"):
        match = HCPCS_CODES.get(code)
        if match:
            return {"code": code, "code_type": "HCPCS", **match}
            
    return None

def analyze_medical_codes(
    icd10_codes: List[str] = None,
    cpt_codes: List[str] = None,
    ndc_codes: List[str] = None,
    hcpcs_codes: List[str] = None
) -> Dict[str, Any]:
    """
    Analyzes a batch of medical codes to calculate overall medical risk scores and cost estimates.
    """
    icd10_list = icd10_codes or []
    cpt_list = cpt_codes or []
    ndc_list = ndc_codes or []
    hcpcs_list = hcpcs_codes or []
    
    risk_weights = []
    estimated_cost = 0.0
    high_risk_factors = []
    
    # Process ICD-10
    for code in icd10_list:
        match = lookup_code("icd10", code)
        if match:
            risk_weights.append(match["risk_weight"])
            if match["risk_weight"] >= 65:
                high_risk_factors.append(f"Diagnosis: {match['description']} ({code})")
                
    # Process CPT
    for code in cpt_list:
        match = lookup_code("cpt", code)
        if match:
            risk_weights.append(match["risk_weight"])
            estimated_cost += match.get("cost_estimate", 0.0)
            if match["risk_weight"] >= 60:
                high_risk_factors.append(f"High-risk procedure: {match['description']} ({code})")
                
    # Process NDC
    for code in ndc_list:
        match = lookup_code("ndc", code)
        if match:
            risk_weights.append(match["risk_weight"])
            if match["risk_weight"] >= 60:
                high_risk_factors.append(f"Medication: {match['description']} ({code})")
                
    # Process HCPCS
    for code in hcpcs_list:
        match = lookup_code("hcpcs", code)
        if match:
            risk_weights.append(match["risk_weight"])
            estimated_cost += match.get("cost_estimate", 0.0)
            if match["risk_weight"] >= 50:
                high_risk_factors.append(f"Equipment/DME: {match['description']} ({code})")
                
    # Calculate Overall Medical Risk Score using co-morbidity index logic
    if not risk_weights:
        overall_score = 0.0
    else:
        max_weight = max(risk_weights)
        others_contrib = sum(w for w in risk_weights if w != max_weight) * 0.10
        overall_score = min(100.0, max_weight + others_contrib)
        
    # Recommendations
    recommendations = []
    if overall_score >= 75:
        recommendations.extend(["Decline standard policy issue", "Refer to medical director audit panel", "Apply 50%+ high-risk premium loading"])
    elif overall_score >= 50:
        recommendations.extend(["Apply 20-30% premium loading", "Enforce 24-month pre-existing condition waiting period", "Request doctor checkup reports"])
    else:
        recommendations.append("Approve under standard medical underwriting conditions")
        
    return {
        "overall_medical_risk_score": float(round(overall_score, 2)),
        "total_estimated_cost": float(estimated_cost),
        "high_risk_factors": high_risk_factors,
        "recommendations": recommendations
    }
