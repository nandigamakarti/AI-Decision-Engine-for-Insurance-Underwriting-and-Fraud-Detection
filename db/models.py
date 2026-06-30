"""
SQLAlchemy database models for Insurance Risk Assessment Engine.

This module defines all 15 database tables required for the 7-JSON data extraction model:
1. Core Proposal & Policy Tables (3)
2. Medical & Lifestyle Tables (2)
3. Financial & KYC Tables (2)
4. Region & Location Tables (2)
5. Claims & Agent Tables (3)
6. Missing Dimension Tables (3)
"""

from sqlalchemy import (
    Column, Integer, String, Text, Numeric, Boolean, 
    TIMESTAMP, Date, ForeignKey, Index
)
from sqlalchemy.sql import func
from db.database import Base


# ============================================================================
# 1. CORE PROPOSAL & POLICY TABLES
# ============================================================================

class ProposalDetails(Base):
    """
    Main proposal/application table.
    Stores core information about insurance proposals.
    """
    __tablename__ = "proposal_details"

    id = Column(Integer, primary_key=True, index=True)
    proposal_num = Column(String(100), unique=True, nullable=False, index=True)
    policy_number = Column(String(50))
    lead_id = Column(String(100))
    agent_code = Column(String(100))
    product_id = Column(Integer)
    annual_income = Column(Numeric(18, 2))
    sum_insured = Column(Numeric(18, 2))
    proposer_pan = Column(String(20))
    optional_covers_json = Column(Text)  # JSON string of selected add-ons
    created_date = Column(TIMESTAMP, server_default=func.now())


class MemberDetails(Base):
    """
    Individual member/insured person details.
    Links to ProposalDetails via policy_number.
    """
    __tablename__ = "member_details"

    id = Column(Integer, primary_key=True, index=True)
    policy_number = Column(String(50), index=True)
    member_id = Column(String(50), unique=True)
    age = Column(Integer)
    gender = Column(String(50))
    height = Column(String(50))  # Stored as string, may need parsing
    weight = Column(String(50))  # Stored as string, may need parsing
    nature_of_work = Column(String(200))  # Employment status
    marital_status = Column(String(50))


class ProductDetails(Base):
    """
    Insurance product catalog.
    Defines available insurance products and their features.
    """
    __tablename__ = "product_details"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(200))
    product_code = Column(String(50))
    key_features = Column(Text)
    pre_existing_waiting_period = Column(Integer)  # In months
    co_pay_percentage = Column(Integer)


# ============================================================================
# 2. MEDICAL & LIFESTYLE TABLES (PED)
# ============================================================================

class ChronicDiseaseDetails(Base):
    """
    Pre-existing disease (PED) information.
    Tracks chronic conditions like diabetes, hypertension, etc.
    """
    __tablename__ = "chronic_disease_details"

    id = Column(Integer, primary_key=True, index=True)
    proposal_number = Column(String(50), index=True)
    is_diabetes = Column(Boolean)
    diabetes_remark = Column(String(255))
    is_hypertension = Column(Boolean)
    is_asthma = Column(Boolean)
    asthma_remark = Column(String(255))
    is_hyperlipidemia = Column(Boolean)


class ProductSubQuestionMapping(Base):
    """
    Questionnaire responses for lifestyle and medical history.
    Stores answers to questions about smoking, alcohol, surgeries, etc.
    """
    __tablename__ = "product_sub_question_mapping"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)  # Contextual link
    smoking = Column(String(255))
    alcohol = Column(String(255))
    pan_masala = Column(String(255))
    name_of_surgery = Column(String(255))
    date_of_diagnosis = Column(String(255))
    medicine_details = Column(String(255))
    medication_type = Column(String(255))
    duration = Column(String(255))


# ============================================================================
# 3. FINANCIAL & KYC TABLES
# ============================================================================

class KYCDetails(Base):
    """
    Know Your Customer (KYC) verification details.
    Stores identity verification, AML checks, and face match scores.
    """
    __tablename__ = "kyc_details"

    id = Column(Integer, primary_key=True, index=True)
    proposal_num = Column(String(50))
    risk_level = Column(String(50))  # 'High', 'Medium', 'Low'
    aml_check = Column(String(50))  # Anti-Money Laundering status
    kyc_status = Column(String(50))
    if_face_match = Column(String(10))  # Face match verification result


class PaymentDetails(Base):
    """
    Payment transaction details.
    Tracks payment status and methods for proposals.
    """
    __tablename__ = "payment_details"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(String(50))
    payment_status = Column(String(50))  # 'Failed', 'Success', 'Pending'
    amount = Column(Numeric(19, 2))
    payment_method = Column(String(50))


# ============================================================================
# 4. REGION & LOCATION TABLES
# ============================================================================

class LeadDetails(Base):
    """
    Lead/customer location information.
    Stores geographic data for geo-risk analysis.
    """
    __tablename__ = "lead_details"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(String(20), unique=True, index=True)
    city = Column(String(100))
    state_province = Column(String(100))
    zip_code = Column(String(20))
    zone = Column(String(50))  # Geographic zone classification


class BlackListedHospitals(Base):
    """
    Hospitals flagged for fraud or quality issues.
    Used to detect claims at blacklisted facilities.
    """
    __tablename__ = "blacklisted_hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name_of_hospital = Column(String(1000))
    pincode = Column(Integer)
    city_master = Column(String(255))
    address = Column(Text)


# ============================================================================
# 5. CLAIMS & AGENT TABLES
# ============================================================================

class ClaimDetails(Base):
    """
    Historical claims data.
    Stores information about past insurance claims.
    """
    __tablename__ = "claim_details"

    id = Column(Integer, primary_key=True, index=True)
    claim_number = Column(String(50), unique=True)
    member_id = Column(String(250), index=True)
    policy_number = Column(String(50))
    claimed_amount = Column(Numeric(18, 2))
    approved_amount = Column(Numeric(18, 2))
    claim_status = Column(String(200))  # 'Rejected', 'Approved', 'Pending'
    rejection_reason = Column(Text)  # Critical for fraud detection
    hospital_name = Column(String(500))
    reported_date_time = Column(TIMESTAMP)
    claim_type = Column(String(50))


class AgentDetails(Base):
    """
    Insurance agent/broker information.
    Stores agent profile and channel details.
    """
    __tablename__ = "agent_details"

    id = Column(Integer, primary_key=True, index=True)
    agent_code = Column(String(20), unique=True, index=True)
    agent_category = Column(String(100))
    channel = Column(String(100))  # Distribution channel
    created_on = Column(TIMESTAMP)  # Used to calculate years licensed


class AnnualClubPerformance(Base):
    """
    Agent performance metrics.
    Tracks agent's annual performance indicators.
    """
    __tablename__ = "annual_club_performance"

    id = Column(Integer, primary_key=True, index=True)
    agent_code = Column(String(50))
    loss_ratio = Column(String(50))  # Stored as string '80%' in source
    nop_persistency = Column(String(50))  # Number of Policies persistency
    annual_club_gwp = Column(String(500))  # Gross Written Premium


# ============================================================================
# 6. MISSING DIMENSION TABLES (NEW)
# ============================================================================

class HospitalMaster(Base):
    """
    Network hospitals database.
    Used to assess healthcare access and proximity to quality hospitals.
    """
    __tablename__ = "hospital_master"

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(String(50))
    hospital_name = Column(String(255))
    pincode = Column(String(50), index=True)
    city_id = Column(Integer, index=True)
    state_id = Column(Integer, index=True)
    hospital_address = Column(Text)

    # Composite index for city and state queries
    __table_args__ = (
        Index('idx_hospital_city_state', 'city_id', 'state_id'),
        Index('idx_hospital_name', 'hospital_name'),
    )


class AgentRiskScores(Base):
    """
    Pre-calculated agent risk scores (derived table).
    Stores clean, calculated risk metrics to avoid recalculation on every API call.
    """
    __tablename__ = "agent_risk_scores"

    agent_code = Column(String(50), primary_key=True)
    loss_ratio = Column(Numeric(5, 2))  # e.g., 65.50
    lapse_rate = Column(Numeric(5, 2))
    vintage_years = Column(Integer)
    risk_category = Column(String(20))  # 'High', 'Medium', 'Low'
    last_updated = Column(TIMESTAMP, server_default=func.now())


class PortabilityDetails(Base):
    """
    Previous policy information for portability cases.
    Used to detect waiting period fraud and validate portability claims.
    """
    __tablename__ = "portability_details"

    id = Column(Integer, primary_key=True, index=True)
    proposal_num = Column(String(100), index=True)
    previous_insurer_name = Column(String(255))
    previous_policy_number = Column(String(100))
    first_inception_date = Column(Date)  # Critical for waiting period calculation
    claims_in_previous_policy = Column(Boolean)
    portability_reason = Column(String(255))


# ============================================================================
# CREATE ALL INDEXES
# ============================================================================

# Additional indexes are created via __table_args__ in model definitions above
# The following indexes are automatically created:
# - Primary keys (automatic)
# - Unique constraints (automatic)
# - Explicit index=True columns (automatic)
# - Composite indexes defined in __table_args__
