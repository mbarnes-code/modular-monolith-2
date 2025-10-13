import React from 'react';

interface Transaction {
  id: string;
  date: string;
  description: string;
  amount: number;
  category: string;
}

interface TransactionListProps {
  transactions: Transaction[];
}

export const TransactionList: React.FC<TransactionListProps> = ({ transactions }) => {
  return (
    <div style={{ padding: '16px' }}>
      <h3>Recent Transactions</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left', padding: '8px', borderBottom: '2px solid #ddd' }}>Date</th>
            <th style={{ textAlign: 'left', padding: '8px', borderBottom: '2px solid #ddd' }}>Description</th>
            <th style={{ textAlign: 'left', padding: '8px', borderBottom: '2px solid #ddd' }}>Category</th>
            <th style={{ textAlign: 'right', padding: '8px', borderBottom: '2px solid #ddd' }}>Amount</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx) => (
            <tr key={tx.id}>
              <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>{tx.date}</td>
              <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>{tx.description}</td>
              <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>{tx.category}</td>
              <td
                style={{
                  padding: '8px',
                  borderBottom: '1px solid #ddd',
                  textAlign: 'right',
                  color: tx.amount < 0 ? '#f44336' : '#4caf50',
                }}
              >
                ${Math.abs(tx.amount).toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
