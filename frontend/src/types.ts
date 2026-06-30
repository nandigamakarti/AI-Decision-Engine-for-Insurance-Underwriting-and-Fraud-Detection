// Data schemas matching FastAPI / SQLAlchemy backend models

export interface MemberSummary {
  age?: number;
  gender?: string;
  height?: string;
  weight?: string;
  nature_of_work?: string;
  marital_status?: string;
  smoking_status?: string;
  alcohol_consumption?: string;
  exercise_frequency?: string;
}

export interface ProposalSummary {
  proposal_num: string;
  policy_number?: string;
  agent_code?: string;
  product_id?: number;
  sum_insured?: number;
  annual_income?: number;
  
  // Data availability checklist
  has_member_data: boolean;
  member_age?: number;
  member_gender?: string;
  
  has_kyc_data: boolean;
  kyc_status?: string;
  
  has_claims_data: boolean;
  claims_count: number;
  
  has_agent_data: boolean;
  agent_category?: string;
  
  has_product_data: boolean;
  product_name?: string;
  
  has_lead_data: boolean;
  lead_city?: string;
  lead_state?: string;
  
  has_chronic_disease_data: boolean;
}

export interface RiskFactor {
  factor_name: string;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  score: number;
  description: string;
}

export interface RiskCalculationResult {
  dimension: string;
  risk_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  risk_factors: string[] | RiskFactor[];
  weight_in_overall: number;
  recommendations: string[];
}

export interface CombinedRiskResult {
  proposal_id: string;
  overall_score: number;
  overall_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  decision: 'ACCEPT' | 'REVIEW' | 'DECLINE';
  premium_loading_percentage: number;
  dimension_results: {
    [key: string]: RiskCalculationResult;
  };
  recommendations?: string[];
  top_risk_factors?: string[];
}

export interface SystemHealth {
  api: {
    status: 'healthy' | 'unhealthy' | 'loading';
    service: string;
    version?: string;
  };
  db: {
    status: 'healthy' | 'unhealthy' | 'loading';
    service: string;
    tables_count?: number;
    tables?: string[];
    message?: string;
  };
  ollama: {
    status: 'healthy' | 'unhealthy' | 'loading';
    service: string;
    model?: string;
    base_url?: string;
    temperature?: number;
  };
}

export interface ClaimRecord {
  claim_number: string;
  claimed_amount: number;
  approved_amount: number;
  claim_status: string;
  rejection_reason?: string;
  hospital_name?: string;
  reported_date_time?: string;
  claim_type?: string;
}

export interface AgentRiskSummary {
  agent_code: string;
  agent_category: string;
  channel: string;
  loss_ratio: string;
  persistency_ratio?: string;
  lapse_rate?: string;
  vintage_years?: number;
  compliance_flags?: string[];
}

export interface ProductRiskSummary {
  product_id: number;
  product_name: string;
  pre_existing_waiting_period: number; // in months
  co_pay_percentage: number;
  key_features?: string;
  max_coverage_limit?: number;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  level: 'INFO' | 'WARNING' | 'ERROR';
  category: 'API' | 'DB' | 'OLLAMA' | 'UNDERWRITER';
  message: string;
}

export interface ExportReport {
  id: string;
  filename: string;
  format: 'PDF' | 'JSON' | 'CSV';
  date: string;
  status: 'COMPLETED' | 'PENDING';
}

