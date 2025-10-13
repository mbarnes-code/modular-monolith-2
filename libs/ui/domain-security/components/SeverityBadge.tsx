import React from 'react';

interface SeverityBadgeProps {
  severity: 'info' | 'warning' | 'error' | 'critical';
  text?: string;
}

const styleMap = {
  info: { bg: '#2196f3', color: '#fff' },
  warning: { bg: '#ff9800', color: '#fff' },
  error: { bg: '#f44336', color: '#fff' },
  critical: { bg: '#b71c1c', color: '#fff' },
};

export const SeverityBadge: React.FC<SeverityBadgeProps> = ({ severity, text }) => {
  const style = styleMap[severity];
  return (
    <span
      style={{
        padding: '4px 12px',
        borderRadius: '12px',
        backgroundColor: style.bg,
        color: style.color,
        fontSize: '12px',
        fontWeight: 'bold',
        textTransform: 'uppercase',
      }}
    >
      {text || severity}
    </span>
  );
};
