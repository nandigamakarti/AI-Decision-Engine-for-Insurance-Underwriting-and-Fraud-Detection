# Risk Assessment Test Data

This directory contains **70 JSON test files** organized by risk calculator type for the Underwriting Risk Assessment Engine.

## Directory Structure

```
risk_tests/
├── agent/          (10 test files)
├── claims/         (10 test files)
├── demographic/    (10 test files)
├── financial/      (10 test files)
├── medical/        (10 test files)
├── product/        (10 test files)
└── regional/       (10 test files)
```

## Test Categories

### 1. Agent Risk Tests (`agent/`)
Tests for agent/distribution channel risk assessment covering:
- Low risk agents with excellent performance
- New agents with limited experience
- Online channel risks
- Compliance violations and complaints
- High lapse rates
- Fraud investigations and confirmed fraud cases
- Inactive agents
- Various risk levels from excellent to critical

**Files:** `test_01_low_risk.json` through `test_10_excellent_performer.json`

### 2. Claims Risk Tests (`claims/`)
Tests for claims history risk assessment covering:
- No claims history (ideal)
- Low to moderate claims activity
- High frequency with increasing trends
- High claim amounts
- Multiple denied claims
- Multiple pending claims
- Suspicious patterns detected
- High fraud scores
- Critical cases with extreme activity

**Files:** `test_01_no_claims.json` through `test_10_critical_case.json`

### 3. Demographic Risk Tests (`demographic/`)
Tests for demographic and lifestyle risk factors covering:
- Young, healthy individuals
- Middle-aged with moderate lifestyle
- Former smokers
- Current smokers (high risk)
- Heavy alcohol consumption
- Advanced age (70+)
- Multiple high-risk lifestyle factors
- Excellent health profiles
- Seniors with good habits
- Very advanced age (79+)

**Files:** `test_01_young_healthy.json` through `test_10_very_senior.json`

### 4. Financial Risk Tests (`financial/`)
Tests for financial stability and creditworthiness covering:
- Excellent financial profiles
- Good financial standing
- Self-employed with variable income
- High debt-to-income ratios
- Poor credit scores
- Recent bankruptcy history
- Old bankruptcy with recovery
- Unemployment
- Successful self-employed
- Critical financial distress

**Files:** `test_01_excellent_profile.json` through `test_10_critical_distress.json`

### 5. Medical Risk Tests (`medical/`)
Tests for medical conditions and health status covering:
- Perfect health (no conditions)
- Controlled hypertension
- Type 2 diabetes with obesity
- Active asthma with allergies
- Coronary artery disease with stent
- Cancer survivors
- Multiple chronic conditions with severe obesity
- Heart failure with kidney disease
- Healthy individuals with family history
- Critical cases (recent stroke, hypertensive crisis)

**Files:** `test_01_perfect_health.json` through `test_10_critical_stroke.json`

### 6. Product Risk Tests (`product/`)
Tests for product and underwriting risk covering:
- Ideal product risk profiles
- Standard coverage scenarios
- Whole life products
- Critical illness with exclusions
- High coverage ratios
- Poor affordability
- High loading percentages
- Disability insurance
- Previously declined cases
- Preferred class products

**Files:** `test_01_ideal_profile.json` through `test_10_preferred_critical.json`

### 7. Regional Risk Tests (`regional/`)
Tests for geographic and environmental risk factors covering:
- Urban areas with excellent healthcare access
- Earthquake zones
- Hurricane zones
- Flood zones
- Rural areas with limited healthcare
- Remote locations with high costs
- Poor air quality areas
- Very remote locations
- High crime and unemployment areas
- Critical cases with multiple risk factors

**Files:** `test_01_urban_excellent.json` through `test_10_critical_multiple_risks.json`

## Usage

These test files can be used to:
1. Test individual risk calculators
2. Validate API endpoints
3. Demonstrate the risk assessment engine capabilities
4. Perform integration testing
5. Generate sample risk reports

## File Format

All test files are in JSON format and conform to their respective Pydantic schemas:
- `AgentData` for agent tests
- `ClaimsData` for claims tests
- `DemographicData` for demographic tests
- `FinancialData` for financial tests
- `MedicalData` for medical tests
- `ProductData` for product tests
- `RegionalData` for regional tests

## Test Coverage

Each category includes a range of scenarios from:
- **Low Risk:** Ideal profiles with minimal risk factors
- **Moderate Risk:** Average profiles with some concerns
- **High Risk:** Profiles with significant risk factors
- **Critical Risk:** Extreme cases requiring special attention

## Next Steps

These test files are ready to be integrated into:
- FastAPI backend endpoints for risk calculator selection
- Automated testing frameworks
- Demo and presentation scenarios
- User acceptance testing (UAT)
