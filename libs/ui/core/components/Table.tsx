import React from 'react';

interface TableColumn {
  key: string;
  header: string;
  render?: (value: any, row: any) => React.ReactNode;
}

interface TableProps {
  columns: TableColumn[];
  data: any[];
}

export const Table: React.FC<TableProps> = ({ columns, data }) => {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr>
          {columns.map((col) => (
            <th
              key={col.key}
              style={{
                padding: '12px',
                borderBottom: '2px solid #e0e0e0',
                textAlign: 'left',
                fontWeight: 'bold',
              }}
            >
              {col.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, idx) => (
          <tr key={idx}>
            {columns.map((col) => (
              <td
                key={col.key}
                style={{
                  padding: '12px',
                  borderBottom: '1px solid #e0e0e0',
                }}
              >
                {col.render ? col.render(row[col.key], row) : row[col.key]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};
