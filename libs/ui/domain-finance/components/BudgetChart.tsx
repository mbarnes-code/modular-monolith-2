import React from 'react';

interface BudgetData {
  category: string;
  amount: number;
  budget: number;
}

interface BudgetChartProps {
  data: BudgetData[];
}

export const BudgetChart: React.FC<BudgetChartProps> = ({ data }) => {
  return (
    <div style={{ padding: '16px' }}>
      <h3>Budget Overview</h3>
      {data.map((item, idx) => {
        const percentage = (item.amount / item.budget) * 100;
        return (
          <div key={idx} style={{ marginBottom: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
              <span>{item.category}</span>
              <span>
                ${item.amount.toFixed(2)} / ${item.budget.toFixed(2)}
              </span>
            </div>
            <div style={{ width: '100%', height: '20px', backgroundColor: '#e0e0e0', borderRadius: '4px' }}>
              <div
                style={{
                  width: `${Math.min(percentage, 100)}%`,
                  height: '100%',
                  backgroundColor: percentage > 100 ? '#f44336' : '#4caf50',
                  borderRadius: '4px',
                }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};
