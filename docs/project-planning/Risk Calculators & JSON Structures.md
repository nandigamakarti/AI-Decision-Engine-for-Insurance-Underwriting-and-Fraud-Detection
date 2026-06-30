
# CLAUDE.md - Developer 2 (Week Assignment)

## Your Focus Areas

1. **Modular JSON Data Structures for Each Risk Dimension**
2. **Individual Risk Calculators for Each Dimension**
3. **Combined Risk Calculator with Weighted Scoring**

---

## 1. Modular Risk Dimension JSON Structures

### Objective

Create separate, well-defined JSON schemas for each of 7 risk dimensions, each with its own API endpoint.

---

### 1.1 Demographic Risk JSON

**File:** `data/schemas/demographic_schema.py`

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class DemographicData(BaseModel):
    """Demographic risk factors"""
    customer_id: str

    # Identity
    first_name: str
    last_name: str
    date_of_birth: date
    age: int = Field(ge=0, le=120)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")

    # Lifestyle
    smoking_status: str = Field(..., pattern="^(Never|Former|Current)$")
    alcohol_consumption: str = Field(..., pattern="^(None|Moderate|Heavy)$")
    exercise_frequency: str = Field(..., pattern="^(Sedentary|Light|Moderate|Active)$")

    # Socioeconomic
    education_level: str = Field(..., pattern="^(High School|Bachelor|Master|Doctorate|Other)$")
    occupation: Optional[str] = None
    marital_status: str = Field(..., pattern="^(Single|Married|Divorced|Widowed)$")

    # Household
    household_size: int = Field(ge=1, le=20)
    dependents: int = Field(ge=0)

    # Geographic (basic)
    zip_code: str
    state: str

# Example JSON
{
  "customer_id": "CUST_001",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1980-05-15",
  "age": 44,
  "gender": "Male",
  "smoking_status": "Never",
  "alcohol_consumption": "Moderate",
  "exercise_frequency": "Moderate",
  "education_level": "Bachelor",
  "occupation": "Software Engineer",
  "marital_status": "Married",
  "household_size": 4,
  "dependents": 2,
  "zip_code": "10001",
  "state": "NY"
}
```

**Endpoint:** `POST /api/risk/demographic`

---

### 1.2 Financial Risk JSON

**File:** `data/schemas/financial_schema.py`

```python
class FinancialData(BaseModel):
    """Financial risk factors"""
    customer_id: str

    # Income
    annual_income: float = Field(ge=0)
    income_stability: str = Field(..., pattern="^(Stable|Variable|Unstable)$")
    employment_status: str = Field(..., pattern="^(Employed|Self-Employed|Unemployed|Retired)$")
    years_employed: Optional[int] = Field(ge=0)

    # Credit
    credit_score: int = Field(ge=300, le=850)
    credit_history_length: int = Field(ge=0, description="Years")

    # Debt
    total_debt: float = Field(ge=0)
    debt_to_income_ratio: float = Field(ge=0, le=10)  # Ratio
    mortgage_status: str = Field(..., pattern="^(Own|Rent|Mortgage)$")

    # Assets
    liquid_assets: float = Field(ge=0)
    total_assets: float = Field(ge=0)

    # Financial History
    bankruptcy_history: bool = False
    years_since_bankruptcy: Optional[int] = None
    late_payments_12mo: int = Field(ge=0)

# Example JSON
{
  "customer_id": "CUST_001",
  "annual_income": 125000,
  "income_stability": "Stable",
  "employment_status": "Employed",
  "years_employed": 10,
  "credit_score": 750,
  "credit_history_length": 15,
  "total_debt": 50000,
  "debt_to_income_ratio": 0.4,
  "mortgage_status": "Mortgage",
  "liquid_assets": 25000,
  "total_assets": 300000,
  "bankruptcy_history": false,
  "late_payments_12mo": 0
}
```

**Endpoint:** `POST /api/risk/financial`

---

### 1.3 PED (Medical) Risk JSON

**File:** `data/schemas/medical_schema.py`

```python
from typing import List

class MedicalCondition(BaseModel):
    icd10_code: str
    description: str
    diagnosed_date: date
    treatment_status: str = Field(..., pattern="^(Active|Controlled|Resolved)$")

class Medication(BaseModel):
    ndc_code: str
    name: str
    dosage: str
    frequency: str

class Procedure(BaseModel):
    cpt_code: str
    description: str
    procedure_date: date

class MedicalData(BaseModel):
    """Pre-existing disease (PED) and medical risk factors"""
    customer_id: str

    # Conditions
    conditions: List[MedicalCondition] = []

    # Medications
    current_medications: List[Medication] = []

    # Procedures
    past_procedures: List[Procedure] = []

    # Vitals
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    bmi: float = Field(ge=10, le=100)
    blood_pressure_systolic: int = Field(ge=60, le=250)
    blood_pressure_diastolic: int = Field(ge=40, le=150)

    # Family History
    family_history_cancer: bool = False
    family_history_heart_disease: bool = False
    family_history_diabetes: bool = False

# Example JSON
{
  "customer_id": "CUST_001",
  "conditions": [
    {
      "icd10_code": "I10",
      "description": "Essential hypertension",
      "diagnosed_date": "2018-03-15",
      "treatment_status": "Controlled"
    }
  ],
  "current_medications": [
    {
      "ndc_code": "00093-7169-01",
      "name": "Lisinopril",
      "dosage": "10mg",
      "frequency": "Daily"
    }
  ],
  "past_procedures": [],
  "height_cm": 178,
  "weight_kg": 82,
  "bmi": 25.9,
  "blood_pressure_systolic": 128,
  "blood_pressure_diastolic": 82,
  "family_history_cancer": false,
  "family_history_heart_disease": true,
  "family_history_diabetes": false
}
```

**Endpoint:** `POST /api/risk/medical`

---

### 1.4 Regional Risk JSON

**File:** `data/schemas/regional_schema.py`

```python
class RegionalData(BaseModel):
    """Geographic and regional risk factors"""
    customer_id: str

    # Location
    zip_code: str
    city: str
    state: str
    county: Optional[str] = None

    # Healthcare Access
    nearest_hospital_km: float = Field(ge=0)
    hospitals_within_25km: int = Field(ge=0)
    specialists_available: bool

    # Environmental
    air_quality_index: int = Field(ge=0, le=500)
    natural_disaster_zone: bool
    disaster_type: Optional[str] = None  # "Hurricane|Earthquake|Flood|None"

    # Socioeconomic
    median_income_area: float = Field(ge=0)
    crime_rate_per_1000: float = Field(ge=0)
    unemployment_rate: float = Field(ge=0, le=100)

    # Cost of Living
    healthcare_cost_index: float = Field(ge=0)  # 100 = national average

# Example JSON
{
  "customer_id": "CUST_001",
  "zip_code": "10001",
  "city": "New York",
  "state": "NY",
  "county": "Manhattan",
  "nearest_hospital_km": 2.5,
  "hospitals_within_25km": 15,
  "specialists_available": true,
  "air_quality_index": 45,
  "natural_disaster_zone": false,
  "median_income_area": 85000,
  "crime_rate_per_1000": 15.2,
  "unemployment_rate": 4.5,
  "healthcare_cost_index": 135
}
```

**Endpoint:** `POST /api/risk/regional`

---

### 1.5 Claims History Risk JSON

**File:** `data/schemas/claims_schema.py`

```python
class Claim(BaseModel):
    claim_id: str
    claim_date: date
    claim_type: str  # "Medical|Dental|Vision|Other"
    claim_amount: float
    approved_amount: float
    status: str  # "Approved|Denied|Pending"

class ClaimsData(BaseModel):
    """Claims history risk factors"""
    customer_id: str

    # Claims History
    total_claims_count: int = Field(ge=0)
    claims_last_12mo: int = Field(ge=0)
    claims_last_36mo: int = Field(ge=0)

    # Financial Impact
    total_claims_amount: float = Field(ge=0)
    average_claim_amount: float = Field(ge=0)
    highest_single_claim: float = Field(ge=0)

    # Patterns
    claim_frequency_trend: str = Field(..., pattern="^(Increasing|Stable|Decreasing)$")

    # Detailed Claims
    recent_claims: List[Claim] = []

    # Fraud Indicators
    suspicious_patterns_detected: bool = False
    fraud_score: float = Field(ge=0, le=100)

# Example JSON
{
  "customer_id": "CUST_001",
  "total_claims_count": 8,
  "claims_last_12mo": 2,
  "claims_last_36mo": 5,
  "total_claims_amount": 15000,
  "average_claim_amount": 1875,
  "highest_single_claim": 5000,
  "claim_frequency_trend": "Stable",
  "recent_claims": [
    {
      "claim_id": "CLM_001",
      "claim_date": "2024-08-15",
      "claim_type": "Medical",
      "claim_amount": 2500,
      "approved_amount": 2200,
      "status": "Approved"
    }
  ],
  "suspicious_patterns_detected": false,
  "fraud_score": 12
}
```

**Endpoint:** `POST /api/risk/claims`

---

### 1.6 Agent/Channel Risk JSON

**File:** `data/schemas/agent_schema.py`

```python
class AgentData(BaseModel):
    """Agent/distribution channel risk factors"""
    customer_id: str

    # Agent Info
    agent_id: str
    agent_name: str
    agent_license_number: str
    years_licensed: int = Field(ge=0)

    # Performance
    total_policies_sold: int = Field(ge=0)
    policies_sold_12mo: int = Field(ge=0)
    lapse_rate: float = Field(ge=0, le=100)  # Percentage

    # Compliance
    compliance_violations: int = Field(ge=0)
    active_complaints: int = Field(ge=0)

    # Channel
    distribution_channel: str = Field(..., pattern="^(Direct|Broker|Online|Captive)$")

    # Fraud Risk
    fraud_investigations: int = Field(ge=0)
    fraud_confirmed_cases: int = Field(ge=0)
    agent_risk_score: float = Field(ge=0, le=100)

# Example JSON
{
  "customer_id": "CUST_001",
  "agent_id": "AGT_5432",
  "agent_name": "Jane Smith",
  "agent_license_number": "AGT-NY-12345",
  "years_licensed": 8,
  "total_policies_sold": 450,
  "policies_sold_12mo": 65,
  "lapse_rate": 8.5,
  "compliance_violations": 0,
  "active_complaints": 0,
  "distribution_channel": "Broker",
  "fraud_investigations": 0,
  "fraud_confirmed_cases": 0,
  "agent_risk_score": 15
}
```

**Endpoint:** `POST /api/risk/agent`

---

### 1.7 Product/Underwriting Risk JSON

**File:** `data/schemas/product_schema.py`

```python
class ProductData(BaseModel):
    """Product and underwriting risk factors"""
    customer_id: str

    # Product Details
    product_type: str = Field(..., pattern="^(Term Life|Whole Life|Health|Critical Illness|Disability)$")
    coverage_amount: float = Field(gt=0)
    premium_amount: float = Field(gt=0)
    policy_term_years: int = Field(ge=1, le=100)

    # Underwriting
    underwriting_class: str = Field(..., pattern="^(Preferred|Standard|Substandard|Declined)$")
    loading_percentage: float = Field(ge=0, le=500)  # Extra premium %
    exclusions: List[str] = []

    # Pricing Adequacy
    loss_ratio_expected: float = Field(ge=0, le=200)
    profit_margin: float = Field(ge=-100, le=100)

    # Risk Indicators
    sum_assured_to_income_ratio: float = Field(ge=0)
    affordability_score: float = Field(ge=0, le=100)

# Example JSON
{
  "customer_id": "CUST_001",
  "product_type": "Term Life",
  "coverage_amount": 500000,
  "premium_amount": 850,
  "policy_term_years": 20,
  "underwriting_class": "Standard",
  "loading_percentage": 0,
  "exclusions": [],
  "loss_ratio_expected": 65,
  "profit_margin": 15,
  "sum_assured_to_income_ratio": 4.0,
  "affordability_score": 75
}
```

**Endpoint:** `POST /api/risk/product`

---

## 2. Individual Risk Calculators

### Objective

Create 7 independent risk calculators, each analyzing its dimension and returning a standardized risk score.

### Standardized Response Format

```python
class RiskCalculationResult(BaseModel):
    dimension: str  # "demographic", "financial", etc.
    risk_score: float = Field(ge=0, le=100)
    risk_level: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    risk_factors: List[str]  # Identified risk factors
    weight_in_overall: float = Field(ge=0, le=1)  # For weighted combination
    recommendations: List[str]
```

---

### 2.1 Demographic Risk Calculator

**File:** `models/risk_calculators/demographic_risk.py`

```python
def calculate_demographic_risk(data: DemographicData) -> RiskCalculationResult:
    """
    Risk Factors:
    - Age: 18-30 (LOW), 31-50 (MEDIUM), 51-70 (HIGH), 70+ (CRITICAL)
    - Smoking: Never (0), Former (+15), Current (+40)
    - Exercise: Active (0), Moderate (+10), Light (+20), Sedentary (+30)
    - Alcohol: None (0), Moderate (+10), Heavy (+25)
    - BMI (from lifestyle): <18.5 (+20), 18.5-24.9 (0), 25-29.9 (+15), 30+ (+30)
    """
    score = 0
    factors = []

    # Age scoring
    if data.age < 30:
        score += 10
    elif data.age < 50:
        score += 25
    elif data.age < 70:
        score += 50
    else:
        score += 70
        factors.append("Advanced age (70+)")

    # Smoking
    if data.smoking_status == "Current":
        score += 40
        factors.append("Current smoker")
    elif data.smoking_status == "Former":
        score += 15

    # ... implement rest of logic

    return RiskCalculationResult(
        dimension="demographic",
        risk_score=min(score, 100),
        risk_level=get_risk_level(score),
        risk_factors=factors,
        weight_in_overall=0.15,  # 15% weight
        recommendations=generate_recommendations(factors)
    )
```

**Weight:** 15%

---

### 2.2 Financial Risk Calculator

**File:** `models/risk_calculators/financial_risk.py`

```python
def calculate_financial_risk(data: FinancialData) -> RiskCalculationResult:
    """
    Risk Factors:
    - Credit score: 750+ (LOW), 650-749 (MEDIUM), 550-649 (HIGH), <550 (CRITICAL)
    - Debt-to-income: <0.3 (LOW), 0.3-0.5 (MEDIUM), 0.5-0.8 (HIGH), >0.8 (CRITICAL)
    - Bankruptcy: Yes (+50), No (0)
    - Income stability: Stable (0), Variable (+20), Unstable (+40)
    - Late payments: 0 (0), 1-2 (+15), 3+ (+30)
    """
    # Implementation here
    return RiskCalculationResult(
        dimension="financial",
        risk_score=calculated_score,
        risk_level=get_risk_level(calculated_score),
        risk_factors=identified_factors,
        weight_in_overall=0.20,  # 20% weight
        recommendations=recommendations
    )
```

**Weight:** 20%

---

### 2.3 Medical Risk Calculator

**File:** `models/risk_calculators/medical_risk.py`

```python
def calculate_medical_risk(data: MedicalData) -> RiskCalculationResult:
    """
    Risk Factors:
    - ICD-10 codes: Sum risk_weights from medical_codes database
    - Medications: Sum risk_weights from NDC database
    - Procedures: Recent high-risk procedures (+20 each)
    - BMI: <18.5 (+20), 18.5-24.9 (0), 25-29.9 (+15), 30-34.9 (+30), 35+ (+50)
    - BP: Normal (0), Pre-hypertension (+15), Hypertension (+30)
    - Family history: Each condition (+10)
    """
    from data.medical_codes.icd10_codes import ICD10_CODES
    from data.medical_codes.ndc_codes import NDC_CODES

    score = 0
    factors = []

    # Analyze conditions
    for condition in data.conditions:
        if condition.icd10_code in ICD10_CODES:
            code_data = ICD10_CODES[condition.icd10_code]
            score += code_data["risk_weight"]
            factors.append(f"{code_data['description']} ({code_data['risk_weight']} pts)")

    # ... implement medication and procedure analysis

    return RiskCalculationResult(
        dimension="medical",
        risk_score=min(score, 100),
        risk_level=get_risk_level(score),
        risk_factors=factors,
        weight_in_overall=0.30,  # 30% weight (HIGHEST)
        recommendations=recommendations
    )
```

**Weight:** 30% (HIGHEST - medical is most critical)

---

### 2.4 Regional Risk Calculator

**File:** `models/risk_calculators/regional_risk.py`

**Weight:** 10%

### 2.5 Claims Risk Calculator

**File:** `models/risk_calculators/claims_risk.py`

**Weight:** 15%

### 2.6 Agent Risk Calculator

**File:** `models/risk_calculators/agent_risk.py`

**Weight:** 5%

### 2.7 Product Risk Calculator

**File:** `models/risk_calculators/product_risk.py`

**Weight:** 5%

---

## 3. Combined Risk Calculator

**File:** `models/risk_calculators/combined_risk.py`

```python
from typing import List, Dict

class CombinedRiskResult(BaseModel):
    customer_id: str
    overall_risk_score: float
    overall_risk_level: str
    dimension_scores: List[RiskCalculationResult]
    top_risk_factors: List[str]
    underwriting_decision: str  # "ACCEPT|REVIEW|DECLINE"
    recommended_loading: float  # Premium increase %
    recommendations: List[str]

def calculate_combined_risk(
    demographic: DemographicData,
    financial: FinancialData,
    medical: MedicalData,
    regional: RegionalData,
    claims: ClaimsData,
    agent: AgentData,
    product: ProductData
) -> CombinedRiskResult:
    """
    Weighted Risk Calculation:
    - Medical: 30%
    - Financial: 20%
    - Demographic: 15%
    - Claims: 15%
    - Regional: 10%
    - Agent: 5%
    - Product: 5%

    Overall Score = Σ (dimension_score × weight)
    """

    # Calculate individual risks
    demo_risk = calculate_demographic_risk(demographic)
    fin_risk = calculate_financial_risk(financial)
    med_risk = calculate_medical_risk(medical)
    reg_risk = calculate_regional_risk(regional)
    claims_risk = calculate_claims_risk(claims)
    agent_risk = calculate_agent_risk(agent)
    prod_risk = calculate_product_risk(product)

    # Weighted combination
    overall_score = (
        demo_risk.risk_score * 0.15 +
        fin_risk.risk_score * 0.20 +
        med_risk.risk_score * 0.30 +
        reg_risk.risk_score * 0.10 +
        claims_risk.risk_score * 0.15 +
        agent_risk.risk_score * 0.05 +
        prod_risk.risk_score * 0.05
    )

    # Determine underwriting decision
    if overall_score < 30:
        decision = "ACCEPT"
        loading = 0
    elif overall_score < 50:
        decision = "ACCEPT"
        loading = 10  # 10% premium increase
    elif overall_score < 70:
        decision = "REVIEW"
        loading = 25
    else:
        decision = "DECLINE"
        loading = 0

    return CombinedRiskResult(
        customer_id=demographic.customer_id,
        overall_risk_score=overall_score,
        overall_risk_level=get_risk_level(overall_score),
        dimension_scores=[demo_risk, fin_risk, med_risk, reg_risk, claims_risk, agent_risk, prod_risk],
        top_risk_factors=extract_top_factors([demo_risk, fin_risk, med_risk]),
        underwriting_decision=decision,
        recommended_loading=loading,
        recommendations=generate_combined_recommendations(overall_score, decision)
    )
```

---

## API Endpoints

### Individual Risk Endpoints

```python
POST /api/risk/demographic     → DemographicRiskResult
POST /api/risk/financial       → FinancialRiskResult
POST /api/risk/medical         → MedicalRiskResult
POST /api/risk/regional        → RegionalRiskResult
POST /api/risk/claims          → ClaimsRiskResult
POST /api/risk/agent           → AgentRiskResult
POST /api/risk/product         → ProductRiskResult
```

### Combined Risk Endpoint

```python
POST /api/risk/combined
{
  "demographic": { ... },
  "financial": { ... },
  "medical": { ... },
  "regional": { ... },
  "claims": { ... },
  "agent": { ... },
  "product": { ... }
}

→ CombinedRiskResult (overall assessment)
```

---

## File Structure

```
data/schemas/
  demographic_schema.py
  financial_schema.py
  medical_schema.py
  regional_schema.py
  claims_schema.py
  agent_schema.py
  product_schema.py

models/risk_calculators/
  demographic_risk.py
  financial_risk.py
  medical_risk.py
  regional_risk.py
  claims_risk.py
  agent_risk.py
  product_risk.py
  combined_risk.py
  utils.py  # Shared utilities (get_risk_level, etc.)

api/
  risk_routes.py  # All risk endpoints

tests/
  test_demographic_risk.py
  test_financial_risk.py
  test_medical_risk.py
  ...
  test_combined_risk.py
```

---

## Testing Strategy

### Unit Tests

```python
# Example: test_demographic_risk.py
def test_young_non_smoker_low_risk():
    data = DemographicData(
        customer_id="TEST_001",
        age=25,
        smoking_status="Never",
        exercise_frequency="Active",
        # ... other fields
    )
    result = calculate_demographic_risk(data)
    assert result.risk_level == "LOW"
    assert result.risk_score < 30

def test_elderly_smoker_high_risk():
    data = DemographicData(
        age=75,
        smoking_status="Current",
        exercise_frequency="Sedentary",
        # ...
    )
    result = calculate_demographic_risk(data)
    assert result.risk_level in ["HIGH", "CRITICAL"]
    assert result.risk_score > 60
```

### Integration Tests

```python
def test_combined_risk_calculation():
    """Test full end-to-end risk calculation"""
    result = calculate_combined_risk(
        demographic=sample_demographic_data,
        financial=sample_financial_data,
        medical=sample_medical_data,
        # ... all dimensions
    )
    assert 0 <= result.overall_risk_score <= 100
    assert result.overall_risk_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert len(result.dimension_scores) == 7
```

---

## Deliverables

- [ ] 7 Pydantic schema files for each dimension
- [ ] 7 individual risk calculators
- [ ] 1 combined risk calculator with weighted scoring
- [ ] 8 API endpoints (7 individual + 1 combined)
- [ ] Unit tests for all calculators (80%+ coverage)
- [ ] Integration tests for combined workflow
- [ ] API documentation in Swagger
- [ ] `RISK_CALCULATORS.md` documentation

---

## Development Guidelines

### Risk Level Thresholds

```python
def get_risk_level(score: float) -> str:
    if score < 30:
        return "LOW"
    elif score < 50:
        return "MEDIUM"
    elif score < 70:
        return "HIGH"
    else:
        return "CRITICAL"
```

### Testing

```bash
pytest tests/test_*_risk.py -v
pytest tests/test_combined_risk.py -v
```

### Git Branching Strategy

**Branch Naming Convention:**

- Use `dev2/` prefix for all your branches
- Branch name should describe the feature clearly
- Examples: `dev2/risk-schemas`, `dev2/demographic-calculator`, `dev2/combined-risk`

**Recommended Branching Structure:**

```bash
# Day 1: All 7 JSON Schemas
git checkout -b dev2/risk-schemas
# Create all 7 Pydantic schemas
git add data/schemas/demographic_schema.py
git add data/schemas/financial_schema.py
git add data/schemas/medical_schema.py
git add data/schemas/regional_schema.py
git add data/schemas/claims_schema.py
git add data/schemas/agent_schema.py
git add data/schemas/product_schema.py
git commit -m "feat: Add all 7 risk dimension Pydantic schemas"
git commit -m "test: Add schema validation tests"
git push -u origin dev2/risk-schemas

# Day 2: First Set of Calculators
git checkout -b dev2/calculators-set1
# Implement demographic, financial, regional calculators
git add models/risk_calculators/demographic_risk.py
git add models/risk_calculators/financial_risk.py
git add models/risk_calculators/regional_risk.py
git add models/risk_calculators/utils.py
git commit -m "feat: Implement demographic risk calculator with age/lifestyle scoring"
git commit -m "feat: Implement financial risk calculator with credit/debt analysis"
git commit -m "feat: Implement regional risk calculator with geographic factors"
git commit -m "feat: Add shared utilities for risk level determination"
git push -u origin dev2/calculators-set1

# Day 3: Second Set of Calculators
git checkout -b dev2/calculators-set2
# Implement claims, agent, product calculators
git add models/risk_calculators/claims_risk.py
git add models/risk_calculators/agent_risk.py
git add models/risk_calculators/product_risk.py
git commit -m "feat: Implement claims risk calculator with fraud detection"
git commit -m "feat: Implement agent risk calculator with compliance scoring"
git commit -m "feat: Implement product risk calculator with pricing adequacy"
git push -u origin dev2/calculators-set2

# Day 4: Medical Calculator + Combined Risk
git checkout -b dev2/medical-and-combined
# Implement medical calculator (integrate Dev 1's codes) + combined risk
git add models/risk_calculators/medical_risk.py
git add models/risk_calculators/combined_risk.py
git commit -m "feat: Implement medical risk calculator with ICD-10/CPT/NDC integration"
git commit -m "feat: Implement combined risk calculator with weighted scoring"
git commit -m "feat: Add underwriting decision logic (ACCEPT/REVIEW/DECLINE)"
git commit -m "test: Add combined risk calculation tests"
git push -u origin dev2/medical-and-combined

# Day 5: API Endpoints + Integration Testing
git checkout -b dev2/api-endpoints
# Create API routes and integration tests
git add api/risk_routes.py
git commit -m "feat: Add 7 individual risk assessment endpoints"
git commit -m "feat: Add combined risk assessment endpoint"
git commit -m "feat: Add request/response validation"
git commit -m "test: Add API integration tests"
git commit -m "docs: Add Swagger documentation for all endpoints"
git commit -m "docs: Add RISK_CALCULATORS.md with usage examples"
git push -u origin dev2/api-endpoints
```

**Best Practices:**

1. **Create branches from main/First-commit-branch:**

   ```bash
   git checkout First-commit-branch
   git pull origin First-commit-branch
   git checkout -b dev2/your-feature-name
   ```
2. **Commit messages format:**

   - `feat:` - New feature (calculator, schema, endpoint)
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `test:` - Test additions/changes
   - `refactor:` - Code refactoring
3. **Keep branches organized by day/task:**

   - Day 1: All schemas in one branch (`dev2/risk-schemas`)
   - Day 2-3: Group related calculators together
   - Day 4: Medical + combined (since they depend on Dev 1's work)
   - Day 5: All API work in one branch
4. **Push regularly:**

   ```bash
   # Always use -u flag on first push
   git push -u origin dev2/branch-name

   # Subsequent pushes
   git push
   ```
5. **Sync with main branch regularly:**

   ```bash
   git checkout First-commit-branch
   git pull origin First-commit-branch
   git checkout dev2/your-feature
   git merge First-commit-branch
   # Resolve conflicts if any
   git push
   ```
6. **Coordinate with Developer 1:**

   ```bash
   # On Day 4, before implementing medical calculator:
   # Pull Dev 1's medical codes branches
   git fetch origin dev1/medical-codes-icd10
   git fetch origin dev1/medical-codes-extended

   # Or merge their changes if already in First-commit-branch
   git checkout First-commit-branch
   git pull origin First-commit-branch
   git checkout dev2/medical-and-combined
   git merge First-commit-branch
   ```
7. **Create Pull Requests:**

   - After completing each major feature, create PR to First-commit-branch
   - Request code review from Developer 1 or team lead
   - Ensure all tests pass before merging
   - Address review comments promptly

---

## Timeline (Nov 24-28, 2025)

- **Day 1 (Mon, Nov 24):** Create all 7 JSON schemas + Pydantic models
- **Day 2 (Tue, Nov 25):** Implement demographic + financial + regional calculators
- **Day 3 (Wed, Nov 26):** Implement claims + agent + product calculators
- **Day 4 (Thu, Nov 27):** Implement medical risk calculator (integrate Dev 1's codes) + combined risk calculator
- **Day 5 (Fri, Nov 28):** API endpoints + integration testing + documentation + code review

**Coordinate with Developer 1** on Day 4 to integrate medical codes into your medical risk calculator.

---

## Success Criteria

✅ All 7 dimension schemas defined with proper validation
✅ All 7 individual calculators return accurate risk scores
✅ Combined calculator correctly applies weighted scoring
✅ API endpoints functional with Swagger documentation
✅ Unit tests passing (80%+ coverage)
✅ Integration with medical codes database (from Dev 1)
✅ Clear documentation for future maintenance
