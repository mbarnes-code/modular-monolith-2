import React from 'react';

interface ThreatIndicatorProps {
  level: 'low' | 'medium' | 'high' | 'critical';
  label?: string;
}

const colorMap = {
  low: '#4caf50',
  medium: '#ff9800',
  high: '#f44336',
  critical: '#b71c1c',
};

export const ThreatIndicator: React.FC<ThreatIndicatorProps> = ({ level, label }) => {
  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
      <div
        style={{
          width: '12px',
          height: '12px',
          borderRadius: '50%',
          backgroundColor: colorMap[level],
        }}
      />
      <span style={{ textTransform: 'uppercase', fontSize: '12px', fontWeight: 'bold' }}>
        {label || level}
      </span>
    </div>
  );
};
