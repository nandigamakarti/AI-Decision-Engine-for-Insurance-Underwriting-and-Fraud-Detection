Here are the PostgreSQL `CREATE TABLE` queries optimized for the 7 JSON datasets you need to generate.

### 1. Core Proposal & Policy Tables
*Used in almost every JSON generation (Demographic, Financial, Product).*

```sql
CREATE TABLE ProposalDetails (
    Id SERIAL PRIMARY KEY,
    ProposalNum VARCHAR(100) UNIQUE NOT NULL,
    PolicyNumber VARCHAR(50),
    LeadId VARCHAR(100),
    AgentCode VARCHAR(100),
    ProductId INTEGER,
    AnnualIncome NUMERIC(18, 2),
    SumInsured NUMERIC(18, 2),
    ProposerPAN VARCHAR(20),
    OptionalCoversJson TEXT, -- Stores JSON string of selected addons
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE MemberDetails (
    Id SERIAL PRIMARY KEY,
    PolicyNumber VARCHAR(50), -- Links to ProposalDetails
    MemberId VARCHAR(50) UNIQUE,
    Age INTEGER,
    Gender VARCHAR(50),
    Height VARCHAR(50), -- Stored as string in source, likely needs parsing
    Weight VARCHAR(50),
    NatureOfWork VARCHAR(200), -- Employment Status
    MaritalStatus VARCHAR(50)
);

CREATE TABLE ProductDetails (
    ProductId INTEGER PRIMARY KEY,
    ProductName VARCHAR(200),
    ProductCode VARCHAR(50),
    KeyFeatures TEXT,
    PreExistingWaitingPeriod INTEGER,
    CoPayPercentage INTEGER
);
```

### 2. Medical & Lifestyle Tables (PED JSON)
*Used to extract conditions, surgeries, and habits.*

```sql
CREATE TABLE ChronicDiseaseDetails (
    Id SERIAL PRIMARY KEY,
    ProposalNumber VARCHAR(50), -- Links to ProposalDetails
    IsDiabetes BOOLEAN,
    DiabetesRemark VARCHAR(255),
    IsHypertension BOOLEAN,
    IsAsthma BOOLEAN,
    AsthmaRemark VARCHAR(255),
    IsHyperlipidemia BOOLEAN
);

-- Stores questionnaire responses (Smoking, Alcohol, Surgeries)
CREATE TABLE ProductSubQuestionMapping (
    Id SERIAL PRIMARY KEY,
    ProductId INTEGER, -- Contextual link
    Smoking VARCHAR(255),
    Alcohol VARCHAR(255),
    PanMasala VARCHAR(255),
    NameOfSurgery VARCHAR(255),
    DateOfDiagnosis VARCHAR(255),
    MedicineDetails VARCHAR(255),
    MedicationType VARCHAR(255),
    Duration VARCHAR(255)
);
```

### 3. Financial & KYC Tables (Financial JSON)
*Used for credit checks, AML, and payment history.*

```sql
CREATE TABLE KYCDetails (
    Id SERIAL PRIMARY KEY,
    ProposalNum VARCHAR(50),
    RiskLevel VARCHAR(50), -- e.g., 'High', 'Low'
    AmlCheck VARCHAR(50),
    KycStatus VARCHAR(50),
    IfFaceMatch VARCHAR(10)
);

CREATE TABLE PaymentDetails (
    Id SERIAL PRIMARY KEY,
    ProposalId VARCHAR(50), -- Links to ProposalDetails.ProposalNum
    PaymentStatus VARCHAR(50), -- e.g., 'Failed', 'Success'
    Amount NUMERIC(19, 2),
    PaymentMethod VARCHAR(50)
);
```

### 4. Region & Location Tables (Region JSON)
*Used for geo-risk and hospital proximity.*

```sql
CREATE TABLE LeadDetails (
    Id SERIAL PRIMARY KEY,
    LeadID VARCHAR(20) UNIQUE,
    City VARCHAR(100),
    StateProvince VARCHAR(100),
    ZipCode VARCHAR(20),
    Zone VARCHAR(50)
);

CREATE TABLE BlackListedHostpitals (
    Id SERIAL PRIMARY KEY,
    NameofHospital VARCHAR(1000),
    Pincode INTEGER, -- Used to match against Lead ZipCode
    CityMaster VARCHAR(255),
    Address TEXT
);
```

### 5. Claims Tables (Claims JSON)
*Used for claims history and fraud detection.*

```sql
CREATE TABLE ClaimDetails (
    Id SERIAL PRIMARY KEY,
    ClaimNumber VARCHAR(50) UNIQUE,
    MemberId VARCHAR(250), -- Links to MemberDetails
    PolicyNumber VARCHAR(50),
    ClaimedAmount NUMERIC(18, 2),
    ApprovedAmount NUMERIC(18, 2),
    ClaimStatus VARCHAR(200), -- 'Rejected', 'Approved'
    RejectionReason TEXT, -- Critical for fraud detection
    HospitalName VARCHAR(500),
    ReportedDateTime TIMESTAMP,
    ClaimType VARCHAR(50)
);
```

### 6. Agent Tables (Agent JSON)
*Used for agent risk scoring.*

```sql
CREATE TABLE AgentDetails (
    Id SERIAL PRIMARY KEY,
    AgentCode VARCHAR(20) UNIQUE,
    AgentCategory VARCHAR(100),
    Channel VARCHAR(100),
    CreatedOn TIMESTAMP -- Used to calc years licensed
);

CREATE TABLE AnnualClubPerformance (
    Id SERIAL PRIMARY KEY,
    AgentCode VARCHAR(50), -- Links to AgentDetails
    LossRatio VARCHAR(50), -- Stored as string '80%' in source
    NOPPersistency VARCHAR(50),
    AnnualClubGWP VARCHAR(500) -- Gross Written Premium
);
```


#### 7. `HospitalMaster` (Network Hospitals)
*Why:* You need to know if the customer lives near *Network* hospitals (Good) or only *Blacklisted* hospitals (Bad).
```sql
CREATE TABLE HospitalMaster (
    Id SERIAL PRIMARY KEY,
    HospitalId VARCHAR(50),
    HospitalName VARCHAR(255),
    Pincode VARCHAR(50), -- To match with Customer Pincode
    CityId INTEGER,
    StateId INTEGER,
    HospitalAddress TEXT
);
CREATE INDEX idx_hospital_pincode ON HospitalMaster(Pincode);
```

#### 8. `AgentRiskScores` (Derived Table)
*Why:* The raw `AnnualClubPerformance` table in the source DB is messy. For the API, it is better to have a clean table that stores the pre-calculated risk score of an agent so the API doesn't have to calculate it every time.
```sql
CREATE TABLE AgentRiskScores (
    AgentCode VARCHAR(50) PRIMARY KEY,
    LossRatio NUMERIC(5,2), -- e.g., 65.50
    LapseRate NUMERIC(5,2),
    VintageYears INTEGER,
    RiskCategory VARCHAR(20), -- 'High', 'Medium', 'Low'
    LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 9. `PortabilityDetails` (If applicable)
*Why:* If `is_portability` is true, you need details of the previous policy to check for "Waiting Period" fraud.
```sql
CREATE TABLE PortabilityDetails (
    Id SERIAL PRIMARY KEY,
    ProposalNum VARCHAR(100),
    PreviousInsurerName VARCHAR(255),
    PreviousPolicyNumber VARCHAR(100),
    FirstInceptionDate DATE, -- Critical for calculating waiting periods
    ClaimsInPreviousPolicy BOOLEAN,
    PortabilityReason VARCHAR(255)
);
CREATE INDEX idx_portability_proposal ON PortabilityDetails(ProposalNum);
```

### Indexes for Performance
Since your API will query these tables by specific IDs, run these to ensure the API is fast:

```sql
CREATE INDEX idx_proposal_num ON ProposalDetails(ProposalNum);
CREATE INDEX idx_member_policy ON MemberDetails(PolicyNumber);
CREATE INDEX idx_chronic_proposal ON ChronicDiseaseDetails(ProposalNumber);
CREATE INDEX idx_claims_member ON ClaimDetails(MemberId);
CREATE INDEX idx_agent_code ON AgentDetails(AgentCode);
CREATE INDEX idx_lead_id ON LeadDetails(LeadID);
```

```sql
-- Essential for finding hospitals near the customer
CREATE INDEX idx_hospital_pincode ON HospitalMaster(Pincode);

-- Useful if you filter hospitals by City/State for broader region risk
CREATE INDEX idx_hospital_city_state ON HospitalMaster(CityId, StateId);

-- Useful if you need to look up a specific hospital name from a claim
CREATE INDEX idx_hospital_name ON HospitalMaster(HospitalName);
```

### 3. `PortabilityDetails`
*   **Usage:** You will join this table with `ProposalDetails` using `ProposalNum`.
*   **Required Indexes:**

```sql
-- Essential for joining with the main Proposal table
CREATE INDEX idx_portability_proposal ON PortabilityDetails(ProposalNum);
```

### Summary SQL Script
Run this block to ensure all performance optimizations are in place for the new tables:

```sql
/* 1. Indexes for HospitalMaster */
CREATE INDEX idx_hospital_pincode ON HospitalMaster(Pincode);
CREATE INDEX idx_hospital_city_state ON HospitalMaster(CityId, StateId);
CREATE INDEX idx_hospital_name ON HospitalMaster(HospitalName);

/* 2. Indexes for PortabilityDetails */
CREATE INDEX idx_portability_proposal ON PortabilityDetails(ProposalNum);
```


Your current API Request schema is **missing four critical dimensions** that are essential for a high-quality AI Risk Assessment in the insurance domain.

If you only look at the customer's self-declared health and finance, you miss the **context** of the sale (Agent), the **location** risks (Geo), and the **verification** status (KYC).

### 1. Missing Data Points in Your API
You should add these sections to your `POST` request to make the risk assessment robust:

1.  **Agent/Channel Risk:** (Crucial for Fraud)
    *   *Why:* If an agent has a history of bad business (High Loss Ratio), any customer coming from them is higher risk, regardless of how healthy they look.
2.  **Geographic Data:**
    *   *Why:* A healthy person living in a high-pollution zone or a zip code with high hospital fraud rates is a higher risk.
3.  **Product Context:**
    *   *Why:* Risk is relative. A ₹5L Sum Insured is low risk; ₹1Cr Sum Insured is high risk. You need to know what they are buying.
4.  **KYC & Verification:**
    *   *Why:* Did their face match the ID? Is the PAN card valid? If KYC is weak, the risk of impersonation fraud is high.

---

### 2. Improved API Request Schema for /api/risk-assessment
Update your Pydantic model (FastAPI) to this structure. I have added the **`new_`** sections.

```json
{
  "customer_id": "string",
  "proposal_id": "string",  // NEW: To link back to specific proposal
  
  "policy_info": {          // NEW: Context of what is being bought
    "product_name": "string",
    "sum_insured": 0,
    "policy_term": 0,
    "is_portability": boolean
  },

  "personal_info": {
    "first_name": "string",
    "last_name": "string",
    "date_of_birth": "string",
    "age": 0,
    "gender": "string",
    "email": "string",
    "phone": "string",
    "pincode": "string",    // NEW: Critical for Geo-Risk
    "city": "string",       // NEW
    "zone": "string"        // NEW
  },

  "agent_info": {           // NEW: Source of business risk
    "agent_code": "string",
    "agent_category": "string",
    "agent_loss_ratio": 0,  // % of claims vs premium for this agent
    "agent_vintage_years": 0
  },

  "kyc_verification": {     // NEW: Identity Fraud Risk
    "pan_number": "string",
    "kyc_status": "string",
    "aml_check": "string",  // Anti-Money Laundering status
    "face_match_score": 0
  },

  "health_info": {
    "bmi": 0,
    "smoker": true,
    "alcohol_consumption": "string",
    "health_conditions": ["string"], // e.g. ["Diabetes", "Hypertension"]
    "medications": ["string"],
    "surgeries": ["string"]
  },

  "financial_info": {
    "annual_income": 0,
    "credit_score": 0,
    "occupation": "string",
    "sum_insured_to_income_ratio": 0 // Calculated field
  },

  "claims_history": {
    "total_claims_count": 0,
    "total_claims_amount": 0,
    "is_blacklisted_hospital_involved": boolean // NEW: Immediate Fraud Flag
  }
}
```
Here is the concise summary of the implementation steps:

1.  **Create Core Tables:** Run the PostgreSQL `CREATE TABLE` scripts for **Proposal**, **Member**, **Medical**, **Financial**, **Claims**, **Agent**, and **Region** data.
2.  **Create Missing Tables:** Run scripts for the 3 additional tables: **`HospitalMaster`** (Geo risk), **`AgentRiskScores`** (Channel risk), and **`PortabilityDetails`** (Churn risk).
3.  **Add Indexes:** Execute the `CREATE INDEX` scripts for all tables (especially on `ProposalNum`, `Pincode`, and `AgentCode`) to ensure API speed.
4.  **Update API Schema:** Modify your FastAPI request model to include the missing dimensions: **Agent Info**, **Policy Context**, **KYC Status**, and **Pincode**.
5.  **Implement Data Extraction:** Use the provided SQL queries to generate the **7 specific JSON datasets** (Demographic, Financial, PED, Region, Claims, Agent, Product) from these tables.
6.  **Final Logic:** Pass these 7 JSONs to your LLM to get individual scores, then calculate the weighted average for the **Overall Risk Score**.