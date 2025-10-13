import React from 'react';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  className?: string;
}

export const Card: React.FC<CardProps> = ({ children, title, className }) => {
  return (
    <div
      className={className}
      style={{
        border: '1px solid #e0e0e0',
        borderRadius: '8px',
        padding: '16px',
        backgroundColor: 'white',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      }}
    >
      {title && <h3 style={{ marginTop: 0, marginBottom: '16px' }}>{title}</h3>}
      {children}
    </div>
  );
};
