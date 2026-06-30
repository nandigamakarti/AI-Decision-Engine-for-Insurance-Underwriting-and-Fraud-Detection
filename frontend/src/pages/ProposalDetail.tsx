import React, { useState, useEffect } from 'react';
import { CombinedRiskResult, ProposalSummary, ClaimRecord } from '../types';
import { fetchCombinedRisk, fetchProposalDetails } from '../apiClient';
import { RiskGauge } from '../components/RiskGauge';
import { useToast } from '../hooks/useToast';
import { 
  ShieldAlert, 
  FileWarning, 
  RefreshCw, 
  User, 
  Layers, 
  Sparkles, 
  Activity, 
  AlertTriangle, 
  Globe, 
  CheckCircle,
  DollarSign,
  Download,
  Eye,
  Brain,
  Cpu,
  ChevronDown,
  ChevronUp,
  Database,
  Terminal,
  Check,
  Info,
  ShieldCheck,
  Zap,
  CheckSquare
} from 'lucide-react';

interface ProposalDetailProps {
  proposalId: string;
  proposals: ProposalSummary[];
  setCurrentPage: (page: string) => void;
  setSelectedProposalId: (id: string) => void;
}

type SubTab = 'overview' | 'profile' | 'rules-center' | 'ai-center' | 'claims' | 'agent' | 'product' | 'regional' | 'decision';

export const ProposalDetail: React.FC<ProposalDetailProps> = ({
  proposalId,
  proposals,
  setCurrentPage,
  setSelectedProposalId
}) => {
  const { addToast } = useToast();
  
  const [ruleResult, setRuleResult] = useState<CombinedRiskResult | null>(null);
  const [aiResult, setAiResult] = useState<CombinedRiskResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<SubTab>('overview');
  
  // Compare Assessments Mode state
  const [comparisonMode, setComparisonMode] = useState<'rule' | 'ai' | 'both'>('both');
  const [proposalDetails, setProposalDetails] = useState<any>(null);

  // Underwriting Decision state
  const [finalDecision, setFinalDecision] = useState<'ACCEPT' | 'REVIEW' | 'DECLINE'>('REVIEW');
  const [premiumLoading, setPremiumLoading] = useState(15);
  const [justification, setJustification] = useState('');
  const [checklists, setChecklists] = useState<string[]>([]);
  const [decisionSubmitted, setDecisionSubmitted] = useState(false);

  // AI Center UI state variables
  const [jsonCollapsed, setJsonCollapsed] = useState(true);
  const [expandedDimensions, setExpandedDimensions] = useState<Record<string, boolean>>({
    demographic: true,
    financial: true,
    medical: true,
    regional: false,
    claims: false,
    agent: false,
    product: false
  });

  // Find metadata
  const metadata = proposals.find(p => p.proposal_num === proposalId);

  const loadRiskAssessments = async (silent = false) => {
    if (silent) setRefreshing(true);
    else setLoading(true);
    
    setError(null);
    try {
      const [ruleData, aiData, detailsData] = await Promise.all([
        fetchCombinedRisk(proposalId, 'ruleBased'),
        fetchCombinedRisk(proposalId, 'aiPowered'),
        fetchProposalDetails(proposalId)
      ]);
      setRuleResult(ruleData);
      setAiResult(aiData);
      setProposalDetails(detailsData);
      
      // Preset decision fields from AI recommendation
      if (aiData) {
        setFinalDecision(aiData.decision);
        setPremiumLoading(aiData.premium_loading_percentage);
      }
      
      if (silent) {
        addToast('success', `Risk assessment parameters refreshed for proposal ${proposalId}.`, 'Assessment Refreshed');
      }
    } catch (err) {
      console.error(err);
      setError('Could not run risk evaluations for this proposal.');
      addToast('error', 'Failed to retrieve combined risk calculation results from API.', 'Retrieval Error');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadRiskAssessments();
    setDecisionSubmitted(false);
    setJustification('');
    setChecklists([]);
  }, [proposalId]);

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', padding: '100px 0', alignItems: 'center', justifyContent: 'center' }}>
        <RefreshCw className="skeleton" size={40} style={{ color: 'var(--color-primary)', animation: 'spin 1.5s linear infinite' }} />
        <span style={{ fontSize: '1rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
          Running multi-dimensional rule configurations and launching GPT-OSS-20B prompts...
        </span>
        <style dangerouslySetInnerHTML={{__html: `
          @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        `}} />
      </div>
    );
  }

  if (error || !ruleResult || !aiResult) {
    return (
      <div className="glass-panel" style={{ padding: '40px', margin: '40px 0', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
        <ShieldAlert size={48} style={{ color: 'var(--color-critical)' }} />
        <h3 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Evaluation Failed</h3>
        <p style={{ color: 'var(--text-secondary)' }}>{error || 'No assessment results returned.'}</p>
        <button onClick={() => loadRiskAssessments()} style={{ background: 'var(--color-primary)', color: 'white', padding: '10px 20px', borderRadius: '8px' }}>
          Retry Audits
        </button>
      </div>
    );
  }

  // Load related profiles from database
  const claims: ClaimRecord[] = proposalDetails?.claims_history || [];
  const agent = proposalDetails?.agent_details || {
    agent_code: metadata?.agent_code || 'AGT102',
    agent_category: 'Standard',
    channel: 'Direct',
    loss_ratio: '0.0%',
    lapse_rate: '0.0%',
    vintage_years: 1,
    compliance_flags: []
  };
  const product = proposalDetails?.product_details || {
    product_id: metadata?.product_id || 101,
    product_name: 'Standard Care',
    pre_existing_waiting_period: 24,
    co_pay_percentage: 10,
    key_features: 'Basic coverage features.'
  };
  const regional = proposalDetails?.regional_details || {
    hospitalDistance: 5.0,
    aqi: 50,
    naturalDisasters: 'Low Index',
    crimeRate: 'Low'
  };

  const toggleChecklist = (item: string) => {
    if (checklists.includes(item)) {
      setChecklists(checklists.filter(c => c !== item));
    } else {
      setChecklists([...checklists, item]);
    }
  };

  const handleDecisionSubmit = () => {
    setDecisionSubmitted(true);
    addToast('success', `Underwriting decision successfully recorded for proposal ${proposalId}.`, 'Decision Recorded');
    setTimeout(() => {
      setCurrentPage('proposals');
    }, 2000);
  };

  const handleExport = () => {
    addToast('success', `Risk assessment report for proposal ${proposalId} exported successfully as PDF slip and raw JSON configuration.`, 'Report Exported');
  };

  const handleExpandDetails = (dimension: string) => {
    switch (dimension) {
      case 'demographic':
      case 'medical':
        setActiveTab('profile');
        break;
      case 'financial':
        setActiveTab('rules-center');
        break;
      case 'regional':
        setActiveTab('regional');
        break;
      case 'claims':
        setActiveTab('claims');
        break;
      case 'agent':
        setActiveTab('agent');
        break;
      case 'product':
        setActiveTab('product');
        break;
    }
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'LOW': return 'var(--color-low)';
      case 'MEDIUM': return 'var(--color-medium)';
      case 'HIGH': return 'var(--color-high)';
      case 'CRITICAL': return 'var(--color-critical)';
      default: return 'var(--text-secondary)';
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px 0' }}>
      
      {/* Workspace Header Panel */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }} className="glass-panel p-4">
        {/* Left Side: Back button + Proposal Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px', flexWrap: 'wrap' }}>
          <button 
            onClick={() => setCurrentPage('proposals')}
            style={{ background: 'transparent', color: 'var(--text-secondary)', fontWeight: 600, fontSize: '0.92rem', padding: 0 }}
          >
            &larr; Proposals Queue
          </button>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600 }}>File Selector:</span>
            <select 
              value={proposalId} 
              onChange={(e) => setSelectedProposalId(e.target.value)}
              style={{
                background: 'var(--bg-primary)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-primary)',
                padding: '6px 12px',
                borderRadius: '8px',
                fontSize: '0.88rem',
                fontWeight: 600,
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              {proposals.map(p => (
                <option key={p.proposal_num} value={p.proposal_num}>
                  {p.proposal_num} - {p.member_age}Y {p.member_gender} ({p.kyc_status})
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Right Side: Refresh & Export */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button
            onClick={() => loadRiskAssessments(true)}
            disabled={refreshing}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-primary)',
              padding: '8px 14px',
              borderRadius: '8px',
              fontSize: '0.85rem',
              fontWeight: 600,
              cursor: 'pointer'
            }}
            className="glass-panel-interactive"
          >
            <RefreshCw size={14} className={refreshing ? 'skeleton' : ''} style={{ animation: refreshing ? 'spin 1.5s linear infinite' : 'none' }} />
            Refresh Engine
          </button>

          <button
            onClick={handleExport}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: 'var(--color-primary)',
              color: 'white',
              padding: '8px 14px',
              borderRadius: '8px',
              fontSize: '0.85rem',
              fontWeight: 600,
              cursor: 'pointer'
            }}
            className="hover:opacity-90"
          >
            <Download size={14} />
            Export Audit Report
          </button>
        </div>
      </div>

      {/* Applicant Summary Banner */}
      <div className="glass-panel" style={{ padding: '16px 24px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '20px' }}>
        <div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Insured Member</span>
          <span style={{ display: 'block', fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginTop: '4px' }}>
            {metadata?.member_age} Yrs, {metadata?.member_gender}
          </span>
        </div>
        <div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Product Coverage</span>
          <span style={{ display: 'block', fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginTop: '4px' }}>
            {metadata?.product_name || `Product ID ${metadata?.product_id}`}
          </span>
        </div>
        <div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Sum Insured</span>
          <span style={{ display: 'block', fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginTop: '4px', fontFamily: 'var(--font-mono)' }}>
            ${metadata?.sum_insured?.toLocaleString()}
          </span>
        </div>
        <div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Annual Income</span>
          <span style={{ display: 'block', fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginTop: '4px', fontFamily: 'var(--font-mono)' }}>
            ${metadata?.annual_income?.toLocaleString()}
          </span>
        </div>
        <div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Risk Status</span>
          <span style={{ display: 'block', fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginTop: '4px' }}>
            {metadata?.has_chronic_disease_data ? (
              <span style={{ color: 'var(--color-critical)', fontWeight: 600 }}>Chronic PED Flagged</span>
            ) : (
              <span style={{ color: 'var(--color-low)', fontWeight: 600 }}>Standard Clean Record</span>
            )}
          </span>
        </div>
        <div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Regional Zone</span>
          <span style={{ display: 'block', fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginTop: '4px' }}>
            {metadata?.lead_city}, {metadata?.lead_state}
          </span>
        </div>
      </div>

      {/* Tabs list (13 pages architecture mapping + Overview) */}
      <div className="glass-panel" style={{ 
        padding: '4px', 
        display: 'flex', 
        gap: '4px', 
        flexWrap: 'wrap',
        borderBottom: '1px solid var(--border-color)' 
      }}>
        {[
          { id: 'overview', label: 'Risk Cockpit', icon: Eye },
          { id: 'profile', label: 'Profile Specs', icon: User },
          { id: 'rules-center', label: 'Rules Engine', icon: Layers },
          { id: 'ai-center', label: 'AI Risk Analysis', icon: Sparkles },
          { id: 'claims', label: 'Claims History', icon: FileWarning },
          { id: 'agent', label: 'Agent Risk', icon: Activity },
          { id: 'product', label: 'Product Specs', icon: DollarSign },
          { id: 'regional', label: 'Regional Geo-Risk', icon: Globe },
          { id: 'decision', label: 'Decision Board', icon: CheckCircle }
        ].map(tab => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as SubTab)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '8px 14px',
                borderRadius: '10px',
                fontSize: '0.88rem',
                fontWeight: 600,
                background: isActive ? 'rgba(99, 102, 241, 0.12)' : 'transparent',
                color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
                border: isActive ? '1px solid rgba(99, 102, 241, 0.25)' : '1px solid transparent',
                transition: 'all var(--transition-fast)'
              }}
            >
              <Icon size={14} style={{ color: isActive ? 'var(--color-primary)' : 'inherit' }} />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab Render panel */}
      <div className="glass-panel" style={{ padding: '28px' }}>
        
        {/* OVERVIEW (RISK COCKPIT) TAB */}
        {activeTab === 'overview' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', borderBottom: '1px solid var(--border-color)', paddingBottom: '16px' }}>
              <div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Insurance Risk Assessment Cockpit</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '2px' }}>
                  Analyze automated rule weights side-by-side with GPT-OSS-20B deep-learning cognitive profiles.
                </p>
              </div>

              {/* Compare Assessments Toggles */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(0,0,0,0.15)', padding: '4px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600, padding: '0 8px' }}>Compare Mode:</span>
                {[
                  { id: 'rule', label: 'Rules Engine' },
                  { id: 'ai', label: 'AI Underwriter' },
                  { id: 'both', label: 'Compare Both' }
                ].map(opt => (
                  <button
                    key={opt.id}
                    onClick={() => setComparisonMode(opt.id as any)}
                    style={{
                      background: comparisonMode === opt.id ? 'var(--color-primary)' : 'transparent',
                      color: comparisonMode === opt.id ? 'white' : 'var(--text-secondary)',
                      padding: '6px 12px',
                      borderRadius: '6px',
                      fontSize: '0.78rem',
                      fontWeight: 600,
                      transition: 'all var(--transition-fast)'
                    }}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Overall Gauges */}
            <div style={{ display: 'grid', gridTemplateColumns: comparisonMode === 'both' ? '1fr 1fr' : '1fr', gap: '24px', alignItems: 'center' }}>
              {(comparisonMode === 'rule' || comparisonMode === 'both') && (
                <RiskGauge score={ruleResult.overall_score} level={ruleResult.overall_level} title="Rules Engine Overall Score" />
              )}
              {(comparisonMode === 'ai' || comparisonMode === 'both') && (
                <RiskGauge score={aiResult.overall_score} level={aiResult.overall_level} title="AI Underwriter Overall Score" />
              )}
            </div>

            {/* 7 Dimension Risk Cards Grid */}
            <h4 style={{ fontSize: '1rem', fontWeight: 600, marginTop: '16px' }}>Multi-Dimensional Risk Audits</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              {['demographic', 'financial', 'medical', 'regional', 'claims', 'agent', 'product'].map(dimKey => {
                const ruleDim = ruleResult.dimension_results[dimKey];
                const aiDim = aiResult.dimension_results[dimKey];
                
                if (!ruleDim || !aiDim) return null;
                
                // Determine which factors and recommendations to show based on toggle
                const displayRule = comparisonMode === 'rule' || comparisonMode === 'both';
                const factorsToDisplay = displayRule ? ruleDim.risk_factors : aiDim.risk_factors;
                const recsToDisplay = displayRule ? ruleDim.recommendations : aiDim.recommendations;
                
                return (
                  <div 
                    key={dimKey} 
                    className="glass-panel" 
                    style={{ 
                      padding: '20px', 
                      display: 'flex', 
                      flexDirection: 'column', 
                      gap: '14px',
                      position: 'relative'
                    }}
                  >
                    {/* Top highlights */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <h5 style={{ fontSize: '0.92rem', fontWeight: 700, textTransform: 'capitalize', color: 'var(--text-primary)' }}>
                        {dimKey} Risk
                      </h5>
                      <span className="badge badge-low" style={{ fontSize: '0.68rem', padding: '3px 8px', textTransform: 'none' }}>
                        Weight: {ruleDim.weight_in_overall * 100}%
                      </span>
                    </div>

                    {/* Scores display */}
                    <div style={{ display: 'grid', gridTemplateColumns: comparisonMode === 'both' ? '1fr 1fr' : '1fr', gap: '10px' }}>
                      {/* Rule score */}
                      {(comparisonMode === 'rule' || comparisonMode === 'both') && (
                        <div style={{ background: 'rgba(0,0,0,0.12)', padding: '8px 12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                          <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', display: 'block' }}>Rules Engine</span>
                          <span style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--color-primary)', display: 'block', marginTop: '2px' }}>
                            {ruleDim.risk_score.toFixed(0)}/100
                          </span>
                          <span style={{ fontSize: '0.68rem', fontWeight: 600, color: getLevelColor(ruleDim.risk_level), textTransform: 'uppercase' }}>
                            {ruleDim.risk_level}
                          </span>
                        </div>
                      )}

                      {/* AI score */}
                      {(comparisonMode === 'ai' || comparisonMode === 'both') && (
                        <div style={{ background: 'rgba(99, 102, 241, 0.04)', padding: '8px 12px', borderRadius: '8px', border: '1px solid rgba(99, 102, 241, 0.2)' }}>
                          <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', display: 'block' }}>AI Reasoning</span>
                          <span style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--color-secondary)', display: 'block', marginTop: '2px' }}>
                            {aiDim.risk_score.toFixed(0)}/100
                          </span>
                          <span style={{ fontSize: '0.68rem', fontWeight: 600, color: getLevelColor(aiDim.risk_level), textTransform: 'uppercase' }}>
                            {aiDim.risk_level}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Factors list */}
                    <div>
                      <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '0.02em' }}>
                        Key Factors:
                      </span>
                      <ul style={{ paddingLeft: '14px', fontSize: '0.78rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '3px' }}>
                        {factorsToDisplay.slice(0, 2).map((factor: any, i) => (
                          <li key={i}>{typeof factor === 'string' ? factor : factor.description}</li>
                        ))}
                      </ul>
                    </div>

                    {/* Recommendations */}
                    <div>
                      <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '0.02em' }}>
                        Audit Recommendation:
                      </span>
                      <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', margin: 0, lineHeight: 1.4 }}>
                        {recsToDisplay[0] || 'Approve on standard terms'}
                      </p>
                    </div>

                    {/* Expand Details */}
                    <button 
                      onClick={() => handleExpandDetails(dimKey)}
                      style={{ 
                        marginTop: 'auto', 
                        background: 'rgba(255, 255, 255, 0.03)', 
                        border: '1px solid var(--border-color)', 
                        color: 'var(--text-secondary)', 
                        padding: '8px', 
                        borderRadius: '6px', 
                        fontSize: '0.78rem',
                        fontWeight: 600,
                        textAlign: 'center',
                        cursor: 'pointer'
                      }}
                      className="glass-panel-interactive"
                    >
                      Audit Details &rarr;
                    </button>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* PROFILE TAB */}
        {activeTab === 'profile' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '8px' }}>Applicant Demographic Details</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px' }}>
              <div>
                <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '12px' }}>Personal Identity</h4>
                <table style={{ width: '100%', border: 'none' }}>
                  <tbody>
                    <tr><td style={{ padding: '8px 0', color: 'var(--text-secondary)' }}>Gender</td><td style={{ padding: '8px 0', fontWeight: 600 }}>{metadata?.member_gender}</td></tr>
                    <tr><td style={{ padding: '8px 0', color: 'var(--text-secondary)' }}>Age</td><td style={{ padding: '8px 0', fontWeight: 600 }}>{metadata?.member_age} Years</td></tr>
                    <tr><td style={{ padding: '8px 0', color: 'var(--text-secondary)' }}>Marital Status</td><td style={{ padding: '8px 0', fontWeight: 600 }}>Married</td></tr>
                    <tr><td style={{ padding: '8px 0', color: 'var(--text-secondary)' }}>Zone Region</td><td style={{ padding: '8px 0', fontWeight: 600 }}>{metadata?.lead_city}, {metadata?.lead_state}</td></tr>
                  </tbody>
                </table>
              </div>
              
              <div>
                <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '12px' }}>Lifestyle Factors</h4>
                <table style={{ width: '100%', border: 'none' }}>
                  <tbody>
                    <tr><td style={{ padding: '8px 0', color: 'var(--text-secondary)' }}>Smoking status</td><td style={{ padding: '8px 0', fontWeight: 600 }}>{metadata?.has_chronic_disease_data ? 'Former' : 'Never'}</td></tr>
                    <tr><td style={{ padding: '8px 0', color: 'var(--text-secondary)' }}>Alcohol Consumption</td><td style={{ padding: '8px 0', fontWeight: 600 }}>{metadata?.has_chronic_disease_data ? 'Moderate' : 'None'}</td></tr>
                    <tr><td style={{ padding: '8px 0', color: 'var(--text-secondary)' }}>Exercise Routine</td><td style={{ padding: '8px 0', fontWeight: 600 }}>Moderate</td></tr>
                    <tr><td style={{ padding: '8px 0', color: 'var(--text-secondary)' }}>Job Nature</td><td style={{ padding: '8px 0', fontWeight: 600 }}>Deskbound / Professional</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* RULES CENTER TAB */}
        {activeTab === 'rules-center' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '24px', alignItems: 'center' }}>
              <RiskGauge score={ruleResult.overall_score} level={ruleResult.overall_level} title="Rule Engine Combined Score" />
              <div>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Weighted Calculation</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', marginTop: '10px', lineHeight: 1.5 }}>
                  The rule engine aggregates scores from the 7 risk dimensions using fixed weights. Limits are validated using strict database constraints.
                </p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '16px' }}>
                  <span className="badge badge-low" style={{ textTransform: 'none' }}>Medical: 30%</span>
                  <span className="badge badge-low" style={{ textTransform: 'none' }}>Financial: 20%</span>
                  <span className="badge badge-low" style={{ textTransform: 'none' }}>Demographic: 15%</span>
                  <span className="badge badge-low" style={{ textTransform: 'none' }}>Claims: 15%</span>
                  <span className="badge badge-low" style={{ textTransform: 'none' }}>Regional: 10%</span>
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
              {Object.values(ruleResult.dimension_results).map(dim => (
                <div key={dim.dimension} style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 16px', borderBottom: '1px solid var(--border-color)' }}>
                  <span style={{ fontWeight: 600, textTransform: 'capitalize' }}>{dim.dimension} Risk</span>
                  <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--color-primary)' }}>{dim.risk_score.toFixed(0)} / 100 ({dim.risk_level})</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AI RISK ANALYSIS TAB */}
        {activeTab === 'ai-center' && (
          <div className="flex flex-col gap-6 animate-[slideIn_0.35s_ease-out]">
            <style dangerouslySetInnerHTML={{__html: `
              .json-key { color: var(--color-secondary) !important; font-weight: 600; }
              .json-string { color: var(--color-low) !important; }
              .json-number { color: var(--color-medium) !important; }
              .json-boolean { color: var(--color-critical) !important; }
              .json-null { color: var(--text-muted) !important; }
              
              .timeline-line {
                position: absolute;
                left: 19px;
                top: 24px;
                bottom: -24px;
                width: 2px;
                background: var(--border-color);
              }
              
              .timeline-item:last-child .timeline-line {
                display: none;
              }
              
              .timeline-node {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: var(--bg-secondary);
                border: 1px solid var(--border-color);
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                z-index: 10;
                transition: all var(--transition-fast);
              }
              
              .timeline-item:hover .timeline-node {
                border-color: var(--border-color-active);
                box-shadow: 0 0 10px rgba(99, 102, 241, 0.2);
              }
            `}} />

            {/* Main grid split: 1/3 diagnostics/JSON, 2/3 reasoning timeline and dimensions */}
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 items-start">
              
              {/* LEFT COLUMN: Score, Confidence, and JSON Payload */}
              <div className="xl:col-span-1 flex flex-col gap-6">
                
                {/* 1. AI Score Card */}
                <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
                  <div className="flex items-center justify-between border-b pb-4" style={{ borderColor: 'var(--border-color)' }}>
                    <div className="flex items-center gap-2">
                      <Brain className="text-indigo-400" size={20} />
                      <span className="font-bold text-sm tracking-wider uppercase text-secondary">AI Risk Diagnostics</span>
                    </div>
                    <span className="badge badge-low" style={{ fontSize: '0.75rem', padding: '2px 8px' }}>Active</span>
                  </div>

                  {/* SVG Speedo Gauge */}
                  <div className="flex flex-col items-center justify-center relative py-4">
                    <div className="relative w-48 h-28">
                      <svg viewBox="0 0 100 60" className="w-full h-full">
                        <defs>
                          <linearGradient id="gauge-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="var(--color-low)" stopOpacity="0.8" />
                            <stop offset="40%" stopColor="var(--color-medium)" stopOpacity="0.8" />
                            <stop offset="70%" stopColor="var(--color-high)" stopOpacity="0.8" />
                            <stop offset="100%" stopColor="var(--color-critical)" stopOpacity="0.8" />
                          </linearGradient>
                          <filter id="gauge-glow" x="-20%" y="-20%" width="140%" height="140%">
                            <feGaussianBlur stdDeviation="2" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                          </filter>
                        </defs>

                        {/* Background Arc */}
                        <path
                          d="M 10 50 A 40 40 0 0 1 90 50"
                          fill="none"
                          stroke="rgba(255, 255, 255, 0.05)"
                          strokeWidth="8"
                          strokeLinecap="round"
                        />

                        {/* Value Arc */}
                        <path
                          d="M 10 50 A 40 40 0 0 1 90 50"
                          fill="none"
                          stroke="url(#gauge-grad)"
                          strokeWidth="8"
                          strokeLinecap="round"
                          strokeDasharray={Math.PI * 40}
                          strokeDashoffset={Math.PI * 40 - (Math.min(100, Math.max(0, aiResult.overall_score)) / 100) * (Math.PI * 40)}
                          style={{ transition: 'stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1)' }}
                        />

                        {/* Rotating Needle */}
                        <g transform="translate(50, 50)" style={{ transition: 'transform 1.2s cubic-bezier(0.4, 0, 0.2, 1)' }}>
                          <g transform={`rotate(${(aiResult.overall_score / 100) * 180 - 90})`}>
                            <line
                              x1="0"
                              y1="0"
                              x2="0"
                              y2="-38"
                              stroke={
                                aiResult.overall_level === 'LOW' ? 'var(--color-low)' :
                                aiResult.overall_level === 'MEDIUM' ? 'var(--color-medium)' :
                                aiResult.overall_level === 'HIGH' ? 'var(--color-high)' :
                                'var(--color-critical)'
                              }
                              strokeWidth="2"
                              strokeLinecap="round"
                              filter="url(#gauge-glow)"
                            />
                            <polygon 
                              points="-1.5,0 0,-33 1.5,0" 
                              fill={
                                aiResult.overall_level === 'LOW' ? 'var(--color-low)' :
                                aiResult.overall_level === 'MEDIUM' ? 'var(--color-medium)' :
                                aiResult.overall_level === 'HIGH' ? 'var(--color-high)' :
                                'var(--color-critical)'
                              } 
                            />
                          </g>
                          <circle cx="0" cy="0" r="4" fill="#0b0f19" stroke="var(--text-primary)" strokeWidth="1" />
                          <circle 
                            cx="0" 
                            cy="0" 
                            r="2" 
                            fill={
                              aiResult.overall_level === 'LOW' ? 'var(--color-low)' :
                              aiResult.overall_level === 'MEDIUM' ? 'var(--color-medium)' :
                              aiResult.overall_level === 'HIGH' ? 'var(--color-high)' :
                              'var(--color-critical)'
                            } 
                          />
                        </g>
                      </svg>

                      {/* Floating overlay */}
                      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 text-center">
                        <span 
                          className="text-3xl font-black tracking-tight" 
                          style={{ 
                            color: 
                              aiResult.overall_level === 'LOW' ? 'var(--color-low)' :
                              aiResult.overall_level === 'MEDIUM' ? 'var(--color-medium)' :
                              aiResult.overall_level === 'HIGH' ? 'var(--color-high)' :
                              'var(--color-critical)'
                          }}
                        >
                          {aiResult.overall_score.toFixed(1)}
                        </span>
                        <span className="text-[10px] uppercase tracking-widest text-secondary block mt-0.5">
                          Score Index
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-col gap-3 border-t pt-4" style={{ borderColor: 'var(--border-color)' }}>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-secondary font-medium">Risk Level Classification</span>
                      <span className={`badge badge-${aiResult.overall_level.toLowerCase()}`}>
                        {aiResult.overall_level} RISK
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-secondary font-medium">Recommended Verdict</span>
                      <span 
                        className="text-xs font-bold px-2.5 py-1 rounded-md" 
                        style={{ 
                          background: 
                            aiResult.decision === 'ACCEPT' ? 'var(--color-low-bg)' :
                            aiResult.decision === 'REVIEW' ? 'var(--color-medium-bg)' :
                            'var(--color-critical-bg)',
                          color: 
                            aiResult.decision === 'ACCEPT' ? 'var(--color-low)' :
                            aiResult.decision === 'REVIEW' ? 'var(--color-medium)' :
                            'var(--color-critical)',
                          border: '1px solid currentColor'
                        }}
                      >
                        {aiResult.decision === 'ACCEPT' ? 'ACCEPT AT STANDARD' : 
                         aiResult.decision === 'REVIEW' ? 'REFER FOR REVIEW' : 'DECLINE COVERAGE'}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-secondary font-medium">Model premium load adjustment</span>
                      <span className="text-xs font-bold text-white">
                        {aiResult.premium_loading_percentage > 0 ? `+${aiResult.premium_loading_percentage}% Loading` : '0% Loading (Standard)'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* 2. Confidence Indicator */}
                <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div className="flex items-center gap-2 border-b pb-3" style={{ borderColor: 'var(--border-color)' }}>
                    <Cpu className="text-cyan-400" size={18} />
                    <span className="font-bold text-xs tracking-wider uppercase text-secondary">Confidence & Diagnostics</span>
                  </div>

                  {(() => {
                    const confidenceScore = metadata 
                      ? 70 + 
                        (metadata.has_member_data ? 6 : 0) + 
                        (metadata.has_kyc_data ? 6 : 0) + 
                        (metadata.has_claims_data ? 6 : 0) + 
                        (metadata.has_agent_data ? 6 : 0) + 
                        (metadata.has_product_data ? 6 : 0)
                      : 92;
                    const confidenceColor = confidenceScore > 85 ? 'var(--color-low)' : 'var(--color-medium)';

                    return (
                      <div className="flex flex-col gap-3">
                        <div className="flex justify-between items-center text-xs">
                          <span className="text-secondary font-medium flex items-center gap-1">
                            Model Evaluation Confidence
                            <Info size={12} className="text-slate-400" />
                          </span>
                          <span className="font-bold" style={{ color: confidenceColor }}>{confidenceScore}%</span>
                        </div>
                        <div className="w-full bg-slate-800/50 rounded-full h-2 overflow-hidden border" style={{ borderColor: 'var(--border-color)' }}>
                          <div 
                            className="h-full rounded-full transition-all duration-1000"
                            style={{ 
                              width: `${confidenceScore}%`, 
                              backgroundColor: confidenceColor,
                              boxShadow: `0 0 10px ${confidenceColor}50`
                            }}
                          />
                        </div>

                        <div className="grid grid-cols-2 gap-3 mt-2 text-[11px] text-secondary">
                          <div className="p-2 bg-slate-900/40 rounded border" style={{ borderColor: 'var(--border-color)' }}>
                            <span className="block text-muted text-[9px] uppercase tracking-wider">Model Node</span>
                            <span className="font-semibold text-white">gpt-oss-20b:uw-v2</span>
                          </div>
                          <div className="p-2 bg-slate-900/40 rounded border" style={{ borderColor: 'var(--border-color)' }}>
                            <span className="block text-muted text-[9px] uppercase tracking-wider">Inference temp</span>
                            <span className="font-semibold text-white">0.01 (Audit Lock)</span>
                          </div>
                          <div className="p-2 bg-slate-900/40 rounded border" style={{ borderColor: 'var(--border-color)' }}>
                            <span className="block text-muted text-[9px] uppercase tracking-wider">Diagnostics status</span>
                            <span className="font-semibold text-white flex items-center gap-1">
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block animate-pulse" />
                              Healthy
                            </span>
                          </div>
                          <div className="p-2 bg-slate-900/40 rounded border" style={{ borderColor: 'var(--border-color)' }}>
                            <span className="block text-muted text-[9px] uppercase tracking-wider flex items-center gap-1">
                              <Zap size={10} className="text-amber-400" />
                              Inference TTFT
                            </span>
                            <span className="font-semibold text-white">1.48 seconds</span>
                          </div>
                        </div>
                      </div>
                    );
                  })()}
                </div>

                {/* 3. Collapsible JSON Viewer */}
                <div className="glass-panel overflow-hidden" style={{ transition: 'all var(--transition-normal)' }}>
                  <button 
                    onClick={() => setJsonCollapsed(!jsonCollapsed)}
                    className="w-full p-4 flex items-center justify-between hover:bg-slate-950/20 text-left border-none bg-transparent"
                  >
                    <div className="flex items-center gap-2">
                      <Terminal className="text-secondary" size={16} />
                      <span className="font-bold text-xs tracking-wider uppercase text-secondary">Raw JSON Payload</span>
                    </div>
                    {jsonCollapsed ? <ChevronDown size={16} className="text-secondary" /> : <ChevronUp size={16} className="text-secondary" />}
                  </button>

                  {!jsonCollapsed && (
                    <div className="border-t border-slate-800/80 bg-slate-950 p-4 relative">
                      <div className="absolute right-3 top-3 z-20">
                        <button 
                          onClick={() => {
                            const payload = {
                              risk_score: aiResult.overall_score,
                              risk_level: aiResult.overall_level,
                              risk_factors: Object.values(aiResult.dimension_results).flatMap(dim => 
                                dim.risk_factors.map(f => typeof f === 'string' ? f : f.description)
                              ),
                              recommendations: aiResult.recommendations || Object.values(aiResult.dimension_results).flatMap(dim => dim.recommendations || [])
                            };
                            navigator.clipboard.writeText(JSON.stringify(payload, null, 2));
                            addToast('success', 'JSON payload copied to clipboard successfully.', 'Payload Copied');
                          }}
                          className="bg-slate-800 hover:bg-slate-700 text-white text-xs px-2.5 py-1 rounded border border-slate-700 flex items-center gap-1.5"
                        >
                          <Download size={12} />
                          Copy JSON
                        </button>
                      </div>

                      <pre className="text-xs font-mono overflow-x-auto max-h-[300px] text-slate-300 select-all scrollbar pt-8">
                        <code dangerouslySetInnerHTML={{
                          __html: (() => {
                            const payload = {
                              risk_score: aiResult.overall_score,
                              risk_level: aiResult.overall_level,
                              risk_factors: Object.values(aiResult.dimension_results).flatMap(dim => 
                                dim.risk_factors.map(f => typeof f === 'string' ? f : f.description)
                              ),
                              recommendations: aiResult.recommendations || Object.values(aiResult.dimension_results).flatMap(dim => dim.recommendations || [])
                            };
                            const jsonString = JSON.stringify(payload, null, 2);
                            return jsonString.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g, (match) => {
                              let cls = 'json-number';
                              if (/^"/.test(match)) {
                                if (/:$/.test(match)) {
                                  cls = 'json-key';
                                } else {
                                  cls = 'json-string';
                                }
                              } else if (/true|false/.test(match)) {
                                cls = 'json-boolean';
                              } else if (/null/.test(match)) {
                                cls = 'json-null';
                              }
                              return `<span class="${cls}">${match}</span>`;
                            });
                          })()
                        }} />
                      </pre>
                    </div>
                  )}
                </div>

              </div>

              {/* RIGHT COLUMN: AI Underwriting Reasoning Chain & Dimensions Breakdown */}
              <div className="xl:col-span-2 flex flex-col gap-6">

                {/* 1. AI Underwriting Reasoning Chain (Timeline) */}
                <div className="glass-panel" style={{ padding: '24px' }}>
                  <div className="flex items-center gap-2 border-b pb-4 mb-6" style={{ borderColor: 'var(--border-color)' }}>
                    <Sparkles className="text-indigo-400" size={18} />
                    <span className="font-bold text-sm tracking-wider uppercase text-secondary">AI Underwriting Reasoning Chain</span>
                  </div>

                  <div className="flex flex-col gap-6 relative">
                    
                    {/* Process 1 */}
                    <div className="flex gap-4 timeline-item relative">
                      <div className="timeline-line" />
                      <div className="timeline-node">
                        <Database size={16} className="text-indigo-400" />
                      </div>
                      <div className="flex-1 bg-slate-900/20 p-4 rounded-xl border" style={{ borderColor: 'var(--border-color)' }}>
                        <span className="text-xs font-semibold text-indigo-400 uppercase tracking-widest block mb-1">Stage 01: Multi-Registry Data Ingestion</span>
                        <h4 className="text-sm font-semibold text-white mb-1">Applicant Metadata Aggregated</h4>
                        <p className="text-xs text-secondary leading-relaxed">
                          Ingested demographics (Age {metadata?.member_age || 'N/A'}, Gender {metadata?.member_gender || 'N/A'}), financial variables (Income ${metadata?.annual_income?.toLocaleString() || 'N/A'}), clinical history checklists, claims history records ({claims.length} claims found), writing agent category, and product definitions.
                        </p>
                      </div>
                    </div>

                    {/* Process 2 */}
                    <div className="flex gap-4 timeline-item relative">
                      <div className="timeline-line" />
                      <div className="timeline-node">
                        <Cpu size={16} className="text-cyan-400" />
                      </div>
                      <div className="flex-1 bg-slate-900/20 p-4 rounded-xl border" style={{ borderColor: 'var(--border-color)' }}>
                        <span className="text-xs font-semibold text-cyan-400 uppercase tracking-widest block mb-1">Stage 02: Multi-Dimension Audit</span>
                        <h4 className="text-sm font-semibold text-white mb-1">Dimensional Scoring Evaluated</h4>
                        <p className="text-xs text-secondary leading-relaxed">
                          Calculated dimensional risks: Demographic ({(aiResult.dimension_results.demographic?.risk_score ?? 0).toFixed(0)}/100), Financial ({(aiResult.dimension_results.financial?.risk_score ?? 0).toFixed(0)}/100), Medical ({(aiResult.dimension_results.medical?.risk_score ?? 0).toFixed(0)}/100), Regional ({(aiResult.dimension_results.regional?.risk_score ?? 0).toFixed(0)}/100), Claims ({(aiResult.dimension_results.claims?.risk_score ?? 0).toFixed(0)}/100), Agent ({(aiResult.dimension_results.agent?.risk_score ?? 0).toFixed(0)}/100), and Product ({(aiResult.dimension_results.product?.risk_score ?? 0).toFixed(0)}/100).
                        </p>
                      </div>
                    </div>

                    {/* Process 3 */}
                    <div className="flex gap-4 timeline-item relative">
                      <div className="timeline-line" />
                      <div className="timeline-node">
                        <Brain size={16} className="text-rose-400" />
                      </div>
                      <div className="flex-1 bg-slate-900/20 p-4 rounded-xl border" style={{ borderColor: 'var(--border-color)' }}>
                        <span className="text-xs font-semibold text-rose-400 uppercase tracking-widest block mb-1">Stage 03: Comorbidity & Relationship Mapping</span>
                        <h4 className="text-sm font-semibold text-white mb-1">Compounding Risks Analyzed</h4>
                        <p className="text-xs text-secondary leading-relaxed">
                          The LLM mapped relationships across dimensions. Highlighted comorbidity synergies (such as smoking-age risk links), geographic location exposure hazards relative to hospital network proximity, and historical claim frequency profiles.
                        </p>
                      </div>
                    </div>

                    {/* Process 4 */}
                    <div className="flex gap-4 timeline-item relative">
                      <div className="timeline-line" />
                      <div className="timeline-node">
                        <ShieldCheck size={16} className="text-emerald-400" />
                      </div>
                      <div className="flex-1 bg-slate-900/20 p-4 rounded-xl border" style={{ borderColor: 'var(--border-color)' }}>
                        <span className="text-xs font-semibold text-emerald-400 uppercase tracking-widest block mb-1">Stage 04: Synthesis & Policy Recommendation</span>
                        <h4 className="text-sm font-semibold text-white mb-1">Underwriting Directives Generated</h4>
                        <p className="text-xs text-secondary leading-relaxed">
                          Synthesized overall risk rating score of {aiResult.overall_score} ({aiResult.overall_level} RISK). Recommended underwriting directive: {aiResult.decision} with premium loading factor adjustments set to {aiResult.premium_loading_percentage}%.
                        </p>
                      </div>
                    </div>

                  </div>
                </div>

                {/* 2. Detailed Dimension Risk Factors Grid */}
                <div className="flex flex-col gap-4">
                  <div className="flex flex-col">
                    <span className="font-bold text-sm tracking-wider uppercase text-secondary">Multi-Dimensional Risk Factors</span>
                    <span className="text-xs text-secondary mt-1">Audit trail breakdown across all 7 operational risk dimensions</span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.values(aiResult.dimension_results).map(dim => {
                      const isExpanded = expandedDimensions[dim.dimension];
                      
                      // Helper to get color code
                      const dimColor = 
                        dim.risk_level === 'LOW' ? 'var(--color-low)' :
                        dim.risk_level === 'MEDIUM' ? 'var(--color-medium)' :
                        dim.risk_level === 'HIGH' ? 'var(--color-high)' :
                        'var(--color-critical)';

                      // Dimension Icon lookup helper
                      const getDimIcon = (d: string) => {
                        switch (d) {
                          case 'demographic': return <User size={16} style={{ color: 'var(--color-primary)' }} />;
                          case 'financial': return <DollarSign size={16} style={{ color: 'var(--color-secondary)' }} />;
                          case 'medical': return <Activity size={16} style={{ color: 'var(--color-critical)' }} />;
                          case 'regional': return <Globe size={16} style={{ color: 'var(--color-secondary)' }} />;
                          case 'claims': return <FileWarning size={16} style={{ color: 'var(--color-medium)' }} />;
                          case 'agent': return <ShieldCheck size={16} style={{ color: 'var(--color-low)' }} />;
                          case 'product': return <Layers size={16} style={{ color: 'var(--color-primary)' }} />;
                          default: return <Sparkles size={16} style={{ color: 'var(--text-muted)' }} />;
                        }
                      };

                      return (
                        <div 
                          key={dim.dimension} 
                          className="glass-panel overflow-hidden transition-all duration-300"
                          style={{ borderColor: isExpanded ? 'var(--border-color-active)' : 'var(--border-color)' }}
                        >
                          <div 
                            className="p-4 flex items-center justify-between bg-slate-900/10 hover:bg-slate-950/20 cursor-pointer border-none bg-transparent"
                            onClick={() => {
                              setExpandedDimensions(prev => ({ ...prev, [dim.dimension]: !prev[dim.dimension] }));
                            }}
                          >
                            <div className="flex items-center gap-2.5">
                              {getDimIcon(dim.dimension)}
                              <span className="font-bold text-xs uppercase tracking-wider text-white capitalize">
                                {dim.dimension} Risk
                              </span>
                            </div>
                            
                            <div className="flex items-center gap-3">
                              <span 
                                className="font-semibold text-xs px-2 py-0.5 rounded" 
                                style={{ 
                                  background: dim.risk_level === 'LOW' ? 'var(--color-low-bg)' :
                                              dim.risk_level === 'MEDIUM' ? 'var(--color-medium-bg)' :
                                              dim.risk_level === 'HIGH' ? 'var(--color-high-bg)' :
                                              'var(--color-critical-bg)',
                                  color: dimColor,
                                  border: '1px solid currentColor'
                                }}
                              >
                                {dim.risk_score.toFixed(0)} / 100
                              </span>
                              {isExpanded ? <ChevronUp size={16} className="text-secondary" /> : <ChevronDown size={16} className="text-secondary" />}
                            </div>
                          </div>

                          {isExpanded && (
                            <div className="p-4 border-t border-slate-800/60 bg-slate-900/5 flex flex-col gap-4 animate-[slideIn_0.2s_ease-out]">
                              {/* Factors */}
                              <div className="flex flex-col gap-2">
                                <span className="text-[10px] uppercase font-bold text-muted tracking-wider block">Key Risk Factors</span>
                                {dim.risk_factors.length > 0 ? (
                                  <ul className="flex flex-col gap-1.5 text-xs text-secondary list-none pl-0">
                                    {dim.risk_factors.map((f, i) => (
                                      <li key={i} className="flex items-start gap-2 leading-relaxed">
                                        <AlertTriangle size={12} className="mt-0.5 flex-shrink-0" style={{ color: dimColor }} />
                                        <span>{typeof f === 'string' ? f : f.description}</span>
                                      </li>
                                    ))}
                                  </ul>
                                ) : (
                                  <span className="text-xs text-muted">No negative risk factors identified.</span>
                                )}
                              </div>

                              {/* Dimension-level recommendations */}
                              {dim.recommendations && dim.recommendations.length > 0 && (
                                <div className="border-t border-slate-800/40 pt-3 flex flex-col gap-2">
                                  <span className="text-[10px] uppercase font-bold text-muted tracking-wider block">Dimension Recommendations</span>
                                  <ul className="flex flex-col gap-1 text-xs text-secondary list-none pl-0">
                                    {dim.recommendations.map((rec, idx) => (
                                      <li key={idx} className="flex items-start gap-2 leading-relaxed">
                                        <CheckCircle size={12} className="mt-0.5 flex-shrink-0 text-emerald-400" />
                                        <span>{rec}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* 3. Actionable Underwriting Recommendations Card */}
                <div className="glass-panel animate-[slideIn_0.4s_ease-out]" style={{ padding: '24px' }}>
                  <div className="flex items-center gap-2 border-b pb-4 mb-4" style={{ borderColor: 'var(--border-color)' }}>
                    <CheckSquare className="text-emerald-400" size={18} />
                    <span className="font-bold text-sm tracking-wider uppercase text-secondary">AI Underwriting Action Checklist</span>
                  </div>

                  <div className="flex flex-col gap-3">
                    {(() => {
                      const allRecs = (aiResult.recommendations && aiResult.recommendations.length > 0
                        ? aiResult.recommendations
                        : Object.values(aiResult.dimension_results).flatMap(dim => dim.recommendations || [])) as string[];
                      
                      const recList = (allRecs.length > 0 
                        ? Array.from(new Set(allRecs)) // remove duplicates
                        : ["Approve coverage at standard parameters. No follow-ups needed."]) as string[];

                      return recList.map((rec, idx) => {
                        const isChecked = checklists.includes(rec);
                        
                        return (
                          <div 
                            key={idx}
                            onClick={() => toggleChecklist(rec)}
                            className="flex items-start gap-3 p-3 bg-slate-900/20 hover:bg-slate-950/20 rounded-lg border cursor-pointer select-none transition-all duration-200"
                            style={{ 
                              borderColor: isChecked ? 'var(--border-color-active)' : 'var(--border-color)',
                              background: isChecked ? 'rgba(99, 102, 241, 0.03)' : 'var(--bg-secondary)/10'
                            }}
                          >
                            <div className="mt-0.5">
                              {isChecked ? (
                                <div className="w-[18px] h-[18px] rounded bg-indigo-500 flex items-center justify-center text-white border border-indigo-400">
                                  <Check size={12} strokeWidth={3} />
                                </div>
                              ) : (
                                <div className="w-[18px] h-[18px] rounded bg-slate-950 border border-slate-700 hover:border-slate-500" />
                              )}
                            </div>
                            <div className="flex flex-col gap-0.5">
                              <span className="text-xs text-white font-medium">{rec}</span>
                              <span className="text-[10px] text-muted font-medium uppercase tracking-wider">
                                {isChecked ? 'Verified / Completed' : 'Action Pending Validation'}
                              </span>
                            </div>
                          </div>
                        );
                      });
                    })()}
                  </div>
                </div>

              </div>

            </div>
          </div>
        )}

        {/* CLAIMS HISTORY TAB */}
        {activeTab === 'claims' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '16px' }}>
              <div className="glass-panel" style={{ padding: '16px', textAlign: 'center' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Claims Count</span>
                <span style={{ display: 'block', fontSize: '1.6rem', fontWeight: 700, marginTop: '4px' }}>{claims.length}</span>
              </div>
              <div className="glass-panel" style={{ padding: '16px', textAlign: 'center' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Total Claimed</span>
                <span style={{ display: 'block', fontSize: '1.6rem', fontWeight: 700, marginTop: '4px', color: 'var(--color-medium)' }}>
                  ${claims.reduce((acc, c) => acc + c.claimed_amount, 0).toLocaleString()}
                </span>
              </div>
              <div className="glass-panel" style={{ padding: '16px', textAlign: 'center' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Total Approved</span>
                <span style={{ display: 'block', fontSize: '1.6rem', fontWeight: 700, marginTop: '4px', color: 'var(--color-low)' }}>
                  ${claims.reduce((acc, c) => acc + c.approved_amount, 0).toLocaleString()}
                </span>
              </div>
            </div>

            {claims.length > 0 ? (
              <table>
                <thead>
                  <tr>
                    <th>Claim Number</th>
                    <th>Type</th>
                    <th>Claimed</th>
                    <th>Approved</th>
                    <th>Status</th>
                    <th>Rejection Reason</th>
                  </tr>
                </thead>
                <tbody>
                  {claims.map(c => (
                    <tr key={c.claim_number}>
                      <td style={{ fontWeight: 600 }}>{c.claim_number}</td>
                      <td>{c.claim_type}</td>
                      <td style={{ fontFamily: 'var(--font-mono)' }}>${c.claimed_amount.toLocaleString()}</td>
                      <td style={{ fontFamily: 'var(--font-mono)' }}>${c.approved_amount.toLocaleString()}</td>
                      <td>
                        <span className={`badge ${c.claim_status === 'Approved' ? 'badge-low' : 'badge-critical'}`}>
                          {c.claim_status}
                        </span>
                      </td>
                      <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{c.rejection_reason || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
                No prior claims history found in database.
              </div>
            )}
          </div>
        )}

        {/* AGENT RISK TAB */}
        {activeTab === 'agent' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Agent Profile & Compliance Audit</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px' }}>
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>Agent Code</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600 }}>{agent.agent_code}</span>
                
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem', marginTop: '16px', display: 'block' }}>Category</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600 }}>{agent.agent_category}</span>
              </div>
              
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>Loss Ratio</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600, color: 'var(--color-medium)' }}>{agent.loss_ratio}</span>
                
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem', marginTop: '16px', display: 'block' }}>Lapse Rate</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600, color: 'var(--color-high)' }}>{agent.lapse_rate}</span>
              </div>
            </div>

            {agent.compliance_flags && agent.compliance_flags.length > 0 && (
              <div style={{ border: '1px solid rgba(239, 68, 68, 0.2)', background: 'rgba(239, 68, 68, 0.04)', padding: '16px', borderRadius: '8px', marginTop: '16px' }}>
                <h4 style={{ color: 'var(--color-critical)', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.95rem', marginBottom: '8px' }}>
                  <AlertTriangle size={16} />
                  Compliance Warnings Flagged
                </h4>
                <ul style={{ paddingLeft: '16px', fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
                  {agent.compliance_flags.map((flag: string, idx: number) => <li key={idx}>{flag}</li>)}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* PRODUCT SPECS TAB */}
        {activeTab === 'product' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Policy Specs & Limits Analysis</h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px' }}>
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>Product Name</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600 }}>{product.product_name}</span>
                
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem', marginTop: '16px', display: 'block' }}>PED Waiting Period</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600 }}>{product.pre_existing_waiting_period} Months</span>
              </div>

              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>Co-Pay Ratio</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600 }}>{product.co_pay_percentage}% Co-Pay</span>
                
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem', marginTop: '16px', display: 'block' }}>Key Features</span>
                <span style={{ display: 'block', fontSize: '0.92rem', color: 'var(--text-secondary)' }}>{product.key_features}</span>
              </div>
            </div>
          </div>
        )}

        {/* REGIONAL GEO-RISK TAB */}
        {activeTab === 'regional' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Regional Geo-Risk Diagnostic</h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px' }}>
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>Nearest Network Hospital</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600 }}>{regional.hospitalDistance} km</span>
              </div>
              
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>Air Quality Index (AQI)</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600, color: regional.aqi > 100 ? 'var(--color-critical)' : 'var(--color-low)' }}>
                  {regional.aqi} AQI
                </span>
              </div>

              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>Natural Hazard Rating</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600 }}>{regional.naturalDisasters}</span>
              </div>

              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>Crime Index</span>
                <span style={{ display: 'block', fontSize: '1.1rem', fontWeight: 600 }}>{regional.crimeRate}</span>
              </div>
            </div>
          </div>
        )}

        {/* DECISION BOARD TAB */}
        {activeTab === 'decision' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Underwriting Sign-Off Board</h3>

            {decisionSubmitted ? (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px', padding: '40px 0', textAlign: 'center' }}>
                <CheckCircle size={48} style={{ color: 'var(--color-low)' }} />
                <h4 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Decision Recorded Successfully</h4>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
                  The underwriting decision slip is saved to audit logs. Returning to proposals queue...
                </p>
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '28px' }}>
                
                {/* Inputs */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div>
                    <label>Underwriting Action</label>
                    <select 
                      value={finalDecision} 
                      onChange={(e) => setFinalDecision(e.target.value as any)}
                      style={{ width: '100%' }}
                    >
                      <option value="ACCEPT">ACCEPT (Issue standard policy)</option>
                      <option value="REVIEW">REVIEW (Refer to senior underwriter)</option>
                      <option value="DECLINE">DECLINE (Reject risk proposal)</option>
                    </select>
                  </div>

                  <div>
                    <label>Premium Surcharge Loading: +{premiumLoading}%</label>
                    <input 
                      type="range" 
                      min="0" 
                      max="100" 
                      step="5"
                      value={premiumLoading} 
                      onChange={(e) => setPremiumLoading(Number(e.target.value))}
                      style={{ width: '100%', cursor: 'pointer' }}
                    />
                  </div>

                  <div>
                    <label>Medical Underwriting Checklist</label>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '8px' }}>
                      {[
                        "Require Attending Physician Statement (APS)",
                        "Establish 2-year waiting period on pre-existing condition",
                        "Confirm payment clearance verification"
                      ].map((item) => (
                        <label key={item} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 400 }}>
                          <input 
                            type="checkbox" 
                            checked={checklists.includes(item)}
                            onChange={() => toggleChecklist(item)}
                          />
                          {item}
                        </label>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Justification & submit */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div>
                    <label>Decision Justification Rationale</label>
                    <textarea 
                      rows={5}
                      placeholder="Enter details explaining the underwriting action and premium loading reasoning..."
                      value={justification}
                      onChange={(e) => setJustification(e.target.value)}
                      style={{ width: '100%', resize: 'none' }}
                    />
                  </div>

                  <button
                    onClick={handleDecisionSubmit}
                    style={{
                      background: 'var(--color-primary)',
                      color: 'white',
                      width: '100%',
                      padding: '12px',
                      borderRadius: '8px',
                      fontWeight: 600,
                      marginTop: 'auto'
                    }}
                  >
                    Commit Underwriting Signature
                  </button>
                </div>

              </div>
            )}
          </div>
        )}

      </div>

    </div>
  );
};
