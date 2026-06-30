import React, { useState } from 'react';
import { ProposalSummary, SystemHealth } from '../types';
import { 
  FileText, Shield, AlertTriangle, CheckCircle, Database, Brain, 
  TrendingUp, Users, Activity, MapPin, BarChart3
} from 'lucide-react';

interface DashboardProps {
  proposals: ProposalSummary[];
  systemHealth: SystemHealth | null;
  setCurrentPage: (page: string) => void;
  setSelectedProposalId: (id: string) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({
  proposals,
  systemHealth,
  setCurrentPage,
  setSelectedProposalId
}) => {
  const [activeTooltip, setActiveTooltip] = useState<string | null>(null);

  // Widget calculations (using loaded proposals properties)
  const realCount = proposals.length;
  
  const totalApps = realCount;
  const acceptedApps = proposals.filter(p => p.kyc_status === 'Verified' && !p.has_chronic_disease_data).length;
  const reviewApps = proposals.filter(p => p.has_chronic_disease_data || p.has_claims_data).length;
  const declinedApps = proposals.filter(p => p.kyc_status === 'High Risk Flags' || (p.member_age && p.member_age > 75)).length;
  
  const computeProposalRiskScore = (p: ProposalSummary): number => {
    let score = 15;
    if (p.has_chronic_disease_data) score += 35;
    if (p.kyc_status === 'High Risk Flags') score += 30;
    if (p.claims_count) score += Math.min(30, p.claims_count * 8);
    if (p.member_age) {
      if (p.member_age > 60) score += 20;
      else if (p.member_age > 45) score += 10;
    }
    return Math.min(100, score);
  };

  const getProposalRiskLevel = (score: number): 'Low' | 'Medium' | 'High' | 'Critical' => {
    if (score >= 70) return 'Critical';
    if (score >= 50) return 'High';
    if (score >= 30) return 'Medium';
    return 'Low';
  };

  const avgRiskScore = realCount > 0 
    ? Math.round(proposals.reduce((acc, p) => acc + computeProposalRiskScore(p), 0) / realCount)
    : 0;

  const avgMedicalRisk = realCount > 0
    ? Math.round((proposals.filter(p => p.has_chronic_disease_data).length / realCount) * 100)
    : 0;

  const avgFinancialRisk = realCount > 0
    ? Math.round((proposals.filter(p => p.annual_income && p.annual_income < 100000).length / realCount) * 100)
    : 0;

  const avgClaimsRisk = realCount > 0
    ? Math.round((proposals.filter(p => p.has_claims_data).length / realCount) * 100)
    : 0;

  const avgAgentRisk = realCount > 0
    ? Math.round((proposals.filter(p => p.agent_category && p.agent_category.includes('Broker')).length / realCount) * 100)
    : 0;

  const avgRegionalRisk = realCount > 0
    ? Math.round((proposals.filter(p => p.lead_state === 'CA' || p.lead_state === 'FL').length / realCount) * 100)
    : 0;


  // 10 Dashboard Widgets Data
  const widgets = [
    { label: 'Total Applications', value: totalApps, sub: '+12% vs last month', icon: FileText, color: '#6366f1' },
    { label: 'Accepted Applications', value: acceptedApps, sub: '60.8% acceptance rate', icon: CheckCircle, color: '#10b981' },
    { label: 'Review Applications', value: reviewApps, sub: '26.1% manual audit pool', icon: AlertTriangle, color: '#f59e0b' },
    { label: 'Declined Applications', value: declinedApps, sub: '13.1% high-risk filters', icon: Shield, color: '#ef4444' },
    { label: 'Average Risk Score', value: `${avgRiskScore}/100`, sub: 'Medium Severity Grade', icon: Activity, color: '#06b6d4' },
    { label: 'Medical Risk Index', value: `${avgMedicalRisk}%`, sub: 'Cardio & Diabetes primary', icon: Brain, color: '#ec4899' },
    { label: 'Financial Risk Index', value: `${avgFinancialRisk}%`, sub: 'Debt Ratio standard bounds', icon: BarChart3, color: '#8b5cf6' },
    { label: 'Claims Risk Index', value: `${avgClaimsRisk}%`, sub: 'Low claims frequency', icon: TrendingUp, color: '#14b8a6' },
    { label: 'Agent Channel Risk', value: `${avgAgentRisk}%`, sub: 'High persistency rating', icon: Users, color: '#f97316' },
    { label: 'Regional Risk Index', value: `${avgRegionalRisk}%`, sub: 'Low geo-hazard triggers', icon: MapPin, color: '#3b82f6' }
  ];

  const decisionsData = [
    { label: 'Accepted', value: acceptedApps, color: '#10b981' },
    { label: 'Review', value: reviewApps, color: '#f59e0b' },
    { label: 'Declined', value: declinedApps, color: '#ef4444' }
  ];

  const topAgents = [
    { name: 'Monocept Channel', sales: 65, persistency: 94, color: '#6366f1' },
    { name: 'Direct Portal', sales: 48, persistency: 91, color: '#06b6d4' },
    { name: 'Apex Brokers', sales: 32, persistency: 88, color: '#10b981' },
    { name: 'Metropolitan Corp', sales: 26, persistency: 85, color: '#f59e0b' },
    { name: 'Northwest Agency', sales: 18, persistency: 82, color: '#ef4444' }
  ];

  const handleUnderwrite = (proposalNum: string) => {
    setSelectedProposalId(proposalNum);
    setCurrentPage('detail');
  };

  // Helper for SVG donut segments calculation
  // Radius = 40, Circumference = 2 * PI * r = 251.327
  const donutRadius = 40;
  const donutCircumference = 2 * Math.PI * donutRadius;
  
  const lowCount = proposals.filter(p => getProposalRiskLevel(computeProposalRiskScore(p)) === 'Low').length;
  const mediumCount = proposals.filter(p => getProposalRiskLevel(computeProposalRiskScore(p)) === 'Medium').length;
  const highCount = proposals.filter(p => getProposalRiskLevel(computeProposalRiskScore(p)) === 'High').length;
  const criticalCount = proposals.filter(p => getProposalRiskLevel(computeProposalRiskScore(p)) === 'Critical').length;

  const pieCategories = [
    { label: 'Low Risk', value: realCount > 0 ? lowCount : 1, color: '#10b981' },
    { label: 'Medium Risk', value: realCount > 0 ? mediumCount : 0, color: '#f59e0b' },
    { label: 'High Risk', value: realCount > 0 ? highCount : 0, color: '#f97316' },
    { label: 'Critical Risk', value: realCount > 0 ? criticalCount : 0, color: '#ef4444' }
  ];

  let accumulatedPercentage = 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px', padding: '24px 0' }}>
      
      {/* 10 Enterprise Dashboard Widgets */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
        {widgets.map((widget, idx) => {
          const Icon = widget.icon;
          return (
            <div 
              key={idx} 
              className="glass-panel" 
              style={{ 
                padding: '16px 20px', 
                display: 'flex', 
                flexDirection: 'column', 
                gap: '12px',
                position: 'relative',
                overflow: 'hidden'
              }}
            >
              {/* Colored top gradient highlight strip */}
              <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: '3px', background: widget.color }} />
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  {widget.label}
                </span>
                <Icon size={16} style={{ color: widget.color }} />
              </div>
              <div>
                <span style={{ fontSize: '1.6rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                  {widget.value}
                </span>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'block', marginTop: '2px' }}>
                  {widget.sub}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* SVG Charts Rows */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }} className="max-xl:grid-cols-1">
        
        {/* Chart 1: Risk Trend Line Chart */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>Risk Score Historical Trend</h3>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Average monthly portfolio evaluation risk indexes</span>
            </div>
            <span className="badge badge-low" style={{ fontSize: '0.72rem' }}>
              6-Month aggregate: 43.5 Avg
            </span>
          </div>

          {/* Line Chart SVG */}
          <div style={{ width: '100%', height: '220px', position: 'relative' }}>
            <svg width="100%" height="100%" viewBox="0 0 600 220" preserveAspectRatio="none">
              <defs>
                <linearGradient id="trendGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="rgba(99, 102, 241, 0.25)" />
                  <stop offset="100%" stopColor="rgba(99, 102, 241, 0.0)" />
                </linearGradient>
              </defs>
              
              {/* Grid Lines */}
              {[40, 90, 140, 190].map((y, i) => (
                <line key={i} x1="50" y1={y} x2="570" y2={y} stroke="var(--border-color)" strokeWidth="1" strokeDasharray="3 3" />
              ))}

              {/* Area Under Curve */}
              <path 
                d="M 50 190 L 50 110 L 150 90 L 255 100 L 360 75 L 465 85 L 570 95 L 570 190 Z" 
                fill="url(#trendGrad)" 
              />
              
              {/* Line path */}
              <path 
                d="M 50 110 Q 100 95 150 90 T 255 100 T 360 75 T 465 85 T 570 95" 
                fill="none" 
                stroke="#6366f1" 
                strokeWidth="3.5" 
                strokeLinecap="round"
              />

              {/* Data circles & hover logic */}
              {[
                { x: 50, y: 110, val: 39, date: 'Jan' },
                { x: 150, y: 90, val: 43, date: 'Feb' },
                { x: 255, y: 100, val: 41, date: 'Mar' },
                { x: 360, y: 75, val: 46, date: 'Apr' },
                { x: 465, y: 85, val: 44, date: 'May' },
                { x: 570, y: 95, val: avgRiskScore, date: 'Jun' }
              ].map((pt, i) => (
                <g key={i}>
                  <circle 
                    cx={pt.x} 
                    cy={pt.y} 
                    r="5" 
                    fill="#1e1b4b" 
                    stroke="#818cf8" 
                    strokeWidth="3" 
                    style={{ cursor: 'pointer' }}
                    onMouseEnter={() => setActiveTooltip(`trend-${i}`)}
                    onMouseLeave={() => setActiveTooltip(null)}
                  />
                  <text x={pt.x} y="212" fill="var(--text-muted)" fontSize="11" textAnchor="middle">
                    {pt.date}
                  </text>
                  {activeTooltip === `trend-${i}` && (
                    <g>
                      <rect x={pt.x - 30} y={pt.y - 34} width="60" height="22" rx="4" fill="var(--bg-secondary)" stroke="var(--border-color)" strokeWidth="1" />
                      <text x={pt.x} y={pt.y - 19} fill="var(--text-primary)" fontSize="11" fontWeight="600" textAnchor="middle">
                        {pt.val}/100
                      </text>
                    </g>
                  )}
                </g>
              ))}
            </svg>
          </div>
        </div>

        {/* Chart 2: Risk Category Pie/Donut Chart */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>Risk Classification</h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Portfolio split by risk categories</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '180px', marginTop: '12px', gap: '16px' }}>
            {/* SVG Donut */}
            <svg width="120" height="120" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="40" fill="transparent" stroke="rgba(255,255,255,0.02)" strokeWidth="10" />
              {pieCategories.map((cat, i) => {
                const dashOffset = donutCircumference - (donutCircumference * cat.value) / 100;
                const rotation = (accumulatedPercentage * 360) / 100;
                accumulatedPercentage += cat.value;
                return (
                  <circle
                    key={i}
                    cx="50"
                    cy="50"
                    r="40"
                    fill="transparent"
                    stroke={cat.color}
                    strokeWidth="10"
                    strokeDasharray={donutCircumference}
                    strokeDashoffset={dashOffset}
                    transform={`rotate(${rotation - 90} 50 50)`}
                    strokeLinecap="round"
                    style={{ transition: 'stroke-dashoffset 0.5s ease' }}
                  />
                );
              })}
              {/* Inner Label */}
              <text x="50" y="47" textAnchor="middle" fill="var(--text-primary)" fontSize="11" fontWeight="700">
                PORTFOLIO
              </text>
              <text x="50" y="60" textAnchor="middle" fill="var(--text-secondary)" fontSize="9" fontWeight="600">
                100% AUDIT
              </text>
            </svg>

            {/* Legends */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', flex: 1 }}>
              {pieCategories.map((cat, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', justifySelf: 'start', gap: '8px' }}>
                  <span style={{ width: '8px', height: '8px', borderRadius: '2px', background: cat.color }} />
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
                    {cat.label}: <strong style={{ color: 'var(--text-primary)' }}>{cat.value}%</strong>
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }} className="max-xl:grid-cols-1">
        
        {/* Chart 3: Underwriting Decision Bar Chart */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>Underwriting Decisions Ratio</h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Status aggregation for general policy issuance recommendations</span>
          </div>

          <div style={{ width: '100%', height: '220px', display: 'flex', alignItems: 'flex-end', justifyContent: 'space-around', padding: '20px 40px 10px 40px', marginTop: '12px', borderBottom: '1px solid var(--border-color)', position: 'relative' }}>
            
            {/* Grid background markers */}
            <div style={{ position: 'absolute', top: '10px', bottom: '50px', left: '20px', right: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', zIndex: 1, pointerEvents: 'none' }}>
              {[1, 2, 3].map((_, i) => (
                <div key={i} style={{ borderBottom: '1px solid var(--border-color)', width: '100%', opacity: 0.5 }} />
              ))}
            </div>

            {decisionsData.map((d, i) => {
              const maxVal = Math.max(...decisionsData.map(v => v.value));
              const heightPct = (d.value / maxVal) * 75; // Cap at 75% height
              return (
                <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px', zIndex: 2 }}>
                  <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {d.value}
                  </span>
                  <div 
                    style={{ 
                      width: '64px', 
                      height: `${heightPct}%`, 
                      background: `linear-gradient(to top, ${d.color}, ${d.color}cc)`, 
                      borderRadius: '8px 8px 0 0',
                      minHeight: '20px',
                      boxShadow: `0 4px 12px ${d.color}22`
                    }} 
                  />
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
                    {d.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Chart 4: Claims Analysis Chart */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>Claims Utilization vs Denials</h3>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Claims processed volumes relative to percent denial rate</span>
            </div>
            <span className="badge badge-medium" style={{ fontSize: '0.72rem' }}>
              Average Denial: 5.3%
            </span>
          </div>

          {/* Area/Line Chart SVG */}
          <div style={{ width: '100%', height: '220px', position: 'relative' }}>
            <svg width="100%" height="100%" viewBox="0 0 600 220" preserveAspectRatio="none">
              <defs>
                <linearGradient id="claimsGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="rgba(6, 182, 212, 0.2)" />
                  <stop offset="100%" stopColor="rgba(6, 182, 212, 0.0)" />
                </linearGradient>
              </defs>

              {/* Grid Lines */}
              {[40, 90, 140, 190].map((y, i) => (
                <line key={i} x1="50" y1={y} x2="570" y2={y} stroke="var(--border-color)" strokeWidth="1" strokeDasharray="3 3" />
              ))}

              {/* Volume Area (Claims Volume Series) */}
              {/* Data: [18, 24, 21, 35, 29, 34] maps to Y: [140, 120, 130, 80, 100, 85] */}
              <path 
                d="M 50 190 L 50 140 L 150 120 L 255 130 L 360 80 L 465 100 L 570 85 L 570 190 Z" 
                fill="url(#claimsGrad)" 
              />
              <path 
                d="M 50 140 Q 100 125 150 120 T 255 130 T 360 80 T 465 100 T 570 85" 
                fill="none" 
                stroke="#06b6d4" 
                strokeWidth="2.5" 
                strokeLinecap="round"
              />

              {/* Denial Rate Line (Denials Series in Red) */}
              {/* Data: [4, 6, 5, 8, 4, 5] maps to Y: [150, 130, 140, 110, 150, 140] */}
              <path 
                d="M 50 150 Q 100 135 150 130 T 255 140 T 360 110 T 465 150 T 570 140" 
                fill="none" 
                stroke="#ef4444" 
                strokeWidth="2" 
                strokeLinecap="round"
                strokeDasharray="4 4"
              />

              {/* Dots and Labels */}
              {[
                { x: 50, vol: 18, rate: 4, label: 'Jan' },
                { x: 150, vol: 24, rate: 6, label: 'Feb' },
                { x: 255, vol: 21, rate: 5, label: 'Mar' },
                { x: 360, vol: 35, rate: 8, label: 'Apr' },
                { x: 465, vol: 29, rate: 4, label: 'May' },
                { x: 570, vol: 34, rate: 5, label: 'Jun' }
              ].map((pt, i) => (
                <g key={i}>
                  <text x={pt.x} y="212" fill="var(--text-muted)" fontSize="11" textAnchor="middle">
                    {pt.label}
                  </text>
                  {/* Hover tooltip triggers for volume */}
                  <circle cx={pt.x} cy={80 + (40 * (i % 2))} r="4" fill="#06b6d4" />
                </g>
              ))}
            </svg>
            
            {/* Visual indicators */}
            <div style={{ position: 'absolute', top: '10px', right: '10px', display: 'flex', gap: '12px', fontSize: '0.72rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                <span style={{ width: '10px', height: '2px', background: '#06b6d4' }} />
                <span style={{ color: 'var(--text-secondary)' }}>Claims Count</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                <span style={{ width: '10px', height: '2px', background: '#ef4444', borderStyle: 'dashed', borderWidth: '1px' }} />
                <span style={{ color: 'var(--text-secondary)' }}>Denial Rate %</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }} className="max-xl:grid-cols-1">
        
        {/* Chart 5: Agent Performance Chart */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>Top Distribution Channels Performance</h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Total written policies relative to persistency rate %</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginTop: '20px' }}>
            {topAgents.map((agent, i) => {
              const maxSales = Math.max(...topAgents.map(a => a.sales));
              const widthPct = (agent.sales / maxSales) * 75; // Scale to max 75%
              return (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{ width: '120px', fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {agent.name}
                  </span>
                  
                  {/* Horizontal Bar container */}
                  <div style={{ flex: 1, background: 'rgba(255,255,255,0.02)', height: '14px', borderRadius: '4px', overflow: 'hidden' }}>
                    <div 
                      style={{ 
                        width: `${widthPct}%`, 
                        background: agent.color, 
                        height: '100%', 
                        borderRadius: '4px',
                        boxShadow: `0 0 10px ${agent.color}33`
                      }} 
                    />
                  </div>

                  <span style={{ width: '50px', fontSize: '0.85rem', color: 'var(--text-primary)', fontWeight: 700, textAlign: 'right' }}>
                    {agent.sales}
                  </span>
                  
                  {/* Persistency indicator badge */}
                  <span className="badge badge-low" style={{ fontSize: '0.7rem', padding: '2px 8px', width: '55px', justifyContent: 'center' }}>
                    {agent.persistency}%
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Diagnostic info block / Summary info */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Database size={24} style={{ color: 'var(--color-primary)' }} />
            <div>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>Active Database Inspection</h3>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Status validation & indexing metrics</span>
            </div>
          </div>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            The risk calculation model dynamically pulls demographics, chronic PED codes (ICD-10), historical claims frequency indexes, and ambulance logs (HCPCS) directly from the persistent schema nodes.
          </p>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', background: 'rgba(0,0,0,0.12)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem' }}>
              <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Active Postgres Pool:</span>
              <strong style={{ color: 'var(--text-primary)' }}>Healthy ({systemHealth?.db.tables_count || 15} tables)</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginTop: '4px' }}>
              <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Ollama AI Service:</span>
              <strong style={{ color: 'var(--text-primary)' }}>{systemHealth?.ollama.model || 'gpt-oss:20b'}</strong>
            </div>
          </div>
        </div>

      </div>

      {/* Recent Proposals List */}
      <div className="glass-panel" style={{ padding: '24px', overflow: 'hidden' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Active Proposals Queue</h3>
          <button 
            onClick={() => setCurrentPage('proposals')}
            style={{ fontSize: '0.85rem', color: 'var(--color-primary)', background: 'transparent', fontWeight: 600 }}
          >
            View All Proposals &rarr;
          </button>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table>
            <thead>
              <tr>
                <th>Proposal Num</th>
                <th>Insured Member</th>
                <th>Product Plan</th>
                <th>Sum Insured</th>
                <th>Risk Factors</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {proposals.map(proposal => (
                <tr key={proposal.proposal_num}>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                    {proposal.proposal_num}
                  </td>
                  <td>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                      <span style={{ fontWeight: 500 }}>
                        {proposal.member_age} Years, {proposal.member_gender}
                      </span>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        {proposal.lead_city || 'N/A'}, {proposal.lead_state || 'N/A'}
                      </span>
                    </div>
                  </td>
                  <td>
                    <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>
                      {proposal.product_name || `Product ID ${proposal.product_id}`}
                    </span>
                  </td>
                  <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 500 }}>
                    ${proposal.sum_insured?.toLocaleString()}
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                      {proposal.has_chronic_disease_data && (
                        <span className="badge badge-critical" style={{ fontSize: '0.68rem', padding: '3px 8px' }}>Chronic PED</span>
                      )}
                      {proposal.has_claims_data && (
                        <span className="badge badge-medium" style={{ fontSize: '0.68rem', padding: '3px 8px' }}>Has Claims</span>
                      )}
                      {!proposal.has_chronic_disease_data && !proposal.has_claims_data && (
                        <span className="badge badge-low" style={{ fontSize: '0.68rem', padding: '3px 8px' }}>Clean Record</span>
                      )}
                    </div>
                  </td>
                  <td>
                    <button
                      onClick={() => handleUnderwrite(proposal.proposal_num)}
                      style={{
                        background: 'var(--color-primary)',
                        color: 'white',
                        padding: '6px 14px',
                        borderRadius: '6px',
                        fontSize: '0.82rem',
                        fontWeight: 600
                      }}
                      className="glass-panel-interactive"
                    >
                      Audit Risk
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
    </div>
  );
};
