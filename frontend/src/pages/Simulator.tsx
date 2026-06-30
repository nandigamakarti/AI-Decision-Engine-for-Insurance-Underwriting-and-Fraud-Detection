import React, { useState } from 'react';
import { assessCustomCustomer } from '../apiClient';
import { RiskGauge } from '../components/RiskGauge';
import { Sparkles, Code, User, AlertCircle, RefreshCw, X } from 'lucide-react';
import { useToast } from '../hooks/useToast';

export const Simulator: React.FC = () => {
  const { addToast } = useToast();
  const [activeTab, setActiveTab] = useState<'form' | 'json'>('json');
  const [jsonInput, setJsonInput] = useState(JSON.stringify({
    customer_id: "CUST_SIM_880",
    personal_info: {
      first_name: "Gregory",
      last_name: "Smith",
      age: 52,
      email: "greg.smith@example.com"
    },
    health_info: {
      smoker: true,
      bmi: 29.5,
      health_conditions: ["hypertension", "type_2_diabetes"]
    },
    financial_info: {
      annual_income: 95000,
      credit_score: 640,
      employment_status: "Self-Employed"
    }
  }, null, 2));

  // Form State
  const [formAge, setFormAge] = useState(35);
  const [formGender, setFormGender] = useState('Male');
  const [formIncome, setFormIncome] = useState(60000);
  const [formSmoker, setFormSmoker] = useState(false);
  const [formBP, setFormBP] = useState('120/80');
  const [formPED, setFormPED] = useState('None');

  // Validation State
  const [validationErrors, setValidationErrors] = useState<{ age?: string; income?: string; bp?: string }>({});

  // Result States
  const [evaluating, setEvaluating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRunJSON = async () => {
    setEvaluating(true);
    setError(null);
    setResult(null);
    try {
      const parsed = JSON.parse(jsonInput);
      
      // Basic validation of keys
      if (!parsed.customer_id) {
        throw new Error("JSON payload must contain a 'customer_id' field.");
      }
      if (!parsed.personal_info || typeof parsed.personal_info.age !== 'number') {
        throw new Error("JSON payload must contain 'personal_info' with a numeric 'age'.");
      }
      
      const data = await assessCustomCustomer(parsed);
      setResult(data);
      addToast('success', 'Custom customer JSON evaluated successfully by AI underwriter.', 'Evaluation Complete');
    } catch (err: any) {
      console.error(err);
      const errMsg = err.message || 'Invalid JSON syntax. Please verify commas and quotes.';
      setError(errMsg);
      addToast('error', errMsg, 'JSON Validation Failed');
    } finally {
      setEvaluating(false);
    }
  };

  const handleRunForm = async () => {
    // Form Validation Checks
    const errors: { age?: string; income?: string; bp?: string } = {};
    if (!formAge || formAge < 18 || formAge > 120) {
      errors.age = 'Age must be between 18 and 120.';
    }
    if (!formIncome || formIncome <= 0) {
      errors.income = 'Annual income must be greater than 0.';
    }
    const bpPattern = /^\d{2,3}\/\d{2,3}$/;
    if (!formBP || !bpPattern.test(formBP.trim())) {
      errors.bp = 'BP must be in SYS/DIA format (e.g. 120/80).';
    }

    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      addToast('error', 'Please resolve the form validation errors before submitting.', 'Validation Failed');
      return;
    }

    setValidationErrors({});
    setEvaluating(true);
    setError(null);
    setResult(null);
    
    // Compile JSON payload from Form fields
    const payload = {
      customer_id: `CUST_FORM_${Math.floor(Math.random()*900)+100}`,
      personal_info: {
        first_name: "Applicant",
        last_name: "Form-Entry",
        age: Number(formAge),
        gender: formGender
      },
      health_info: {
        smoker: formSmoker,
        bmi: 24.5, // Standard BMI
        health_conditions: formPED === 'None' ? [] : [formPED]
      },
      financial_info: {
        annual_income: Number(formIncome),
        credit_score: 720,
        employment_status: "Employed"
      }
    };

    try {
      const data = await assessCustomCustomer(payload);
      setResult(data);
      addToast('success', 'Form parameters successfully compiled and run through rules engine.', 'Simulation Complete');
    } catch (err: any) {
      console.error(err);
      const errMsg = err.message || 'Underwriting model failed to execute.';
      setError(errMsg);
      addToast('error', errMsg, 'Evaluation Error');
    } finally {
      setEvaluating(false);
    }
  };

  const loadPreset = (type: 'low' | 'high') => {
    if (type === 'low') {
      setJsonInput(JSON.stringify({
        customer_id: "CUST_LOW_901",
        personal_info: {
          first_name: "Sarah",
          last_name: "Miller",
          age: 28,
          email: "sarah.m@example.com"
        },
        health_info: {
          smoker: false,
          bmi: 21.8,
          health_conditions: []
        },
        financial_info: {
          annual_income: 110000,
          credit_score: 780,
          employment_status: "Employed"
        }
      }, null, 2));
    } else {
      setJsonInput(JSON.stringify({
        customer_id: "CUST_HIGH_404",
        personal_info: {
          first_name: "Arthur",
          last_name: "Pendleton",
          age: 67,
          email: "arthur.p@example.com"
        },
        health_info: {
          smoker: true,
          bmi: 34.2,
          health_conditions: ["coronary_heart_disease", "chronic_kidney_disease"]
        },
        financial_info: {
          annual_income: 48000,
          credit_score: 520,
          employment_status: "Retired"
        }
      }, null, 2));
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px 0' }}>
      
      {/* Selector and run actions */}
      <div style={{ display: 'grid', gridTemplateColumns: '3fr 2fr', gap: '20px', alignItems: 'start' }}>
        
        {/* Left Interactive Input Panel */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          {/* Tabs header */}
          <div style={{ display: 'flex', borderBottom: '1px solid var(--border-color)', marginBottom: '24px', gap: '16px' }}>
            <button
              onClick={() => setActiveTab('json')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '12px 8px',
                borderBottom: activeTab === 'json' ? '2px solid var(--color-primary)' : '2px solid transparent',
                color: activeTab === 'json' ? 'var(--text-primary)' : 'var(--text-secondary)',
                background: 'transparent',
                fontWeight: 600
              }}
            >
              <Code size={16} />
              JSON Schema Editor
            </button>
            
            <button
              onClick={() => setActiveTab('form')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '12px 8px',
                borderBottom: activeTab === 'form' ? '2px solid var(--color-primary)' : '2px solid transparent',
                color: activeTab === 'form' ? 'var(--text-primary)' : 'var(--text-secondary)',
                background: 'transparent',
                fontWeight: 600
              }}
            >
              <User size={16} />
              Quick Form Entry
            </button>
          </div>

          {/* Render Active Tab */}
          {activeTab === 'json' ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
                <button onClick={() => loadPreset('low')} style={{ fontSize: '0.75rem', background: 'rgba(255,255,255,0.05)', color: 'var(--text-secondary)', padding: '4px 10px', borderRadius: '4px' }}>
                  Load Healthy Profile
                </button>
                <button onClick={() => loadPreset('high')} style={{ fontSize: '0.75rem', background: 'rgba(255,255,255,0.05)', color: 'var(--text-secondary)', padding: '4px 10px', borderRadius: '4px' }}>
                  Load Critical Profile
                </button>
              </div>

              <textarea
                id="simulator-json-input"
                aria-label="JSON Schema Input"
                value={jsonInput}
                onChange={(e) => setJsonInput(e.target.value)}
                style={{
                  width: '100%',
                  height: '280px',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.85rem',
                  lineHeight: 1.4,
                  background: 'rgba(0, 0, 0, 0.3)',
                  border: '1px solid var(--border-color)',
                  color: '#818cf8',
                  borderRadius: '10px',
                  padding: '16px'
                }}
              />

              <button
                onClick={handleRunJSON}
                disabled={evaluating}
                style={{
                  background: 'var(--color-primary)',
                  color: 'white',
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  fontSize: '0.95rem'
                }}
              >
                {evaluating ? (
                  <>
                    <RefreshCw className="skeleton" size={16} style={{ animation: 'spin 1.5s linear infinite' }} />
                    Evaluating customer parameters...
                  </>
                ) : (
                  <>
                    <Sparkles size={16} />
                    Submit to AI Underwriter
                  </>
                )}
              </button>
            </div>
          ) : (
            // Form Entry Tab
            <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div>
                  <label htmlFor="sim-age-input">Applicant Age</label>
                  <input 
                    id="sim-age-input"
                    type="number" 
                    value={formAge} 
                    onChange={(e) => setFormAge(Number(e.target.value))} 
                    style={{ 
                      width: '100%',
                      borderColor: validationErrors.age ? 'var(--color-critical)' : 'var(--border-color)',
                      boxShadow: validationErrors.age ? '0 0 8px rgba(239, 68, 68, 0.25)' : 'none'
                    }} 
                  />
                  {validationErrors.age && (
                    <span style={{ color: 'var(--color-critical)', fontSize: '0.72rem', marginTop: '4px', display: 'block' }}>
                      {validationErrors.age}
                    </span>
                  )}
                </div>
                <div>
                  <label htmlFor="sim-gender-select">Gender</label>
                  <select id="sim-gender-select" value={formGender} onChange={(e) => setFormGender(e.target.value)} style={{ width: '100%' }}>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div>
                  <label htmlFor="sim-income-input">Annual Income ($)</label>
                  <input 
                    id="sim-income-input"
                    type="number" 
                    value={formIncome} 
                    onChange={(e) => setFormIncome(Number(e.target.value))} 
                    style={{ 
                      width: '100%',
                      borderColor: validationErrors.income ? 'var(--color-critical)' : 'var(--border-color)',
                      boxShadow: validationErrors.income ? '0 0 8px rgba(239, 68, 68, 0.25)' : 'none'
                    }} 
                  />
                  {validationErrors.income && (
                    <span style={{ color: 'var(--color-critical)', fontSize: '0.72rem', marginTop: '4px', display: 'block' }}>
                      {validationErrors.income}
                    </span>
                  )}
                </div>
                <div>
                  <label htmlFor="sim-smoker-select">Lifestyle: Smoking status</label>
                  <select id="sim-smoker-select" value={formSmoker ? 'yes' : 'no'} onChange={(e) => setFormSmoker(e.target.value === 'yes')} style={{ width: '100%' }}>
                    <option value="no">Never Smoked</option>
                    <option value="yes">Current Smoker</option>
                  </select>
                </div>
                <div>
                  <label htmlFor="sim-bp-input">Blood Pressure</label>
                  <input 
                    id="sim-bp-input"
                    type="text" 
                    value={formBP} 
                    onChange={(e) => setFormBP(e.target.value)} 
                    style={{ 
                      width: '100%',
                      borderColor: validationErrors.bp ? 'var(--color-critical)' : 'var(--border-color)',
                      boxShadow: validationErrors.bp ? '0 0 8px rgba(239, 68, 68, 0.25)' : 'none'
                    }} 
                  />
                  {validationErrors.bp && (
                    <span style={{ color: 'var(--color-critical)', fontSize: '0.72rem', marginTop: '4px', display: 'block' }}>
                      {validationErrors.bp}
                    </span>
                  )}
                </div>
                <div>
                  <label htmlFor="sim-ped-select">Pre-Existing Diseases (PED)</label>
                  <select id="sim-ped-select" value={formPED} onChange={(e) => setFormPED(e.target.value)} style={{ width: '100%' }}>
                    <option value="None">None Reported</option>
                    <option value="hypertension">Hypertension</option>
                    <option value="type_2_diabetes">Type 2 Diabetes</option>
                    <option value="asthma">Chronic Asthma</option>
                  </select>
                </div>
              </div>

              <button
                onClick={handleRunForm}
                disabled={evaluating}
                style={{
                  background: 'var(--color-primary)',
                  color: 'white',
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  fontSize: '0.95rem',
                  marginTop: '12px'
                }}
              >
                {evaluating ? (
                  <>
                    <RefreshCw className="skeleton" size={16} style={{ animation: 'spin 1.5s linear infinite' }} />
                    Calculating risk boundaries...
                  </>
                ) : (
                  <>
                    <Sparkles size={16} />
                    Run Assessment Checks
                  </>
                )}
              </button>
            </div>
          )}

          {error && (
            <div className="glass-panel" style={{ background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.2)', padding: '12px 16px', borderRadius: '8px', marginTop: '16px', display: 'flex', gap: '10px', alignItems: 'center', color: 'var(--color-critical)' }}>
              <AlertCircle size={18} />
              <span style={{ fontSize: '0.88rem', fontWeight: 500 }}>{error}</span>
            </div>
          )}
        </div>

        {/* Right Output Dashboard Preview */}
        <div style={{ minHeight: '350px' }}>
          {result ? (
            <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px', position: 'relative' }}>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  AI Assessment Result
                </h3>
                <button onClick={() => setResult(null)} style={{ background: 'transparent', color: 'var(--text-muted)' }}>
                  <X size={16} />
                </button>
              </div>

              {/* Score gauge render */}
              <RiskGauge 
                score={result.overall_risk_score} 
                level={result.overall_risk_level} 
                title="Overall Risk Rating"
                size={160}
              />

              {/* Factors */}
              <div>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '8px' }}>
                  Risk Factors Rationale:
                </h4>
                <ul style={{ paddingLeft: '16px', fontSize: '0.88rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {result.risk_factors.map((item: any, idx: number) => (
                    <li key={idx}>
                      <strong style={{ color: 'var(--text-primary)' }}>{item.factor_name}</strong>: {item.description}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Recommendations */}
              <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '12px' }}>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '8px' }}>
                  Underwriting Recommendations:
                </h4>
                <ul style={{ paddingLeft: '16px', fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '4px', listStyleType: 'circle' }}>
                  {result.recommendations.map((item: string, idx: number) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>

            </div>
          ) : (
            // Placeholder empty state
            <div className="glass-panel" style={{ height: '100%', minHeight: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '40px', textAlign: 'center', borderStyle: 'dashed' }}>
              <Sparkles size={36} style={{ color: 'var(--color-primary)', opacity: 0.3, marginBottom: '16px' }} />
              <h4 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Awaiting Parameters Entry</h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', maxWidth: '250px', marginTop: '8px' }}>
                Configure form inputs or enter a JSON payload, then execute the AI Underwriter validation.
              </p>
            </div>
          )}
        </div>

      </div>
      
    </div>
  );
};
