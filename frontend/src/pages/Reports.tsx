import React, { useState } from 'react';
import { Download, FileText, FileSpreadsheet, Code } from 'lucide-react';

export const Reports: React.FC = () => {
  const [reports, setReports] = useState<any[]>([]);
  const [format, setFormat] = useState<'PDF' | 'JSON' | 'CSV'>('PDF');
  const [proposalId, setProposalId] = useState('PROP001');
  const [generating, setGenerating] = useState(false);

  const handleGenerate = () => {
    setGenerating(true);
    setTimeout(() => {
      const extension = format.toLowerCase();
      const newReport = {
        id: `R00${reports.length + 1}`,
        filename: `Underwriting_Slip_${proposalId}.${extension}`,
        format: format,
        date: new Date().toISOString().replace('T', ' ').substring(0, 16),
        status: 'COMPLETED' as const
      };
      setReports([newReport, ...reports]);
      setGenerating(false);
    }, 1500);
  };

  const getFormatIcon = (f: 'PDF' | 'JSON' | 'CSV') => {
    if (f === 'PDF') return <FileText size={18} style={{ color: 'var(--color-critical)' }} />;
    if (f === 'CSV') return <FileSpreadsheet size={18} style={{ color: 'var(--color-low)' }} />;
    return <Code size={18} style={{ color: 'var(--color-secondary)' }} />;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px 0' }}>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px', alignItems: 'start' }}>
        
        {/* Generate Card */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '20px' }}>Generate Underwriting Slip</h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <label>Target Proposal ID</label>
              <select value={proposalId} onChange={(e) => setProposalId(e.target.value)} style={{ width: '100%' }}>
                <option value="PROP001">PROP001 (Gregory Smith)</option>
                <option value="PROP002">PROP002 (Sarah Miller)</option>
                <option value="PROP003">PROP003 (Arthur Pendleton)</option>
              </select>
            </div>

            <div>
              <label>Export Format</label>
              <select value={format} onChange={(e) => setFormat(e.target.value as any)} style={{ width: '100%' }}>
                <option value="PDF">PDF Underwriting Summary Document</option>
                <option value="JSON">JSON Schema Payload</option>
                <option value="CSV">CSV Data Row</option>
              </select>
            </div>

            <button
              onClick={handleGenerate}
              disabled={generating}
              style={{
                background: 'var(--color-primary)',
                color: 'white',
                padding: '12px',
                borderRadius: '8px',
                fontWeight: 600,
                marginTop: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              {generating ? (
                <>
                  <RefreshCw className="skeleton" size={16} style={{ animation: 'spin 1.5s linear infinite' }} />
                  Compiling diagnostics PDF...
                </>
              ) : (
                'Compile & Export Document'
              )}
            </button>
            <style dangerouslySetInnerHTML={{__html: `
              @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            `}} />
          </div>
        </div>

        {/* History Logs */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '20px' }}>Export History Registry</h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {reports.map((report) => (
              <div
                key={report.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px',
                  background: 'rgba(0,0,0,0.15)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '10px'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  {getFormatIcon(report.format)}
                  <div>
                    <span style={{ fontSize: '0.9rem', fontWeight: 600, display: 'block', wordBreak: 'break-all' }}>
                      {report.filename}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      Compiled: {report.date}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => alert(`Initiating browser file save for: ${report.filename}`)}
                  style={{
                    background: 'rgba(255,255,255,0.05)',
                    color: 'var(--text-primary)',
                    padding: '8px',
                    borderRadius: '6px',
                    display: 'flex',
                    alignItems: 'center'
                  }}
                  className="glass-panel-interactive"
                >
                  <Download size={14} />
                </button>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};

// Simple Refresh icon helper fallback
const RefreshCw: React.FC<{ className?: string; size?: number; style?: React.CSSProperties }> = ({ className, size = 16, style }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    width={size} 
    height={size} 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    strokeWidth="2" 
    strokeLinecap="round" 
    strokeLinejoin="round" 
    className={className}
    style={style}
  >
    <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
    <path d="M3 3v5h5" />
    <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16" />
    <path d="M16 16h5v5" />
  </svg>
);
