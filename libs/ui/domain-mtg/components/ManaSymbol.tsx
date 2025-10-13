import React from 'react';

interface ManaSymbolProps {
  symbol: string; // e.g., 'W', 'U', 'B', 'R', 'G', '1', '2', etc.
  size?: number;
}

const colorMap: Record<string, string> = {
  W: '#f8f6d8',
  U: '#0e68ab',
  B: '#150b00',
  R: '#d3202a',
  G: '#00733e',
};

export const ManaSymbol: React.FC<ManaSymbolProps> = ({ symbol, size = 24 }) => {
  const bgColor = colorMap[symbol] || '#ccc';
  return (
    <span
      style={{
        display: 'inline-block',
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: bgColor,
        color: symbol === 'W' || symbol === 'Y' ? '#000' : '#fff',
        textAlign: 'center',
        lineHeight: `${size}px`,
        fontSize: size * 0.6,
        fontWeight: 'bold',
        border: '2px solid #000',
      }}
    >
      {symbol}
    </span>
  );
};
