import React, { useState } from 'react';
import { Search, AlertCircle, AlertTriangle, Info, Terminal } from 'lucide-react';

export const AuditLogs: React.FC = () => {
  const [logs, setLogs] = useState<any[]>([
    { id: "L001", timestamp: new Date().toISOString().substring(0, 19), level: "INFO", category: "API", message: "FastAPI server logging stream initialized." },
    { id: "L002", timestamp: new Date().toISOString().substring(0, 19), level: "INFO", category: "DB", message: "Database connection initialized. Tables verified." }
  ]);
  const [levelFilter, setLevelFilter] = useState<'ALL' | 'INFO' | 'WARNING' | 'ERROR'>('ALL');
  const [search, setSearch] = useState('');

  const filteredLogs = logs.filter(log => {
    const matchesLevel = levelFilter === 'ALL' || log.level === levelFilter;
    const matchesSearch = log.message.toLowerCase().includes(search.toLowerCase()) || 
                          log.category.toLowerCase().includes(search.toLowerCase());
    return matchesLevel && matchesSearch;
  });

  const getLevelColor = (level: 'INFO' | 'WARNING' | 'ERROR') => {
    if (level === 'ERROR') return 'var(--color-critical)';
    if (level === 'WARNING') return 'var(--color-medium)';
    return 'var(--color-low)';
  };

  const getLevelIcon = (level: 'INFO' | 'WARNING' | 'ERROR') => {
    if (level === 'ERROR') return <AlertCircle size={14} style={{ color: 'var(--color-critical)' }} />;
    if (level === 'WARNING') return <AlertTriangle size={14} style={{ color: 'var(--color-medium)' }} />;
    return <Info size={14} style={{ color: 'var(--color-low)' }} />;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px 0' }}>
      
      {/* Filters bar */}
      <div className="glass-panel" style={{ padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        
        {/* Search */}
        <div style={{ display: 'flex', alignItems: 'center', position: 'relative', flex: 1, minWidth: '250px' }}>
          <Search size={16} style={{ position: 'absolute', left: '12px', color: 'var(--text-muted)' }} />
          <input 
            type="text" 
            placeholder="Search console logs by keyword or category..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: '100%', paddingLeft: '38px', fontSize: '0.88rem' }}
          />
        </div>

        {/* Level Filters */}
        <div style={{ display: 'flex', gap: '6px' }}>
          {(['ALL', 'INFO', 'WARNING', 'ERROR'] as const).map(lvl => {
            const isActive = levelFilter === lvl;
            return (
              <button
                key={lvl}
                onClick={() => setLevelFilter(lvl)}
                style={{
                  background: isActive ? 'rgba(99, 102, 241, 0.12)' : 'transparent',
                  color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
                  border: isActive ? '1px solid rgba(99, 102, 241, 0.3)' : '1px solid var(--border-color)',
                  padding: '6px 12px',
                  borderRadius: '6px',
                  fontSize: '0.82rem',
                  fontWeight: 600
                }}
                className={isActive ? '' : 'glass-panel-interactive'}
              >
                {lvl}
              </button>
            );
          })}
        </div>

      </div>

      {/* Terminal logs list */}
      <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px', marginBottom: '8px' }}>
          <Terminal size={18} style={{ color: 'var(--color-primary)' }} />
          <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>System Execution Streams</h3>
          <button 
            onClick={() => setLogs([])}
            style={{ marginLeft: 'auto', fontSize: '0.8rem', color: 'var(--text-muted)', background: 'transparent' }}
          >
            Clear Terminal
          </button>
        </div>

        <div style={{
          background: 'rgba(0, 0, 0, 0.35)',
          border: '1px solid var(--border-color)',
          borderRadius: '10px',
          padding: '16px',
          fontFamily: 'var(--font-mono)',
          fontSize: '0.85rem',
          lineHeight: 1.6,
          maxHeight: '400px',
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px'
        }}>
          {filteredLogs.length > 0 ? (
            filteredLogs.map(log => (
              <div key={log.id} style={{ display: 'flex', gap: '12px', alignItems: 'start' }}>
                <span style={{ color: 'var(--text-muted)' }}>[{log.timestamp}]</span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: getLevelColor(log.level), fontWeight: 600 }}>
                  {getLevelIcon(log.level)}
                  {log.level}
                </span>
                <span style={{ color: 'var(--color-secondary)', fontWeight: 500 }}>[{log.category}]</span>
                <span style={{ color: '#d1d5db', flex: 1 }}>{log.message}</span>
              </div>
            ))
          ) : (
            <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px' }}>
              No log messages matching search criteria.
            </div>
          )}
        </div>

      </div>

    </div>
  );
};
