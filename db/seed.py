"""
Database seeding script.
Populates standard mock profiles into the PostgreSQL database.
"""

import datetime
from sqlalchemy import text
from db.database import SessionLocal, init_db
from db.models import (
    ProposalDetails, MemberDetails, ProductDetails, ChronicDiseaseDetails,
    ProductSubQuestionMapping, KYCDetails, PaymentDetails, LeadDetails,
    BlackListedHospitals, ClaimDetails, AgentDetails, AnnualClubPerformance,
    HospitalMaster, AgentRiskScores, PortabilityDetails
)

def seed_data():
    init_db()
    db = SessionLocal()
    try:
        print("Clearing old data...")
        tables = [
            "claim_details", "payment_details", "kyc_details", "chronic_disease_details",
            "product_sub_question_mapping", "portability_details", "proposal_details",
            "member_details", "lead_details", "blacklisted_hospitals",
            "annual_club_performance", "agent_risk_scores", "agent_details",
            "hospital_master", "product_details"
        ]
        for t in tables:
            db.execute(text(f"TRUNCATE TABLE {t} RESTART IDENTITY CASCADE;"))
        db.commit()
        
        print("Seeding new data...")
        # 1. Product Details
        products = [
            ProductDetails(product_id=101, product_name="Care Free Life Plan", product_code="CFLP", pre_existing_waiting_period=12, co_pay_percentage=0, key_features="Comprehensive life, zero co-pay, low wait times on standard chronic triggers."),
            ProductDetails(product_id=102, product_name="Heart Care Plus", product_code="HCP", pre_existing_waiting_period=24, co_pay_percentage=10, key_features="Specialized cardiac support, co-pay mandatory on network procedures."),
            ProductDetails(product_id=103, product_name="Premier Health Shield", product_code="PHS", pre_existing_waiting_period=36, co_pay_percentage=20, key_features="Critical illness shield, high-tier hospital access network included.")
        ]
        db.add_all(products)
        
        # 2. Agent Details
        agents = [
            AgentDetails(agent_code="AGT102", agent_category="Silver Broker", channel="Direct", created_on=datetime.datetime(2020, 5, 12)),
            AgentDetails(agent_code="AGT405", agent_category="Gold Channel Partner", channel="Agency", created_on=datetime.datetime(2014, 8, 20)),
            AgentDetails(agent_code="AGT990", agent_category="Direct Brokerage", channel="Broker", created_on=datetime.datetime(2024, 11, 4))
        ]
        db.add_all(agents)
        
        # 3. Agent Risk Scores
        agent_risks = [
            AgentRiskScores(agent_code="AGT102", loss_ratio=22.5, lapse_rate=5.8, vintage_years=6, risk_category="Low"),
            AgentRiskScores(agent_code="AGT405", loss_ratio=58.4, lapse_rate=11.4, vintage_years=12, risk_category="Medium"),
            AgentRiskScores(agent_code="AGT990", loss_ratio=84.2, lapse_rate=31.5, vintage_years=2, risk_category="High")
        ]
        db.add_all(agent_risks)
        
        # 4. Annual Club Performance
        agent_perf = [
            AnnualClubPerformance(agent_code="AGT102", loss_ratio="22.5%", nop_persistency="94.2%", annual_club_gwp="500000"),
            AnnualClubPerformance(agent_code="AGT405", loss_ratio="58.4%", nop_persistency="88.6%", annual_club_gwp="1200000"),
            AnnualClubPerformance(agent_code="AGT990", loss_ratio="84.2%", nop_persistency="68.5%", annual_club_gwp="250000")
        ]
        db.add_all(agent_perf)
        
        # 5. Lead Details
        leads = [
            LeadDetails(lead_id="L_PROP001", city="Chicago", state_province="IL", zip_code="60601", zone="Central"),
            LeadDetails(lead_id="L_PROP002", city="Orlando", state_province="FL", zip_code="32801", zone="South"),
            LeadDetails(lead_id="L_PROP003", city="Los Angeles", state_province="CA", zip_code="90001", zone="West")
        ]
        db.add_all(leads)
        
        # 6. Hospital Master
        hospitals = [
            HospitalMaster(hospital_id="HOSP01", hospital_name="Saint Mercy General Hospital", pincode="32801", city_id=1, state_id=1, hospital_address="123 Health Ave, Orlando, FL"),
            HospitalMaster(hospital_id="HOSP02", hospital_name="Orange Medical Center", pincode="32801", city_id=1, state_id=1, hospital_address="456 Care Blvd, Orlando, FL"),
            HospitalMaster(hospital_id="HOSP03", hospital_name="Downtown General Hospital", pincode="90001", city_id=2, state_id=2, hospital_address="789 Main St, Los Angeles, CA"),
            HospitalMaster(hospital_id="HOSP04", hospital_name="Valley West Hospital", pincode="90001", city_id=2, state_id=2, hospital_address="101 West Rd, Los Angeles, CA")
        ]
        db.add_all(hospitals)
        
        # 7. BlackListed Hospitals
        blacklisted = [
            BlackListedHospitals(name_of_hospital="Mercy Wellness Clinic", pincode=32801, city_master="Orlando", address="999 Fraud St, Orlando, FL")
        ]
        db.add_all(blacklisted)
        
        # 8. Proposal Details
        proposals = [
            ProposalDetails(proposal_num="PROP001", policy_number="POL889102", lead_id="L_PROP001", agent_code="AGT102", product_id=101, annual_income=125000.0, sum_insured=500000.0, proposer_pan="ABCDE1234F", created_date=datetime.datetime(2026, 6, 15)),
            ProposalDetails(proposal_num="PROP002", policy_number="POL992811", lead_id="L_PROP002", agent_code="AGT405", product_id=102, annual_income=75000.0, sum_insured=800000.0, proposer_pan="FGHIJ5678K", created_date=datetime.datetime(2026, 6, 14)),
            ProposalDetails(proposal_num="PROP003", policy_number="POL118273", lead_id="L_PROP003", agent_code="AGT990", product_id=103, annual_income=220000.0, sum_insured=1200000.0, proposer_pan="KLMNO9012L", created_date=datetime.datetime(2026, 6, 13))
        ]
        db.add_all(proposals)
        
        # 9. Member Details
        members = [
            MemberDetails(policy_number="POL889102", member_id="MEM001", age=32, gender="Male", height="175cm", weight="70kg", nature_of_work="Office Executive", marital_status="Single"),
            MemberDetails(policy_number="POL992811", member_id="MEM002", age=58, gender="Female", height="160cm", weight="65kg", nature_of_work="Teacher", marital_status="Married"),
            MemberDetails(policy_number="POL118273", member_id="MEM003", age=46, gender="Male", height="180cm", weight="95kg", nature_of_work="Business Owner", marital_status="Married")
        ]
        db.add_all(members)
        
        # 10. Chronic Disease Details
        chronic = [
            ChronicDiseaseDetails(proposal_number="PROP001", is_diabetes=False, is_hypertension=False, is_asthma=False, is_hyperlipidemia=False),
            ChronicDiseaseDetails(proposal_number="PROP002", is_diabetes=True, diabetes_remark="Type 2 Diabetes, controlled with metformin", is_hypertension=True, is_asthma=False, is_hyperlipidemia=False),
            ChronicDiseaseDetails(proposal_number="PROP003", is_diabetes=True, diabetes_remark="Type 2 Diabetes, uncontrolled", is_hypertension=True, is_asthma=True, asthma_remark="Mild asthma, uses inhaler occasionally", is_hyperlipidemia=True)
        ]
        db.add_all(chronic)
        
        # 11. KYC Details
        kyc = [
            KYCDetails(proposal_num="PROP001", risk_level="Low", aml_check="Passed", kyc_status="Verified", if_face_match="98%"),
            KYCDetails(proposal_num="PROP002", risk_level="Low", aml_check="Passed", kyc_status="Verified", if_face_match="95%"),
            KYCDetails(proposal_num="PROP003", risk_level="High", aml_check="Warning Flags", kyc_status="High Risk Flags", if_face_match="82%")
        ]
        db.add_all(kyc)
        
        # 12. Claim Details
        claims = [
            ClaimDetails(claim_number="CLM99201", member_id="MEM002", policy_number="POL992811", claimed_amount=12500.0, approved_amount=11000.0, claim_status="Approved", hospital_name="Saint Mercy General Hospital", reported_date_time=datetime.datetime(2024, 8, 12), claim_type="Medical Surgery"),
            ClaimDetails(claim_number="CLM99827", member_id="MEM002", policy_number="POL992811", claimed_amount=4500.0, approved_amount=4500.0, claim_status="Approved", hospital_name="Orange Medical Center", reported_date_time=datetime.datetime(2025, 1, 20), claim_type="Outpatient Check"),
            ClaimDetails(claim_number="CLM11204", member_id="MEM003", policy_number="POL118273", claimed_amount=35000.0, approved_amount=0.0, claim_status="Rejected", rejection_reason="Pre-existing condition clause violation: Undisclosed diabetes history", hospital_name="Downtown General Hospital", reported_date_time=datetime.datetime(2023, 11, 4), claim_type="Diabetes Complication Crisis"),
            ClaimDetails(claim_number="CLM11822", member_id="MEM003", policy_number="POL118273", claimed_amount=18000.0, approved_amount=18000.0, claim_status="Approved", hospital_name="Valley West Hospital", reported_date_time=datetime.datetime(2024, 4, 15), claim_type="Cardiology Monitoring Session"),
            ClaimDetails(claim_number="CLM12045", member_id="MEM003", policy_number="POL118273", claimed_amount=8500.0, approved_amount=4000.0, claim_status="Approved", hospital_name="Downtown General Hospital", reported_date_time=datetime.datetime(2024, 9, 2), claim_type="Hypertensive Crisis Emergency")
        ]
        db.add_all(claims)
        
        # 13. Payment Details
        payments = [
            PaymentDetails(proposal_id="PROP001", payment_status="Success", amount=1200.0, payment_method="Credit Card"),
            PaymentDetails(proposal_id="PROP002", payment_status="Success", amount=2500.0, payment_method="Net Banking"),
            PaymentDetails(proposal_id="PROP003", payment_status="Success", amount=4500.0, payment_method="Debit Card")
        ]
        db.add_all(payments)
        
        # 14. Product Sub Question Mapping (Lifestyle/Medical Questionnaire responses)
        question_mappings = [
            ProductSubQuestionMapping(product_id=101, smoking="No", alcohol="Socially", pan_masala="No", name_of_surgery="None", date_of_diagnosis="None", medicine_details="None", medication_type="None", duration="None"),
            ProductSubQuestionMapping(product_id=102, smoking="No", alcohol="Regularly", pan_masala="No", name_of_surgery="None", date_of_diagnosis="2020-01-01", medicine_details="Metformin 500mg", medication_type="Oral Hypoglycemic", duration="5 years"),
            ProductSubQuestionMapping(product_id=103, smoking="Yes (Pack a day)", alcohol="Frequently", pan_masala="No", name_of_surgery="Appendectomy", date_of_diagnosis="2018-05-15", medicine_details="Metformin 1000mg, Lisinopril 10mg, Albuterol Inhaler", medication_type="Oral/Inhaled", duration="8 years")
        ]
        db.add_all(question_mappings)
        
        # 15. Portability Details
        portability = [
            PortabilityDetails(proposal_num="PROP003", previous_insurer_name="Star Health Insurance", previous_policy_number="STAR-99201", first_inception_date=datetime.date(2020, 10, 1), claims_in_previous_policy=True, portability_reason="Premium cost and better network hospital coverage")
        ]
        db.add_all(portability)
        
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
