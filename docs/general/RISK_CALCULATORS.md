# Risk Assessment Engine - Complete Documentation

**Version:** 1.0.0  
**Date:** November 25, 2025  
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Risk Calculators](#risk-calculators)
4. [API Endpoints](#api-endpoints)
5. [Usage Examples](#usage-examples)
6. [Integration Guide](#integration-guide)
7. [Future Enhancements](#future-enhancements)

---

## Overview

The Risk Assessment Engine is a comprehensive insurance underwriting system that evaluates applicant risk across 7 dimensions using rule-based calculators and weighted scoring.

### Key Features

- ✅ **7 Risk Dimensions:** Demographic, Financial, Medical, Regional, Claims, Agent, Product
- ✅ **Weighted Scoring:** Medical (30%), Financial (20%), Demographic (15%), Claims (15%), Regional (10%), Agent (5%), Product (5%)
- ✅ **Automated Decisions:** ACCEPT, REVIEW, or DECLINE with premium loading recommendations
- ✅ **REST API:** 8 endpoints with OpenAPI/Swagger documentation
- ✅ **Production Ready:** Full validation, error handling, and test coverage

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│                         (main.py)                        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐       ┌───────▼────────┐
│  AI Endpoint   │       │ Risk Calculator │
│  (Ollama GPT)  │       │   Endpoints     │
└────────────────┘       └───────┬─────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
            ┌───────▼────────┐       ┌───────▼────────┐
            │   Individual    │       │    Combined    │
            │   Calculators   │       │   Calculator   │
            │     (7 dims)    │       │  (Weighted)    │
            └───────┬─────────┘       └───────┬────────┘
                    │                         │
            ┌───────▼─────────────────────────▼────────┐
            │         Pydantic Schemas (Input)         │
            │  Demographic, Financial, Medical, etc.   │
            └──────────────────────────────────────────┘
```

### Directory Structure

```
uw-risk-assessment-engine/
├── api/
│   ├── routes.py              # AI risk assessment endpoint
│   └── risk_routes.py         # Risk calculator endpoints ⭐
├── data/schemas/
│   ├── demographic_schema.py  # Demographic data model
│   ├── financial_schema.py    # Financial data model
│   ├── medical_schema.py      # Medical data model
│   ├── regional_schema.py     # Regional data model
│   ├── claims_schema.py       # Claims data model
│   ├── agent_schema.py        # Agent data model
│   ├── product_schema.py      # Product data model
│   └── result_schema.py       # Result models ⭐
├── models/risk_calculators/
│   ├── demographic_risk.py    # Demographic calculator
│   ├── financial_risk.py      # Financial calculator
│   ├── medical_risk.py        # Medical calculator
│   ├── regional_risk.py       # Regional calculator
│   ├── claims_risk.py         # Claims calculator
│   ├── agent_risk.py          # Agent calculator
│   ├── product_risk.py        # Product calculator
│   ├── combined_risk.py       # Combined calculator ⭐
│   └── utils.py               # Utility functions
├── tests/
│   └── test_integration.py    # API integration tests
└── main.py                    # FastAPI application
```

---

## Risk Calculators

### 1. Demographic Risk Calculator (15% weight)

**Factors:**
- Age (18-30: LOW, 31-50: MEDIUM, 51-70: HIGH, 70+: CRITICAL)
- Smoking (Never: 0, Former: +15, Current: +40)
- Alcohol (None: 0, Moderate: +5, Heavy: +20)
- Exercise (Active: 0, Moderate: +5, Light: +10, Sedentary: +15)

**Example:**
- 44-year-old, non-smoker, moderate alcohol, moderate exercise = **Score: 45 (MEDIUM)**

---

### 2. Financial Risk Calculator (20% weight)

**Factors:**
- Credit Score (750+: LOW, 650-749: MEDIUM, 550-649: HIGH, <550: CRITICAL)
- Debt-to-Income (<0.3: LOW, 0.3-0.5: MEDIUM, 0.5-0.8: HIGH, >0.8: CRITICAL)
- Bankruptcy (Recent: +50, Historical: +15-30)
- Income Stability (Stable: 0, Variable: +15, Unstable: +30)

**Example:**
- 750 credit score, 40% DTI, no bankruptcy = **Score: 22 (LOW)**

---

### 3. Medical Risk Calculator (30% weight - HIGHEST)

**Factors:**
- BMI (<18.5: +20, 25-29.9: +10, 30-34.9: +20, 35+: +35)
- Blood Pressure (180+/120+: +40, 140+/90+: +25, 130+/80+: +15)
- Pre-existing Conditions (Active: +20, Controlled: +10, Resolved: +3)
- Family History (Cancer: +12, Heart Disease: +15, Diabetes: +10)

**Example:**
- BMI 25.9, BP 128/82, family history of heart disease = **Score: 33 (MEDIUM)**

**Future Integration:**
- ICD-10 risk weights for conditions
- NDC medication risk weights
- CPT procedure risk weights

---

### 4. Regional Risk Calculator (10% weight)

**Factors:**
- Healthcare Access (Hospital distance, specialist availability)
- Environmental (Air quality, natural disasters)
- Socioeconomic (Crime rate, unemployment)
- Cost of Living (Healthcare cost index)

**Example:**
- Urban area, good healthcare access, moderate costs = **Score: 15 (LOW)**

---

### 5. Claims Risk Calculator (15% weight)

**Factors:**
- Frequency (>5 claims in 12mo: +35)
- Amounts (High average: +20, High single: +25)
- Fraud Score (>70: +50, >50: +30)
- Trend (Increasing: +25)

**Example:**
- 2 claims in 12mo, low fraud score = **Score: 20 (LOW)**

---

### 6. Agent Risk Calculator (5% weight)

**Factors:**
- Compliance (Violations: +20-30, Complaints: +12-25)
- Performance (High lapse rate: +20, Low experience: +15)
- Fraud (Confirmed cases: +50, Investigations: +20)

**Example:**
- Experienced agent, no violations = **Score: 13 (LOW)**

---

### 7. Product Risk Calculator (5% weight)

**Factors:**
- Coverage Ratio (>15x income: +35, >10x: +25)
- Affordability (<40: +30, <60: +20)
- Underwriting Class (Declined: +50, Substandard: +25)
- Loss Ratio (>90%: +25, >80%: +15)

**Example:**
- 4x income ratio, 75 affordability, standard class = **Score: 18 (LOW)**

---

### 8. Combined Risk Calculator

**Weighted Formula:**
```
Overall Score = 
  (Medical × 0.30) +
  (Financial × 0.20) +
  (Demographic × 0.15) +
  (Claims × 0.15) +
  (Regional × 0.10) +
  (Agent × 0.05) +
  (Product × 0.05)
```

**Underwriting Decision:**
- **0-49 (ACCEPT):** 0-10% premium loading
- **50-69 (REVIEW):** 25% loading, manual review required
- **70-100 (DECLINE):** Application declined

**Example:**
```
Demographic: 45 × 0.15 = 6.75
Financial:   22 × 0.20 = 4.40
Medical:     33 × 0.30 = 9.90
Regional:     5 × 0.10 = 0.50
Claims:      10 × 0.15 = 1.50
Agent:       13 × 0.05 = 0.65
Product:     18 × 0.05 = 0.90
─────────────────────────────
Overall Score: 26.85 (LOW)
Decision: ACCEPT
Loading: 0%
```

---

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Authentication
Currently no authentication required (add JWT/OAuth for production)

### Endpoints

#### 1. POST /api/risk/demographic
Assess demographic risk factors.

**Request:**
```json
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
  "marital_status": "Married",
  "household_size": 4,
  "dependents": 2,
  "zip_code": "10001",
  "state": "NY"
}
```

**Response:**
```json
{
  "dimension": "demographic",
  "risk_score": 45.0,
  "risk_level": "MEDIUM",
  "risk_factors": ["Age 44 (elevated risk)"],
  "weight_in_overall": 0.15,
  "recommendations": ["Request comprehensive health questionnaire"]
}
```

#### 2. POST /api/risk/combined ⭐
Assess combined risk across all 7 dimensions.

**Request:**
```json
{
  "demographic": { ... },
  "financial": { ... },
  "medical": { ... },
  "regional": { ... },
  "claims": { ... },
  "agent": { ... },
  "product": { ... }
}
```

**Response:**
```json
{
  "customer_id": "CUST_001",
  "overall_risk_score": 26.85,
  "overall_risk_level": "LOW",
  "dimension_scores": [ ... 7 individual results ... ],
  "top_risk_factors": [
    "Overweight (BMI: 25.9) (Medical)",
    "Family history of heart disease (Medical)",
    "Age 44 (elevated risk) (Demographic)"
  ],
  "underwriting_decision": "ACCEPT",
  "recommended_loading": 0.0,
  "recommendations": [
    "Accept at standard rates"
  ]
}
```

### Error Responses

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is less than or equal to 120",
      "type": "value_error.number.not_le"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error calculating demographic risk: ..."
}
```

---

## Usage Examples

### Python (requests)

```python
import requests

# Single dimension assessment
response = requests.post(
    "http://localhost:8000/api/risk/demographic",
    json={
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
        "marital_status": "Married",
        "household_size": 4,
        "dependents": 2,
        "zip_code": "10001",
        "state": "NY"
    }
)

result = response.json()
print(f"Risk Score: {result['risk_score']}")
print(f"Decision: {result['risk_level']}")
```

### cURL

```bash
curl -X POST "http://localhost:8000/api/risk/demographic" \
  -H "Content-Type: application/json" \
  -d '{
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
    "marital_status": "Married",
    "household_size": 4,
    "dependents": 2,
    "zip_code": "10001",
    "state": "NY"
  }'
```

---

## Integration Guide

### 1. Installation

```bash
# Clone repository
git clone <repository-url>
cd uw-risk-assessment-engine

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

```bash
# Start the server
uvicorn main:app --reload

# Access Swagger documentation
http://localhost:8000/docs

# Access ReDoc documentation
http://localhost:8000/redoc
```

### 3. Running Tests

```bash
# Run integration tests
pytest tests/test_integration.py -v

# Run all tests
pytest -v
```

### 4. Integration with LOS (Loan Origination System)

```python
from risk_assessment_client import RiskAssessmentClient

# Initialize client
client = RiskAssessmentClient(base_url="http://localhost:8000")

# Assess applicant
result = client.assess_combined_risk(
    demographic=demographic_data,
    financial=financial_data,
    medical=medical_data,
    regional=regional_data,
    claims=claims_data,
    agent=agent_data,
    product=product_data
)

# Make decision
if result.underwriting_decision == "ACCEPT":
    premium = base_premium * (1 + result.recommended_loading / 100)
    approve_application(premium)
elif result.underwriting_decision == "REVIEW":
    send_to_underwriter(result)
else:
    decline_application(result.recommendations)
```

---

## Future Enhancements

### Phase 1: Medical Code Integration (Pending Developer 1)
- ✅ ICD-10 disease risk weight database
- ✅ NDC medication risk weight database
- ✅ CPT procedure risk weight database
- ✅ Enhanced medical risk scoring

### Phase 2: Advanced Features
- Batch risk assessment endpoint
- Historical risk trend analysis
- Comparative risk reports
- PDF report generation
- Email notifications

### Phase 3: Performance & Scale
- Redis caching for frequent calculations
- Async processing for combined risk
- Database integration for audit trail
- Load balancing for high volume

### Phase 4: ML Enhancement
- Machine learning model integration
- Predictive analytics
- Risk pattern detection
- Anomaly detection

---

## Support & Maintenance

**Version:** 1.0.0  
**Last Updated:** November 25, 2025  
**Status:** Production Ready

**Contact:**
- Technical Support: [support@example.com]
- Documentation: http://localhost:8000/docs

---

## License

Copyright © 2025 Monocept Official. All rights reserved.
