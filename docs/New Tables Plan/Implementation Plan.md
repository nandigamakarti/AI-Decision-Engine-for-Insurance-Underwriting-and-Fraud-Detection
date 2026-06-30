Implementation Plan: Insurance Risk Assessment Engine Optimization

This document outlines the step-by-step execution plan to upgrade the Risk Assessment Engine database schema, API contracts, and logic.

Refer : docs\New Tables Plan\postgres CREATE table queries.md for actual Table Creation Queries.

## 🤖 Instructions for Claude

1. **Read Context:** Before starting, review the project structure to identify where SQL files and Pydantic models are located.
2. **Sequential Execution:** Perform tasks in order. Do not skip phases.
3. **Checklist Management:** After completing a specific task, edit this file (`implementation_plan.md`) and change `[ ]` to `[x]`.
4. **Documentation:**
   * Update `CHANGELOG.md` after every major Phase completion.
   * Update `CLAUDE.md` if new standard commands or architectural decisions are made.
   * Update `README.md` with the latest schema details and API capabilities upon completion.

---

## Phase 1: Database Schema Overhaul

*Objective: Implement the optimized PostgreSQL schema to support the 7-JSON data extraction model.*

### 1.1 Core Proposal & Policy Tables

- [ ] Create/Update `ProposalDetails` table (ensure `OptionalCoversJson` is TEXT).
- [ ] Create/Update `MemberDetails` table (parse Height/Weight logic if needed later).
- [ ] Create/Update `ProductDetails` table.

### 1.2 Medical & Lifestyle (PED)

- [ ] Create/Update `ChronicDiseaseDetails` table.
- [ ] Create/Update `ProductSubQuestionMapping` table (for questionnaire responses).

### 1.3 Financial & KYC

- [ ] Create/Update `KYCDetails` table.
- [ ] Create/Update `PaymentDetails` table.

### 1.4 Region & Location

- [ ] Create/Update `LeadDetails` table.
- [ ] Create/Update `BlackListedHostpitals` table.

### 1.5 Claims & Agent

- [ ] Create/Update `ClaimDetails` table (ensure `RejectionReason` is present).
- [ ] Create/Update `AgentDetails` table.
- [ ] Create/Update `AnnualClubPerformance` table.

### 1.6 Missing Dimensions (New Tables)

- [ ] Create `HospitalMaster` table (Network Hospitals).
- [ ] Create `AgentRiskScores` table (Derived/Pre-calculated risk).
- [ ] Create `PortabilityDetails` table (For churn/waiting period fraud).

### 1.7 Performance Optimization

- [ ] Apply indexes on `ProposalDetails(ProposalNum)` and `MemberDetails(PolicyNumber)`.
- [ ] Apply indexes on `ChronicDiseaseDetails`, `ClaimDetails`, and `AgentDetails`.
- [ ] Apply critical geo-indexes: `HospitalMaster(Pincode)` and `HospitalMaster(CityId, StateId)`.
- [ ] Apply index on `PortabilityDetails(ProposalNum)`.

---

## Phase 2: API Request Schema Update

*Objective: Update the FastAPI Pydantic models to accept the missing risk dimensions.*

### 2.1 Update Pydantic Models

- [ ] Locate the main request model file (e.g., `schemas.py` or `models.py`).
- [ ] Add `policy_info` object (Sum Insured, Term, Portability flag).
- [ ] Update `personal_info` to include `pincode`, `city`, and `zone`.
- [ ] Add `agent_info` object (Code, Category, Loss Ratio, Vintage).
- [ ] Add `kyc_verification` object (PAN, AML check, Face match score).
- [ ] Update `claims_history` to include `is_blacklisted_hospital_involved`.

### 2.2 Input Validation

- [ ] Ensure proper types (enums for Risk Levels, numeric validation for income/loss ratios).

---

## Phase 3: Data Logic & Integration

*Objective: Implement the extraction of the 7 specific JSON datasets and integration with the LLM.*

### 3.1 Data Extraction Layer

- [ ] Write SQL/ORM queries to fetch **Demographic JSON** data.
- [ ] Write SQL/ORM queries to fetch **Financial JSON** data.
- [ ] Write SQL/ORM queries to fetch **Medical/PED JSON** data.
- [ ] Write SQL/ORM queries to fetch **Region JSON** (joining Lead + HospitalMaster).
- [ ] Write SQL/ORM queries to fetch **Claims JSON**.
- [ ] Write SQL/ORM queries to fetch **Agent JSON** (joining AgentDetails + RiskScores).
- [ ] Write SQL/ORM queries to fetch **Product JSON**.

### 3.2 Service Layer Logic

- [ ] Update the `/api/risk-assessment` endpoint controller.
- [ ] Implement logic to receive the expanded POST request.
- [ ] Map API inputs to the Database tables (if persisting) or prepare them for the LLM prompt.
- [ ] Construct the prompt context using the 7 data dimensions.

---

## Phase 4: Documentation & Finalization

### 4.1 Documentation Updates

- [ ] Create/Update `CLAUDE.md` with project commands and architecture summary.
- [ ] Create/Update `CHANGELOG.md` with a summary of the database and API changes.
- [ ] Update `README.md` to reflect the new "Multi-Dimensional Risk Assessment" capabilities.

### 4.2 Verification

- [ ] Run a test SQL script to verify all tables and indexes exist.
- [ ] Test the API endpoint with the new JSON payload structure to ensure no validation errors.

---

## Appendix: File Templates

### `CLAUDE.md` Template

*(Create this if it does not exist)*

```markdown
# CLAUDE.md

## Project Overview
Insurance Risk Assessment API using FastAPI and PostgreSQL.
This system analyzes customer data, agent performance, and geo-data to calculate insurance risk scores.

## Commands
- Run Server: `uvicorn app.main:app --reload`
- Database Migration: `alembic upgrade head` (or specific SQL script runner)
- Run Tests: `pytest`

## Architecture Notes
- **Database:** PostgreSQL with 3 distinct risk categories (Personal, Geo, Agent).
- **API:** FastAPI.
- **Risk Logic:** 7-point JSON extraction passed to LLM for final scoring.
```

### `CHANGELOG.md` Template

*(Create this if it does not exist)*

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- **Database:** New tables `HospitalMaster`, `AgentRiskScores`, `PortabilityDetails`.
- **Database:** Performance indexes for Proposal, Pincode, and Agent lookups.
- **API:** Added `agent_info`, `kyc_verification`, and `policy_info` to risk assessment payload.

### Changed
- Refactored `ProposalDetails` and `MemberDetails` to support new optional covers and physical attributes.
- Optimized Risk Assessment algorithm to consider Geo-location and Agent Vintage.
```
