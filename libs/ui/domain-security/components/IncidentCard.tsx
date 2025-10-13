import React from 'react';

interface IncidentCardProps {
  title: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  timestamp: string;
  description: string;
  status?: 'open' | 'investigating' | 'resolved';
}

export const IncidentCard: React.FC<IncidentCardProps> = ({
  title,
  severity,
  timestamp,
  description,
  status = 'open',
}) => {
  return (
    <div
      style={{
        border: '1px solid #ddd',
        borderRadius: '8px',
        padding: '16px',
        marginBottom: '8px',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <h3 style={{ margin: 0 }}>{title}</h3>
        <span
          style={{
            padding: '2px 8px',
            borderRadius: '4px',
            fontSize: '12px',
            textTransform: 'uppercase',
          }}
        >
          {status}
        </span>
      </div>
      <div style={{ fontSize: '12px', color: '#666', marginBottom: '8px' }}>{timestamp}</div>
      <div style={{ marginBottom: '8px' }}>
        <strong>Severity:</strong> {severity}
      </div>
      <p style={{ margin: 0 }}>{description}</p>
    </div>
  );
};
