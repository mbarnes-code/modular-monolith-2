import React from 'react';

interface ColorIdentityBadgeProps {
  colors: string[]; // e.g., ['W', 'U', 'B', 'R', 'G']
}

export const ColorIdentityBadge: React.FC<ColorIdentityBadgeProps> = ({ colors }) => {
  return (
    <div style={{ display: 'flex', gap: '4px', alignItems: 'center' }}>
      {colors.length === 0 ? (
        <span style={{ fontSize: '12px', color: '#666' }}>Colorless</span>
      ) : (
        colors.map((color, idx) => (
          <span
            key={idx}
            style={{
              width: '20px',
              height: '20px',
              borderRadius: '50%',
              display: 'inline-block',
              border: '1px solid #000',
            }}
            title={color}
          />
        ))
      )}
    </div>
  );
};
