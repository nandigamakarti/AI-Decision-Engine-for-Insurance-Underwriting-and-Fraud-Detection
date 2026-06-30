from pydantic import BaseModel, Field
from typing import List, Optional

class MedicalCodeLookupResponse(BaseModel):
    code: str
    code_type: str = Field(..., description="ICD10|CPT|NDC|HCPCS")
    description: str
    risk_weight: float
    category: str
    cost_estimate: Optional[float] = None
    risk_class: Optional[str] = None

class MedicalCodeAnalysisRequest(BaseModel):
    icd10_codes: List[str] = Field(default_factory=list, description="Array of ICD-10 diagnosis codes")
    cpt_codes: List[str] = Field(default_factory=list, description="Array of CPT procedure codes")
    ndc_codes: List[str] = Field(default_factory=list, description="Array of NDC medication codes")
    hcpcs_codes: List[str] = Field(default_factory=list, description="Array of HCPCS DME/service codes")

class MedicalCodeAnalysisResponse(BaseModel):
    overall_medical_risk_score: float
    total_estimated_cost: float
    high_risk_factors: List[str]
    recommendations: List[str]
