import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({ label, error, ...props }) => {
  return (
    <div style={{ marginBottom: '16px' }}>
      {label && <label style={{ display: 'block', marginBottom: '4px' }}>{label}</label>}
      <input
        {...props}
        style={{
          padding: '8px',
          border: '1px solid #ccc',
          borderRadius: '4px',
          width: '100%',
          ...props.style,
        }}
      />
      {error && <span style={{ color: 'red', fontSize: '12px' }}>{error}</span>}
    </div>
  );
};
