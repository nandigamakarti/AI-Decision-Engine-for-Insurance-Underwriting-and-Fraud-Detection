import React from 'react';
import { ShieldCheck, ShieldAlert, Cpu, Sun, Moon, Menu } from 'lucide-react';
import { SystemHealth } from '../types';
import { useTheme } from '../hooks/useTheme';

interface HeaderProps {
  currentPage: string;
  systemHealth: SystemHealth | null;
  mockMode: boolean;
  onMenuToggle?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ 
  currentPage, 
  systemHealth, 
  mockMode,
  onMenuToggle
}) => {
  const { theme, toggleTheme } = useTheme();
  const getPageTitle = () => {
    switch (currentPage) {
      case 'dashboard': return 'Dashboard Overview';
      case 'proposals': return 'Insurance Proposals';
      case 'detail': return 'Underwriting Risk Analysis';
      case 'simulator': return 'AI Risk Sandbox';
      case 'reports': return 'Reports & Exports';
      case 'logs': return 'Audit Logs Console';
      case 'settings': return 'System Configurations';
      case 'system': return 'System Diagnostics';
      default: return 'Risk Engine';
    }
  };

  // Determine global connection status
  const isOnline = systemHealth && 
                   systemHealth.api.status === 'healthy' && 
                   systemHealth.db.status === 'healthy' && 
                   !mockMode;

  return (
    <header className="glass-panel" style={{
      padding: '16px 28px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      margin: '16px 16px 0 0',
      height: '70px',
      zIndex: 5
    }}>
      {/* Title & Mobile Toggle */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <button 
          onClick={onMenuToggle}
          className="sidebar-toggle-btn"
          aria-label="Open sidebar navigation menu"
        >
          <Menu size={18} />
        </button>
        <h1 style={{ fontSize: '1.4rem', fontWeight: 700, letterSpacing: '-0.02em', color: 'var(--text-primary)', margin: 0 }}>
          {getPageTitle()}
        </h1>
      </div>

      {/* Global Status Indicators */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {/* Model info */}
        {systemHealth?.ollama.status === 'healthy' && !mockMode && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            background: 'rgba(99, 102, 241, 0.08)',
            border: '1px solid rgba(99, 102, 241, 0.2)',
            padding: '6px 14px',
            borderRadius: '8px',
            fontSize: '0.85rem'
          }}>
            <Cpu size={14} style={{ color: 'var(--color-primary)' }} />
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>
              AI Model: <strong style={{ color: 'var(--text-primary)' }}>{systemHealth.ollama.model}</strong>
            </span>
          </div>
        )}

        {/* Theme Toggle Button */}
        <button
          onClick={toggleTheme}
          aria-label={theme === 'dark' ? 'Switch to light visual theme' : 'Switch to dark visual theme'}
          style={{
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid var(--border-color)',
            color: 'var(--text-primary)',
            padding: '8px',
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'background var(--transition-fast)'
          }}
          className="hover:bg-white/10"
          title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
        </button>

        {/* Health status pill */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          background: isOnline ? 'rgba(16, 185, 129, 0.08)' : 'rgba(249, 115, 22, 0.08)',
          border: isOnline ? '1px solid rgba(16, 185, 129, 0.2)' : '1px solid rgba(249, 115, 22, 0.2)',
          padding: '6px 14px',
          borderRadius: '8px',
          fontSize: '0.85rem',
          fontWeight: 600
        }}>
          <span className={`pulse-indicator ${isOnline ? 'pulse-low' : 'pulse-high'}`} />
          <span style={{ color: isOnline ? 'var(--color-low)' : 'var(--color-high)' }}>
            {isOnline ? 'LIVE API ONLINE' : mockMode ? 'SANDBOX STANDALONE' : 'OFFLINE FALLBACK'}
          </span>
          {isOnline ? (
            <ShieldCheck size={16} style={{ color: 'var(--color-low)' }} />
          ) : (
            <ShieldAlert size={16} style={{ color: 'var(--color-high)' }} />
          )}
        </div>
      </div>
    </header>
  );
};
