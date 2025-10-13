import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({ children, onClick }) => {
  return (
    <button onClick={onClick} style={{ padding: '8px 16px', cursor: 'pointer' }}>
      {children}
    </button>
  );
};
