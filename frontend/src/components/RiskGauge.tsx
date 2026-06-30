import React from 'react';

interface RiskGaugeProps {
  score: number;
  level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  title: string;
  size?: number;
}

export const RiskGauge: React.FC<RiskGaugeProps> = ({ score, level, title, size = 180 }) => {
  // Map level to corresponding color variables
  const colorMap = {
    LOW: 'var(--color-low)',
    MEDIUM: 'var(--color-medium)',
    HIGH: 'var(--color-high)',
    CRITICAL: 'var(--color-critical)'
  };
  
  const activeColor = colorMap[level] || 'var(--color-primary)';
  
  // SVG Calculations for semi-circle gauge
  const radius = 50;
  const strokeWidth = 10;
  const circumference = Math.PI * radius; // 157.08
  const strokeDashoffset = circumference - (Math.min(100, Math.max(0, score)) / 100) * circumference;
  
  return (
    <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative', overflow: 'hidden' }}>
      <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '16px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{title}</h3>
      
      <div style={{ position: 'relative', width: `${size}px`, height: `${size / 1.6}px` }}>
        <svg viewBox="0 0 120 70" style={{ width: '100%', height: '100%' }}>
          {/* Background Arc */}
          <path
            d="M 10 60 A 50 50 0 0 1 110 60"
            fill="none"
            stroke="rgba(255, 255, 255, 0.05)"
            strokeWidth={strokeWidth}
            strokeLinecap="round"
          />
          
          {/* Filled Arc */}
          <path
            d="M 10 60 A 50 50 0 0 1 110 60"
            fill="none"
            stroke={activeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 1s ease-in-out, stroke 0.5s ease' }}
          />
          
          {/* Needle Center Pin */}
          <circle cx="60" cy="60" r="4" fill="var(--text-primary)" />
        </svg>
        
        {/* Score Display Overlay */}
        <div style={{
          position: 'absolute',
          bottom: '0',
          left: '50%',
          transform: 'translateX(-50%)',
          textAlign: 'center'
        }}>
          <span style={{ fontSize: '2.2rem', fontWeight: 700, color: 'var(--text-primary)', display: 'block', lineHeight: 1 }}>
            {score.toFixed(1)}
          </span>
          <span className={`badge badge-${level.toLowerCase()}`} style={{ marginTop: '8px' }}>
            {level}
          </span>
        </div>
      </div>
      
      {/* Background Gradient Accent Glow */}
      <div style={{
        position: 'absolute',
        bottom: '-30px',
        width: '120px',
        height: '120px',
        borderRadius: '50%',
        background: activeColor,
        opacity: 0.08,
        filter: 'blur(30px)',
        pointerEvents: 'none'
      }} />
    </div>
  );
};
