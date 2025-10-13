import React from 'react';

interface ComboCardProps {
  comboName: string;
  cards: string[];
  description: string;
}

export const ComboCard: React.FC<ComboCardProps> = ({ comboName, cards, description }) => {
  return (
    <div
      style={{
        border: '1px solid #ddd',
        borderRadius: '8px',
        padding: '16px',
        margin: '8px 0',
      }}
    >
      <h3 style={{ marginTop: 0 }}>{comboName}</h3>
      <div style={{ marginBottom: '8px' }}>
        <strong>Cards:</strong> {cards.join(', ')}
      </div>
      <p style={{ marginBottom: 0 }}>{description}</p>
    </div>
  );
};
