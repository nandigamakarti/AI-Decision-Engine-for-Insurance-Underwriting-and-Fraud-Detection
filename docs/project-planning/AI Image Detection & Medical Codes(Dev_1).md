
# CLAUDE.md - Developer 1 (Week Assignment)

## Your Focus Areas

1. **AI-Generated Image Detection System**
2. **Medical Codes Implementation**

---

## 1. AI-Generated Image Detection for Claims

### Objective

Build a service to detect AI-generated, edited, or suspicious images submitted with insurance claims.

### Requirements

#### Image Analysis Capabilities

- Detect fully AI-generated images (DALL-E, Midjourney, Stable Diffusion artifacts)
- Identify edited/manipulated images (Photoshop, GIMP modifications)
- Flag suspicious patterns (inconsistent lighting, unrealistic textures)
- Support formats: JPG, PNG, PDF (extract images from PDFs)

#### API Endpoint

```python
POST /api/image-analysis
{
  "claim_id": "CLM_12345",
  "image_data": "base64_encoded_string",  # or file upload
  "image_type": "medical_report|invoice|damage_photo|other"
}

Response:
{
  "claim_id": "CLM_12345",
  "is_ai_generated": true/false,
  "confidence_score": 0.87,  # 0-1
  "manipulation_detected": true/false,
  "suspicion_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "analysis_details": {
    "ai_artifacts": ["unnatural_patterns", "pixel_inconsistencies"],
    "editing_traces": ["clone_stamp_detected", "filter_applied"],
    "metadata_issues": ["missing_exif", "modified_timestamp"]
  },
  "recommendation": "ACCEPT|REVIEW|REJECT"
}
```

#### Technical Implementation

**File Structure:**

```
services/
  image_analysis/
    __init__.py
    detector.py           # Main detection logic
    ai_detector.py        # AI generation detection
    manipulation_detector.py  # Edit detection
    metadata_analyzer.py  # EXIF/metadata analysis

api/
  image_routes.py       # Image analysis endpoints
  image_models.py       # Request/response models
```

**Tools/Libraries:**

- `Pillow` - Image processing
- `opencv-python` - Computer vision analysis
- `pillow-heif` - HEIF/HEIC support
- `PyPDF2` or `pdf2image` - PDF image extraction
- `exifread` - Metadata extraction
- **AI Detection:** Use HuggingFace models or build custom detector:
  - `transformers` + pre-trained models (e.g., `umm-maybe/AI-image-detector`)
  - Or local Ollama with vision capabilities (llava, bakllava)

**Key Detection Strategies:**

1. **AI Artifacts:** Repetitive patterns, unrealistic symmetry, impossible physics
2. **Frequency Analysis:** DCT/FFT analysis for generation signatures
3. **Metadata Check:** Missing camera info, suspicious software tags
4. **Error Level Analysis (ELA):** Compression artifact inconsistencies
5. **Statistical Analysis:** Pixel distribution, color histogram anomalies

### Deliverables

- [ ] `services/image_analysis/` module with all detectors
- [ ] `POST /api/image-analysis` endpoint
- [ ] Unit tests for detection algorithms
- [ ] Integration with claims workflow (flag suspicious claims)
- [ ] Documentation: `IMAGE_DETECTION.md` with usage examples

---

## 2. Medical Codes Implementation

### Objective

Create comprehensive medical code databases and integrate into risk assessment API.

### Code Systems to Implement

#### 2.1 ICD-10 Codes (Diagnosis)

**File:** `data/medical_codes/icd10_codes.py`

```python
ICD10_CODES = {
    # Cardiovascular (High Risk - 70-90)
    "I21.0": {"description": "ST elevation MI anterior wall", "risk_weight": 90, "category": "cardiovascular"},
    "I50.9": {"description": "Heart failure, unspecified", "risk_weight": 85, "category": "cardiovascular"},
    "I10": {"description": "Essential hypertension", "risk_weight": 50, "category": "cardiovascular"},

    # Diabetes (Medium-High Risk - 60-75)
    "E11.9": {"description": "Type 2 diabetes", "risk_weight": 65, "category": "endocrine"},
    "E10.9": {"description": "Type 1 diabetes", "risk_weight": 70, "category": "endocrine"},

    # Cancer (High Risk - 75-95)
    "C34.9": {"description": "Lung cancer", "risk_weight": 95, "category": "neoplasm"},
    "C50.9": {"description": "Breast cancer", "risk_weight": 80, "category": "neoplasm"},

    # Respiratory (Medium Risk - 40-60)
    "J45.9": {"description": "Asthma", "risk_weight": 45, "category": "respiratory"},
    "J44.9": {"description": "COPD", "risk_weight": 70, "category": "respiratory"},

    # Mental Health (Medium Risk - 30-55)
    "F32.9": {"description": "Major depressive disorder", "risk_weight": 40, "category": "mental"},
    "F41.9": {"description": "Anxiety disorder", "risk_weight": 35, "category": "mental"},

    # Add 100+ more codes covering all major categories
}
```

**Target:** 150-200 ICD-10 codes with risk weights

#### 2.2 CPT Codes (Procedures)

**File:** `data/medical_codes/cpt_codes.py`

```python
CPT_CODES = {
    # Surgical Procedures (High Cost, Medium-High Risk)
    "33510": {"description": "Coronary artery bypass", "cost_estimate": 75000, "risk_weight": 85, "category": "cardiac_surgery"},
    "43280": {"description": "Laparoscopic fundoplasty", "cost_estimate": 15000, "risk_weight": 50, "category": "gi_surgery"},

    # Imaging (Low-Medium Risk)
    "70450": {"description": "CT head without contrast", "cost_estimate": 500, "risk_weight": 15, "category": "imaging"},
    "71020": {"description": "Chest X-ray 2 views", "cost_estimate": 150, "risk_weight": 10, "category": "imaging"},

    # Lab Tests (Low Risk)
    "80053": {"description": "Comprehensive metabolic panel", "cost_estimate": 50, "risk_weight": 5, "category": "lab"},
    "85025": {"description": "Complete blood count", "cost_estimate": 30, "risk_weight": 5, "category": "lab"},

    # Add 150+ more CPT codes
}
```

**Target:** 200+ CPT codes with cost estimates

#### 2.3 NDC Codes (Medications)

**File:** `data/medical_codes/ndc_codes.py`

```python
NDC_CODES = {
    # High-Risk Medications
    "00004-0008-01": {"description": "Warfarin 5mg", "risk_class": "HIGH", "risk_weight": 70, "category": "anticoagulant"},
    "00002-7510-01": {"description": "Insulin glargine", "risk_class": "MEDIUM", "risk_weight": 60, "category": "diabetes"},

    # Controlled Substances
    "00406-0489-01": {"description": "Oxycodone 10mg", "risk_class": "HIGH", "risk_weight": 75, "category": "opioid"},

    # Routine Medications
    "00093-7169-01": {"description": "Lisinopril 10mg", "risk_class": "LOW", "risk_weight": 25, "category": "antihypertensive"},

    # Add 50+ more NDC codes
}
```

**Target:** 50-100 NDC codes

#### 2.4 HCPCS Codes (DME & Services)

**File:** `data/medical_codes/hcpcs_codes.py`

```python
HCPCS_CODES = {
    # Durable Medical Equipment
    "E0601": {"description": "CPAP device", "cost_estimate": 800, "risk_weight": 40, "category": "respiratory_equipment"},
    "E0250": {"description": "Hospital bed", "cost_estimate": 500, "risk_weight": 30, "category": "bed"},

    # Ambulance
    "A0429": {"description": "Ambulance ALS emergency", "cost_estimate": 1200, "risk_weight": 50, "category": "transport"},

    # Add 30+ more HCPCS codes
}
```

### API Integration

#### Endpoint: Medical Code Lookup

```python
GET /api/medical-codes/{code_type}/{code}
# Example: GET /api/medical-codes/icd10/I21.0

Response:
{
  "code": "I21.0",
  "code_type": "ICD10",
  "description": "ST elevation MI anterior wall",
  "risk_weight": 90,
  "category": "cardiovascular",
  "recommendations": ["Require cardiac clearance", "Apply high-risk loading"]
}
```

#### Endpoint: Batch Code Analysis

```python
POST /api/medical-codes/analyze
{
  "icd10_codes": ["I21.0", "E11.9"],
  "cpt_codes": ["33510"],
  "ndc_codes": ["00004-0008-01"]
}

Response:
{
  "overall_medical_risk_score": 82.5,
  "total_estimated_cost": 75500,
  "high_risk_factors": ["Cardiac history", "Diabetes", "Anticoagulant use"],
  "recommendations": ["Require medical underwriting", "Apply 50% loading"]
}
```

### File Structure

```
data/
  medical_codes/
    __init__.py
    icd10_codes.py       # 150-200 diagnosis codes
    cpt_codes.py         # 200+ procedure codes
    ndc_codes.py         # 50-100 medication codes
    hcpcs_codes.py       # 30+ DME/service codes
    code_analyzer.py     # Analysis logic

api/
  medical_code_routes.py  # Code lookup endpoints
  medical_code_models.py  # Request/response models
```

### Deliverables

- [ ] All 4 medical code databases populated
- [ ] `GET /api/medical-codes/{type}/{code}` endpoint
- [ ] `POST /api/medical-codes/analyze` endpoint
- [ ] Code search functionality (fuzzy matching)
- [ ] Integration tests with sample codes
- [ ] Documentation: `MEDICAL_CODES.md` with code examples

---

## Development Guidelines

### Testing

```bash
# Run your tests
pytest tests/test_image_analysis.py -v
pytest tests/test_medical_codes.py -v
```

### Dependencies to Add

```bash
uv add pillow opencv-python exifread PyPDF2 pdf2image transformers pillow-heif
```

### Git Branching Strategy

**Branch Naming Convention:**

- Use `dev1/` prefix for all your branches
- Branch name should describe the feature clearly
- Examples: `dev1/image-detection`, `dev1/medical-codes-icd10`, `dev1/medical-codes-api`

**Recommended Branching Structure:**

```bash
# Day 1-2: Image Detection Feature
git checkout -b dev1/image-detection
# Work on AI image detection implementation
git add services/image_analysis/
git commit -m "feat: Add AI-generated image detector with HuggingFace model"
git commit -m "feat: Add manipulation detection using OpenCV ELA"
git commit -m "feat: Add metadata analyzer for EXIF data"
git push -u origin dev1/image-detection

# Day 2-3: Medical Codes - ICD-10
git checkout -b dev1/medical-codes-icd10
# Populate ICD-10 codes database
git add data/medical_codes/icd10_codes.py
git commit -m "feat: Add 150 ICD-10 diagnosis codes with risk weights"
git push -u origin dev1/medical-codes-icd10

# Day 3: Medical Codes - CPT, NDC, HCPCS
git checkout -b dev1/medical-codes-extended
# Populate CPT, NDC, HCPCS codes
git add data/medical_codes/cpt_codes.py
git add data/medical_codes/ndc_codes.py
git add data/medical_codes/hcpcs_codes.py
git commit -m "feat: Add 200+ CPT procedure codes with cost estimates"
git commit -m "feat: Add 100 NDC medication codes with risk classifications"
git commit -m "feat: Add 30+ HCPCS codes for DME and services"
git push -u origin dev1/medical-codes-extended

# Day 4: Medical Codes API
git checkout -b dev1/medical-codes-api
# Create API endpoints for medical codes
git add api/medical_code_routes.py
git add api/medical_code_models.py
git commit -m "feat: Add medical code lookup endpoint"
git commit -m "feat: Add batch medical code analysis endpoint"
git commit -m "test: Add integration tests for medical code APIs"
git push -u origin dev1/medical-codes-api

# Day 5: Integration & Documentation
git checkout -b dev1/integration-docs
# Final integration and documentation
git add tests/test_image_analysis.py
git add tests/test_medical_codes.py
git add IMAGE_DETECTION.md
git add MEDICAL_CODES.md
git commit -m "docs: Add comprehensive image detection documentation"
git commit -m "docs: Add medical codes usage guide"
git commit -m "test: Add end-to-end integration tests"
git push -u origin dev1/integration-docs
```

**Best Practices:**

1. **Create branches from main/First-commit-branch:**

   ```bash
   git checkout First-commit-branch
   git pull origin First-commit-branch
   git checkout -b dev1/your-feature-name
   ```
2. **Commit messages format:**

   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `test:` - Test additions/changes
   - `refactor:` - Code refactoring
3. **Keep branches focused:**

   - One branch per major feature/component
   - Don't mix image detection with medical codes in same branch
4. **Push regularly:**

   ```bash
   # Always use -u flag on first push
   git push -u origin dev1/branch-name

   # Subsequent pushes
   git push
   ```
5. **Sync with main branch regularly:**

   ```bash
   git checkout First-commit-branch
   git pull origin First-commit-branch
   git checkout dev1/your-feature
   git merge First-commit-branch
   # Resolve conflicts if any
   git push
   ```
6. **Create Pull Requests:**

   - After completing a feature, create PR to First-commit-branch
   - Request code review from Developer 2 or team lead
   - Address review comments before merging

---

## Success Criteria

✅ Image detection API returns accurate suspicion scores
✅ All 4 medical code databases populated (400+ total codes)
✅ Endpoints fully functional with Swagger docs
✅ Unit tests passing (80%+ coverage)
✅ Integration with existing risk assessment workflow
✅ Clear documentation for other developers

---

## Timeline (Nov 24-28, 2025)

- **Day 1 (Mon, Nov 24):** Image detection research + AI model integration setup
- **Day 2 (Tue, Nov 25):** Image API implementation + medical codes (ICD-10)
- **Day 3 (Wed, Nov 26):** Medical codes database (CPT, NDC, HCPCS)
- **Day 4 (Thu, Nov 27):** Medical code API endpoints + integration testing
- **Day 5 (Fri, Nov 28):** Image detection testing + documentation + code review

**Coordinate with Developer 2** on Day 4 for medical codes integration into risk calculators.
