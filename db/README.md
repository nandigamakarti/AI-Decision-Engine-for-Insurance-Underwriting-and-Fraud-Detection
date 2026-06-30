# Database Schema Documentation

## Overview

This directory contains the database layer for the Insurance Risk Assessment Engine. The schema is designed to support the **7-JSON data extraction model** for comprehensive risk assessment.

## Database Configuration

- **Database**: PostgreSQL
- **Connection**: Configured via `DATABASE_URL` environment variable
- **ORM**: SQLAlchemy
- **Auto-Migration**: Tables are automatically created on application startup

## Files

- `database.py` - Database connection, session management, and initialization
- `models.py` - SQLAlchemy ORM models for all 15 tables
- `__init__.py` - Module exports

## Database Tables (15 Total)

### 1. Core Proposal & Policy Tables (3)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `proposal_details` | Main proposal/application data | proposal_num, policy_number, agent_code, sum_insured |
| `member_details` | Individual insured person details | member_id, policy_number, age, gender |
| `product_details` | Insurance product catalog | product_id, product_name, waiting_period |

### 2. Medical & Lifestyle Tables (2)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `chronic_disease_details` | Pre-existing diseases (PED) | proposal_number, is_diabetes, is_hypertension |
| `product_sub_question_mapping` | Lifestyle questionnaire responses | smoking, alcohol, surgeries |

### 3. Financial & KYC Tables (2)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `kyc_details` | Identity verification, AML checks | proposal_num, kyc_status, aml_check, face_match |
| `payment_details` | Payment transactions | proposal_id, payment_status, amount |

### 4. Region & Location Tables (2)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `lead_details` | Customer location data | lead_id, city, state, zip_code, zone |
| `blacklisted_hospitals` | Fraud-flagged hospitals | hospital_name, pincode, city |

### 5. Claims & Agent Tables (3)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `claim_details` | Historical claims | claim_number, member_id, claimed_amount, rejection_reason |
| `agent_details` | Agent/broker information | agent_code, agent_category, channel |
| `annual_club_performance` | Agent performance metrics | agent_code, loss_ratio, persistency |

### 6. Missing Dimension Tables (3 NEW)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `hospital_master` | Network hospitals database | hospital_id, pincode, city_id, state_id |
| `agent_risk_scores` | Pre-calculated agent risk | agent_code, loss_ratio, lapse_rate, risk_category |
| `portability_details` | Previous policy info | proposal_num, previous_insurer, first_inception_date |

## Performance Indexes

The following indexes are automatically created:

- **Primary Keys**: All `id` and unique identifier columns
- **Foreign Key Lookups**: 
  - `proposal_details.proposal_num`
  - `member_details.policy_number`
  - `agent_details.agent_code`
  - `claim_details.member_id`
- **Geographic Queries**:
  - `hospital_master.pincode`
  - `hospital_master(city_id, state_id)` (composite)
- **Search Optimization**:
  - `hospital_master.hospital_name`
  - `lead_details.lead_id`

## Usage

### Initialize Database

The database is automatically initialized when the FastAPI application starts:

```python
# In main.py
from db import init_db

@app.on_event("startup")
async def startup_event():
    init_db()  # Creates all tables if they don't exist
```

### Get Database Session

Use the `get_db()` dependency in FastAPI routes:

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from db import get_db

@app.get("/proposals/{proposal_num}")
def get_proposal(proposal_num: str, db: Session = Depends(get_db)):
    from db.models import ProposalDetails
    proposal = db.query(ProposalDetails).filter(
        ProposalDetails.proposal_num == proposal_num
    ).first()
    return proposal
```

### Query Examples

```python
from sqlalchemy.orm import Session
from db.models import ProposalDetails, MemberDetails, ClaimDetails

# Get proposal with member details
def get_proposal_with_members(db: Session, proposal_num: str):
    proposal = db.query(ProposalDetails).filter(
        ProposalDetails.proposal_num == proposal_num
    ).first()
    
    members = db.query(MemberDetails).filter(
        MemberDetails.policy_number == proposal.policy_number
    ).all()
    
    return {"proposal": proposal, "members": members}

# Get claims for a member
def get_member_claims(db: Session, member_id: str):
    claims = db.query(ClaimDetails).filter(
        ClaimDetails.member_id == member_id
    ).all()
    return claims

# Check if hospital is blacklisted
def is_hospital_blacklisted(db: Session, hospital_name: str):
    from db.models import BlackListedHospitals
    result = db.query(BlackListedHospitals).filter(
        BlackListedHospitals.name_of_hospital.ilike(f"%{hospital_name}%")
    ).first()
    return result is not None
```

## Data Flow

### External Systems → Database

Other systems (LOS, KYC services, Claims systems) will insert data into these tables:

```
External System → API Endpoint → Database Tables
```

### Database → Risk Assessment

The risk assessment engine reads from these tables:

```
API Request (proposal_id) → Data Extractors → 7 JSON Datasets → Risk Calculators → AI Analysis
```

## Migration Strategy

For schema changes, use Alembic:

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head
```

## Environment Variables

Required in `.env` file:

```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

Example:
```env
DATABASE_URL=postgresql://postgres:12345@localhost:5432/uv_risk_assessment
```

## Health Check

Check database status via API:

```bash
curl http://localhost:8000/api/database-status
```

Response:
```json
{
  "status": "healthy",
  "service": "PostgreSQL",
  "database_url": "localhost:5432/uv_risk_assessment",
  "tables_count": 15,
  "tables": ["agent_details", "agent_risk_scores", ...],
  "message": "Database is connected and tables are ready"
}
```

## Important Notes

### Pre-existing Data

**Q: Should the tables contain pre-existing data?**

**A: Yes!** The tables are designed to store data from external systems:

1. **Proposal Data**: Inserted by the Loan Origination System (LOS) when a new application is submitted
2. **KYC Data**: Inserted by KYC verification services
3. **Claims Data**: Historical claims imported from the claims management system
4. **Agent Data**: Agent profiles and performance metrics from the agency management system
5. **Hospital Data**: Network and blacklisted hospital lists (master data)

### Data Sources

| Table | Data Source |
|-------|-------------|
| ProposalDetails, MemberDetails | LOS (Loan Origination System) |
| KYCDetails | KYC Verification Service |
| PaymentDetails | Payment Gateway |
| ClaimDetails | Claims Management System |
| AgentDetails, AnnualClubPerformance | Agency Management System |
| HospitalMaster, BlackListedHospitals | Master Data / Admin Panel |
| ProductDetails | Product Catalog System |
| ChronicDiseaseDetails | Medical Underwriting System |

### Auto-Creation vs. Migration

- **Development**: Tables auto-create on startup (convenient for testing)
- **Production**: Use Alembic migrations for controlled schema changes
- **Data Persistence**: Data is NOT deleted when the app restarts

## Next Steps

1. ✅ Database schema created
2. ⏳ Create data extraction services (7 extractors)
3. ⏳ Update API models to include new dimensions
4. ⏳ Integrate extractors with risk calculators
5. ⏳ Load sample data for testing

---

**Last Updated**: 2025-11-28  
**Schema Version**: 1.0  
**Total Tables**: 15
