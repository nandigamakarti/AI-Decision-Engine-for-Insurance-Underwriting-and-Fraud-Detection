
# GEMINI Project: AI-Assisted Insurance Underwriting PoC

## Executive Summary

This document outlines a 4-week Proof of Concept (PoC) to evaluate the feasibility of using the **GPT-OSS-120B** model to automate and enhance the insurance underwriting risk assessment process. The goal is to demonstrate significant improvements in accuracy, speed, and decision support for underwriters by processing application documents and generating actionable insights.

---

### 1. Objective

The primary objective of this PoC is to demonstrate how GPT-OSS-120B can:

- Analyze unstructured documents including proposal forms, KYC documents, and medical reports.
- Extract relevant underwriting data points and entities.
- Generate concise, accurate risk summaries and flag anomalies.
- Provide underwriters with data-driven decision support.
- Reduce the overall underwriting turnaround time (TAT).

---

### 2. PoC Scope

#### In-Scope

- Processing of PDF documents (proposal forms, lab reports, ID proofs).
- Data extraction and entity classification.
- Automated generation of risk summaries.
- Rule-based cross-checking of data against underwriting guidelines.
- Flagging of anomalies, inconsistencies, and potential fraud indicators.
- Integration via REST API endpoints for consumption by other systems.

#### Out-of-Scope (for this PoC)

- End-to-end integration with the core Loan Origination System (LOS).
- Actuarial premium computation and pricing.
- Development of a full-fledged fraud scoring engine.
- Real-time, production-scale deployment.

---

### 3. Target Users

- **Underwriters:** Primary users for reviewing AI-generated summaries and making decisions.
- **Quality Analysts:** For validating the accuracy and consistency of the model's output.
- **Business Analysts:** For assessing the business impact and process improvements.
- **Engineering Team:** For providing feedback on API design and integration feasibility.

---

### 4. Success Criteria

The success of this PoC will be measured against the following key performance indicators (KPIs):

| Category                       | KPI                                            | Target        |
| ------------------------------ | ---------------------------------------------- | ------------- |
| **Extraction Accuracy**  | Correct extraction of key data fields          | ≥ 85%        |
| **Risk Summary Quality** | Underwriter satisfaction score                 | ≥ 4 out of 5 |
| **Anomaly Detection**    | Correctly flags intentionally seeded anomalies | ≥ 70%        |
| **Processing Speed**     | Reduction in manual document review time       | ≥ 50%        |
| **Integration**          | API output is usable by a UI/LOS frontend      | Pass / Fail   |

---

### 5. Dataset Requirements

A minimum of **50-100 sample sets** are required. Anonymized data from **Care Health Insurance** is preferred.

#### Documents

- [ ] Proposal Forms
- [ ] KYC Documents (Aadhaar, PAN, Passport)
- [ ] Medical / Lab Reports
- [ ] Past Claims History Documents
- [ ] Income Proofs
- [ ] Customer Declarations

#### Metadata (for validation)

- [ ] Known risk factors for each case.
- [ ] Original underwriter comments.
- [ ] Final decision (Approved / Rejected) and reasons.
- [ ] Product category (Health / Life / Motor).

---

### 6. Technical Architecture (Proposed)

The proposed architecture follows a multi-stage pipeline from document ingestion to final review.

```text
┌────────────────────────┐
│  Document Upload API   │
└─────────────┬──────────┘
              │
┌─────────────▼──────────┐
│ Preprocessing Pipeline │
│ OCR → Text Clean → Chunking │
└─────────────┬──────────┘
              │
┌─────────────▼──────────┐
│    GPT-OSS-120B Engine │
│ Extraction | Risk Summary │
│ Anomaly Detection | Scores │
└─────────────┬──────────┘
              │
┌─────────────▼──────────┐
│     Output JSON API    │
│ Entities | Summary | Flags │
└─────────────┬──────────┘
              │
┌─────────────▼──────────┐
│ Underwriter Review Dash│
└────────────────────────┘
```

---

### 7. PoC Timeline & Deliverables (4 Weeks)

#### Week 1: Preparation

- **Tasks:** Finalize use case details, gather and anonymize sample documents, set up GPU VM environment, deploy GPT-OSS-120B container, and create the target JSON extraction schema.
- **Deliverable:** Environment ready for development; final data schema definition.

#### Week 2: Extraction & Analysis

- **Tasks:** Implement the OCR/PDF parsing pipeline Azure IDP API, develop and refine extraction prompts for the model, build the risk summary generation logic, and create a rule-based anomaly checker.
- **Deliverable:** A working data pipeline that can extract entities and generate summaries from documents.

#### Week 3: Integration & UAT

- **Tasks:** Develop REST APIs to expose the pipeline, generate structured JSON output for each document set, create a simple review UI (optional), and conduct User Acceptance Testing (UAT) with underwriters.
- **Deliverable:** API-enabled PoC with a functional preview interface for feedback.

#### Week 4: Evaluation & Reporting

- **Tasks:** Measure performance against the defined KPIs, present findings to stakeholders, perform a comparative analysis of manual vs. AI-assisted underwriting, and identify gaps and next steps.
- **Deliverable:** Final PoC report with performance metrics and a production rollout recommendation.

---

### 8. Team Roles & Responsibilities

| Role                               | Responsibilities                                             |
| ---------------------------------- | ------------------------------------------------------------ |
| **PoC Owner / Project Lead** | Owns the PoC, reviews progress, aligns with business goals.  |
| **Engineering Manager**      | Manages resource allocation, reviews technical architecture. |
| **Backend Team**             | Implements APIs, integration logic, and pipeline backend.    |
| **AI/ML Engineer**           | Manages the model, prompt engineering, fine-tuning.          |
| **Underwriters**             | Provide domain expertise, validate outputs, give feedback.   |
| **QA Team**                  | Tests inputs, outputs, and overall functionality.            |

---

### 9. Tools & Technology Stack

- **AI/ML:**
  - GPT-OSS-120B (Primary Model)
  - Tesseract / AWS Textract (for OCR)
  - Python, FastAPI
- **Integration:**
  - PostgreSQL (Optional, for metadata)
  - Redis (for async task queueing)
- **UI (Optional):**
  - Angular

---

### 10. Risks & Mitigation

| Risk                             | Mitigation Strategy                                              |
| -------------------------------- | ---------------------------------------------------------------- |
| **Poor OCR Text Quality**  | Improve preprocessing steps; use a robust service like Textract. |
| **PII Data Leakage**       | Run the model in a secure, on-premise environment.               |
| **Insufficient Documents** | Use synthetic data generation techniques to augment the dataset. |
| **Model Hallucination**    | Implement a rule-based validation layer to cross-check outputs.  |

---

### 11. Final PoC Output

At the conclusion of this PoC, the team will deliver:

- A working prototype capable of processing underwriting documents.
- A system that auto-generates risk summaries and anomaly flags.
- A comprehensive report demonstrating measurable TAT improvement and accuracy metrics.
- A clear blueprint for developing a production-grade underwriting assistance engine.
