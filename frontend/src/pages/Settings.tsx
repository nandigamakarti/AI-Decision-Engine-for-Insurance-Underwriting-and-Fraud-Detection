import React, { useState } from 'react';
import { SystemHealth } from '../types';
import { Cpu, Database, Server, RefreshCw, CheckCircle } from 'lucide-react';

interface SettingsProps {
  systemHealth: SystemHealth | null;
  loading: boolean;
  refreshHealth: () => Promise<void>;
  mockMode: boolean;
}

export const Settings: React.FC<SettingsProps> = ({
  systemHealth,
  loading,
  refreshHealth,
  mockMode
}) => {
  // Config States loaded from localStorage or fallback defaults
  const [model, setModel] = useState(() => {
    return localStorage.getItem('uw_settings_model') || systemHealth?.ollama.model || 'gpt-oss:20b';
  });
  const [temperature, setTemperature] = useState(() => {
    const saved = localStorage.getItem('uw_settings_temp');
    return saved !== null ? Number(saved) : (systemHealth?.ollama.temperature || 0.01);
  });
  const [baseURL, setBaseURL] = useState(() => {
    return localStorage.getItem('uw_settings_base_url') || systemHealth?.ollama.base_url || 'http://localhost:11434';
  });
  const [saveSuccess, setSaveSuccess] = useState(false);

  const handleSave = () => {
    localStorage.setItem('uw_settings_model', model);
    localStorage.setItem('uw_settings_temp', temperature.toString());
    localStorage.setItem('uw_settings_base_url', baseURL);
    setSaveSuccess(true);
    setTimeout(() => {
      setSaveSuccess(false);
    }, 2000);
  };

  const getStatusLight = (status: 'healthy' | 'unhealthy' | 'loading' | undefined) => {
    if (status === 'loading') return 'rgba(255, 255, 255, 0.2)';
    return status === 'healthy' ? 'var(--color-low)' : 'var(--color-critical)';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px 0' }}>
      
      <div style={{ display: 'grid', gridTemplateColumns: '5fr 3fr', gap: '24px', alignItems: 'start' }}>
        
        {/* Settings Fields */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Underwriter Engine Configurations</h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div>
              <label htmlFor="settings-model-select">Target LLM Model</label>
              <select id="settings-model-select" value={model} onChange={(e) => setModel(e.target.value)} style={{ width: '100%' }}>
                <option value="gpt-oss:20b">gpt-oss:20b (Default)</option>
                <option value="mistral">mistral (Fast - 7B)</option>
                <option value="llama2">llama2 (Instruction Capable)</option>
              </select>
            </div>

            <div>
              <label htmlFor="settings-base-url-input">Ollama Base URL</label>
              <input id="settings-base-url-input" type="text" value={baseURL} onChange={(e) => setBaseURL(e.target.value)} style={{ width: '100%' }} />
            </div>
          </div>

          <div>
            <label htmlFor="settings-temp-input">Inference Temperature: {temperature.toFixed(2)}</label>
            <input 
              id="settings-temp-input"
              type="range" 
              min="0" 
              max="1" 
              step="0.05"
              value={temperature} 
              onChange={(e) => setTemperature(Number(e.target.value))}
              style={{ width: '100%', cursor: 'pointer' }}
            />
            <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'block', marginTop: '4px' }}>
              Lower temperatures enforce consistent structured JSON underwriting replies.
            </span>
          </div>

          <div style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
            <button
              onClick={handleSave}
              style={{
                background: 'var(--color-primary)',
                color: 'white',
                padding: '10px 20px',
                borderRadius: '8px',
                fontWeight: 600,
                fontSize: '0.9rem'
              }}
            >
              Save Parameters
            </button>
            
            {saveSuccess && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--color-low)', fontSize: '0.88rem', fontWeight: 600 }}>
                <CheckCircle size={16} />
                Configurations saved locally!
              </div>
            )}
          </div>
        </div>

        {/* Diagnostic Checks status list */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Diagnostic Audit</h3>
            <button 
              onClick={refreshHealth} 
              disabled={loading}
              style={{ background: 'transparent', color: 'var(--color-primary)' }}
            >
              <RefreshCw size={16} className={loading ? 'skeleton' : ''} style={{ animation: loading ? 'spin 1.5s linear infinite' : 'none' }} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {[
              { label: 'FastAPI Backend Connection', status: mockMode ? 'healthy' : systemHealth?.api.status, icon: Server },
              { label: 'PostgreSQL Tables Registry', status: mockMode ? 'healthy' : systemHealth?.db.status, icon: Database },
              { label: 'Ollama Inference Health', status: mockMode ? 'healthy' : systemHealth?.ollama.status, icon: Cpu }
            ].map((srv, idx) => {
              const Icon = srv.icon;
              return (
                <div key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px', background: 'rgba(0,0,0,0.15)', border: '1px solid var(--border-color)', borderRadius: '8px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <Icon size={16} style={{ color: 'var(--text-secondary)' }} />
                    <span style={{ fontSize: '0.88rem', fontWeight: 500 }}>{srv.label}</span>
                  </div>
                  <span style={{
                    width: '10px',
                    height: '10px',
                    borderRadius: '50%',
                    background: getStatusLight(srv.status),
                    boxShadow: `0 0 8px ${getStatusLight(srv.status)}`
                  }} />
                </div>
              );
            })}
          </div>
        </div>

      </div>

    </div>
  );
};
