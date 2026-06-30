import React from 'react';
import { LayoutDashboard, FileText, Play, Activity, ToggleLeft, ToggleRight, Download, Terminal, Settings, X } from 'lucide-react';

interface SidebarProps {
  currentPage: string;
  setCurrentPage: (page: string) => void;
  mockMode: boolean;
  setMockMode: (mode: boolean) => void;
  isOpen?: boolean;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  currentPage, 
  setCurrentPage, 
  mockMode, 
  setMockMode,
  isOpen = false,
  onClose
}) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'proposals', label: 'Proposals', icon: FileText },
    { id: 'simulator', label: 'Assessment Sandbox', icon: Play },
    { id: 'reports', label: 'Reports & Exports', icon: Download },
    { id: 'logs', label: 'Audit Logs', icon: Terminal },
    { id: 'settings', label: 'Settings', icon: Settings },
    { id: 'system', label: 'System Diagnostics', icon: Activity },
  ];

  return (
    <aside className={`glass-panel responsive-sidebar ${isOpen ? 'open' : ''}`} style={{
      width: '260px',
      height: 'calc(100vh - 32px)',
      margin: '16px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      padding: '24px 16px',
      position: 'sticky',
      top: '16px',
      zIndex: 100
    }}>
      <div>
        {/* Brand Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 8px 32px 8px', borderBottom: '1px solid var(--border-color)', marginBottom: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: 'linear-gradient(135deg, var(--color-primary), var(--color-secondary))',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 700,
              fontSize: '1.2rem',
              color: 'white',
              boxShadow: '0 0 16px rgba(99, 102, 241, 0.4)'
            }}>
              Ω
            </div>
            <div>
              <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.02em', margin: 0 }}>
                Antigravity
              </h2>
              <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
                Risk Engine UI
              </span>
            </div>
          </div>
          
          {/* Mobile close button */}
          <button 
            onClick={onClose} 
            className="mobile-close-btn"
            aria-label="Close sidebar navigation menu"
          >
            <X size={16} />
          </button>
        </div>
 
        {/* Menu Items */}
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {menuItems.map(item => {
            const Icon = item.icon;
            const isActive = currentPage === item.id || (item.id === 'proposals' && currentPage === 'detail');
            
            return (
              <button
                key={item.id}
                onClick={() => setCurrentPage(item.id)}
                aria-label={`Navigate to ${item.label} section`}
                aria-current={isActive ? 'page' : undefined}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  width: '100%',
                  padding: '12px 16px',
                  borderRadius: '10px',
                  fontSize: '0.95rem',
                  textAlign: 'left',
                  background: isActive ? 'rgba(99, 102, 241, 0.12)' : 'transparent',
                  color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
                  border: isActive ? '1px solid rgba(99, 102, 241, 0.25)' : '1px solid transparent',
                  transition: 'all var(--transition-fast)'
                }}
                className={isActive ? '' : 'glass-panel-interactive'}
              >
                <Icon size={18} style={{ color: isActive ? 'var(--color-primary)' : 'inherit' }} />
                <span style={{ fontWeight: isActive ? 600 : 500 }}>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
 
      {/* Connection Mode Controls */}
      <div style={{
        padding: '16px',
        borderRadius: '12px',
        background: 'rgba(0, 0, 0, 0.2)',
        border: '1px solid var(--border-color)',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
            Mock Fallback
          </span>
          <button 
            onClick={() => setMockMode(!mockMode)}
            aria-label="Toggle mock fallback dataset mode"
            aria-pressed={mockMode}
            style={{ background: 'transparent', display: 'flex', alignItems: 'center' }}
          >
            {mockMode ? (
              <ToggleRight size={36} className="text-primary" style={{ color: 'var(--color-primary)' }} />
            ) : (
              <ToggleLeft size={36} style={{ color: 'var(--text-muted)' }} />
            )}
          </button>
        </div>
        <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', lineHeight: 1.3 }}>
          {mockMode 
            ? 'Forced Standalone Mode. Using high-fidelity local datasets.' 
            : 'Live API Mode. Fetching live database & running real LLM prompts.'}
        </span>
      </div>
    </aside>
  );
};
