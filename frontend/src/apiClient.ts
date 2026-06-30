import { ProposalSummary, CombinedRiskResult, SystemHealth } from './types';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

let useMockFallback = false;

export const setMockMode = (mode: boolean) => {
  useMockFallback = mode;
  console.log(`API client fallback mode set to: ${mode ? 'MOCK' : 'API'}`);
};

export const getMockMode = () => useMockFallback;

export async function fetchProposals(): Promise<ProposalSummary[]> {
  try {
    const res = await fetch(`${BASE_URL}/api/proposals`);
    if (!res.ok) throw new Error('API server returned error code');
    const data = await res.json();
    return data;
  } catch (err) {
    console.error('API connection failed.', err);
    throw err;
  }
}

export async function fetchProposalDetails(proposalId: string): Promise<any> {
  try {
    const res = await fetch(`${BASE_URL}/api/proposals/${proposalId}`);
    if (!res.ok) throw new Error('API server returned error code');
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(`API connection to fetch details for ${proposalId} failed.`, err);
    throw err;
  }
}

export async function fetchCombinedRisk(
  proposalId: string, 
  mode: 'ruleBased' | 'aiPowered'
): Promise<CombinedRiskResult> {
  const endpoint = mode === 'ruleBased' 
    ? `${BASE_URL}/api/risk/combined`
    : `${BASE_URL}/api/ai-risk/combined`;

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ proposal_id: proposalId })
    });
    if (!res.ok) throw new Error('API server returned error code');
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(`API connection to ${endpoint} failed.`, err);
    throw err;
  }
}

export async function fetchSystemHealth(): Promise<SystemHealth> {
  const result: SystemHealth = {
    api: { status: 'loading', service: 'FastAPI Server' },
    db: { status: 'loading', service: 'PostgreSQL Database' },
    ollama: { status: 'loading', service: 'Ollama AI service' }
  };

  try {
    // Check main API health
    const apiPromise = fetch(`${BASE_URL}/api/health`)
      .then(async r => {
        if (!r.ok) throw new Error();
        const d = await r.json();
        result.api = { status: 'healthy', service: 'FastAPI Server', version: d.version || '0.2.0' };
      })
      .catch(() => {
        result.api.status = 'unhealthy';
      });

    // Check DB Status
    const dbPromise = fetch(`${BASE_URL}/api/database-status`)
      .then(async r => {
        if (!r.ok) throw new Error();
        const d = await r.json();
        result.db = { 
          status: 'healthy', 
          service: 'PostgreSQL Database', 
          tables_count: d.tables_count,
          tables: d.tables,
          message: d.message 
        };
      })
      .catch(() => {
        result.db.status = 'unhealthy';
      });

    // Check Ollama Status
    const ollamaPromise = fetch(`${BASE_URL}/api/ollama-status`)
      .then(async r => {
        if (!r.ok) throw new Error();
        const d = await r.json();
        result.ollama = { 
          status: 'healthy', 
          service: 'Ollama AI service',
          model: d.model,
          base_url: d.base_url,
          temperature: d.temperature 
        };
      })
      .catch(() => {
        result.ollama.status = 'unhealthy';
      });

    await Promise.all([apiPromise, dbPromise, ollamaPromise]);
    return result;
  } catch (err) {
    console.error('System health fetching general failure', err);
    result.api.status = 'unhealthy';
    result.db.status = 'unhealthy';
    result.ollama.status = 'unhealthy';
    return result;
  }
}

export async function assessCustomCustomer(payload: any): Promise<any> {
  try {
    const res = await fetch(`${BASE_URL}/api/risk-assessment`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('API server returned error code');
    const data = await res.json();
    return data;
  } catch (err) {
    console.error('Custom assessment call failed.', err);
    throw err;
  }
}

export async function analyzeImage(claimId: string, imageData: string, imageType: string): Promise<any> {
  try {
    const res = await fetch(`${BASE_URL}/api/image-analysis`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ claim_id: claimId, image_data: imageData, image_type: imageType })
    });
    if (!res.ok) throw new Error('API server returned error code');
    return await res.json();
  } catch (err) {
    console.error('Image analysis call failed.', err);
    throw err;
  }
}

export async function lookupMedicalCode(codeType: string, code: string): Promise<any> {
  try {
    const res = await fetch(`${BASE_URL}/api/medical-codes/${codeType}/${code}`);
    if (!res.ok) throw new Error('API server returned error code');
    return await res.json();
  } catch (err) {
    console.error(`Medical code lookup failed for ${codeType}/${code}.`, err);
    throw err;
  }
}

export async function analyzeMedicalCodes(payload: {
  icd10_codes: string[];
  cpt_codes: string[];
  ndc_codes: string[];
  hcpcs_codes: string[];
}): Promise<any> {
  try {
    const res = await fetch(`${BASE_URL}/api/medical-codes/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('API server returned error code');
    return await res.json();
  } catch (err) {
    console.error('Medical codes analysis failed.', err);
    throw err;
  }
}
