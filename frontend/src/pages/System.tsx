import React from 'react';
import { SystemHealth } from '../types';
import { Database, Server, Cpu, RefreshCw, CheckCircle, XCircle } from 'lucide-react';

interface SystemProps {
  systemHealth: SystemHealth | null;
  loading: boolean;
  refreshHealth: () => Promise<void>;
  mockMode: boolean;
  setMockMode: (mode: boolean) => void;
}

export const System: React.FC<SystemProps> = ({
  systemHealth,
  loading,
  refreshHealth,
  mockMode,
  setMockMode
}) => {
  const getStatusBadge = (status: 'healthy' | 'unhealthy' | 'loading') => {
    if (status === 'loading') {
      return <span className="badge" style={{ background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)' }}>Checking...</span>;
    }
    return status === 'healthy' ? (
      <span className="badge badge-low" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
        <CheckCircle size={12} />
        ONLINE
      </span>
    ) : (
      <span className="badge badge-critical" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
        <XCircle size={12} />
        UNREACHABLE
      </span>
    );
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px 0' }}>
      
      {/* Settings bar */}
      <div className="glass-panel" style={{ padding: '16px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>Connection Parameters</h3>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Manage API endpoint behaviors and sandboxing options</span>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={() => setMockMode(!mockMode)}
            style={{
              background: mockMode ? 'rgba(99,102,241,0.15)' : 'rgba(255,255,255,0.05)',
              border: mockMode ? '1px solid rgba(99,102,241,0.3)' : '1px solid var(--border-color)',
              color: mockMode ? 'var(--text-primary)' : 'var(--text-secondary)',
              padding: '8px 16px',
              borderRadius: '8px',
              fontSize: '0.88rem',
              fontWeight: 600
            }}
          >
            {mockMode ? 'Switch to Live API Mode' : 'Switch to Sandbox Standalone'}
          </button>
          <button
            onClick={refreshHealth}
            disabled={loading}
            style={{
              background: 'var(--color-primary)',
              color: 'white',
              padding: '8px 16px',
              borderRadius: '8px',
              fontSize: '0.88rem',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <RefreshCw size={14} className={loading ? 'skeleton' : ''} style={{ animation: loading ? 'spin 1.5s linear infinite' : 'none' }} />
            Run Diagnostics
          </button>
        </div>
      </div>

      {/* Diagnostics Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
        
        {/* API Server */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Server size={22} style={{ color: 'var(--color-primary)' }} />
              <h4 style={{ fontSize: '1.05rem', fontWeight: 600 }}>FastAPI Server</h4>
            </div>
            {getStatusBadge(mockMode ? 'healthy' : systemHealth?.api.status || 'loading')}
          </div>
          
          <div style={{ fontSize: '0.92rem', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>Default Port</span>
              <span style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-mono)' }}>http://127.0.0.1:8000</span>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>Endpoint Version</span>
              <span style={{ color: 'var(--text-primary)' }}>v{mockMode ? '0.2.0' : systemHealth?.api.version || '0.2.0'}</span>
            </div>
          </div>
        </div>

        {/* Database */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Database size={22} style={{ color: 'var(--color-secondary)' }} />
              <h4 style={{ fontSize: '1.05rem', fontWeight: 600 }}>PostgreSQL Database</h4>
            </div>
            {getStatusBadge(mockMode ? 'healthy' : systemHealth?.db.status || 'loading')}
          </div>
          
          <div style={{ fontSize: '0.92rem', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>Active Relational Tables</span>
              <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
                {mockMode ? '15 SQL Tables Created' : systemHealth?.db.tables_count ? `${systemHealth.db.tables_count} Tables Found` : 'No connection'}
              </span>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>ORM Schema Manager</span>
              <span style={{ color: 'var(--text-primary)' }}>SQLAlchemy 2.0 + Alembic</span>
            </div>
          </div>
        </div>

        {/* Ollama LLM */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Cpu size={22} style={{ color: 'var(--color-low)' }} />
              <h4 style={{ fontSize: '1.05rem', fontWeight: 600 }}>Ollama AI Service</h4>
            </div>
            {getStatusBadge(mockMode ? 'healthy' : systemHealth?.ollama.status || 'loading')}
          </div>
          
          <div style={{ fontSize: '0.92rem', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>Target Model Parameter</span>
              <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
                {mockMode ? 'gpt-oss:20b' : systemHealth?.ollama.model || 'gpt-oss:20b'}
              </span>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.78rem' }}>AI Endpoint URL</span>
              <span style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-mono)' }}>
                {mockMode ? 'http://localhost:11434' : systemHealth?.ollama.base_url || 'http://localhost:11434'}
              </span>
            </div>
          </div>
        </div>

      </div>

      {/* Database Tables Detail Viewer */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '16px' }}>Schema Inspection: 15 Tables Registry</h3>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '20px', lineHeight: 1.45 }}>
          The risk calculator pulls data across 15 custom tables. The active tables detected by inspect schema are:
        </p>

        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          {(mockMode ? [
            "proposal_details", "member_details", "product_details", 
            "chronic_disease_details", "product_sub_question_mapping", 
            "kyc_details", "payment_details", "lead_details", 
            "blacklisted_hospitals", "claim_details", "agent_details", 
            "annual_club_performance", "hospital_master", "agent_risk_scores", 
            "portability_details"
          ] : systemHealth?.db.tables || []).map((table) => (
            <div
              key={table}
              style={{
                background: 'rgba(255, 255, 255, 0.03)',
                border: '1px solid var(--border-color)',
                borderRadius: '8px',
                padding: '8px 14px',
                fontSize: '0.88rem',
                fontFamily: 'var(--font-mono)',
                color: 'var(--text-primary)'
              }}
            >
              {table}
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
