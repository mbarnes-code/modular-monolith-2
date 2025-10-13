import React from 'react';

interface IOCDisplayProps {
  type: 'ip' | 'domain' | 'hash' | 'email' | 'url';
  value: string;
  onCopy?: () => void;
}

export const IOCDisplay: React.FC<IOCDisplayProps> = ({ type, value, onCopy }) => {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        padding: '8px',
        backgroundColor: '#f5f5f5',
        borderRadius: '4px',
        fontFamily: 'monospace',
      }}
    >
      <span style={{ fontSize: '10px', color: '#666', textTransform: 'uppercase' }}>{type}</span>
      <code style={{ flex: 1 }}>{value}</code>
      {onCopy && (
        <button onClick={onCopy} style={{ padding: '4px 8px', cursor: 'pointer' }}>
          Copy
        </button>
      )}
    </div>
  );
};
