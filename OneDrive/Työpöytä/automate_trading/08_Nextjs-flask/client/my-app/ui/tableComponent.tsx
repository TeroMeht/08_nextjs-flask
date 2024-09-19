import React, { useState, useEffect } from 'react';

interface Position {
  allocation: number;
  symbol: string;
  quantity: number;
  open_date: string;
  avg_cost: number;
  value: number;
  current_price: number;
  change: number;
}

interface PositionTableProps {
  onDataFetched: (data: Position[]) => void; // Callback to send data to App
}

const PositionTable: React.FC<PositionTableProps> = ({ onDataFetched }) => {
  const [positions, setPositions] = useState<Position[]>([]);
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    fetch('http://localhost:8080/api/home')
      .then((response) => response.json())
      .then((data) => {
        setPositions(data.data);
        console.log('Fetched data:', data.data);

        // Notify App component with fetched data
        onDataFetched(data.data);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setMessage('Error loading data');
      });
  }, []);

  const modernTableStyle: React.CSSProperties = {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '10px',
    boxShadow: '0 4px 4px rgba(0, 0, 0, 0.1)',
    borderRadius: '8px',
    overflow: 'hidden',
  };

  const modernThStyle: React.CSSProperties = {
    padding: '8px 10px',
    textAlign: 'left',
    backgroundColor: '#4CAF50',  // A modern green header
    color: '#fff',
    fontWeight: 'bold',
    textTransform: 'uppercase',
  };

  const modernTdStyle: React.CSSProperties = {
    padding: '8px 10px',
    borderBottom: '1px solid #ddd',
    color: '#333',
  };

  const modernEvenRowStyle: React.CSSProperties = {
    backgroundColor: '#f9f9f9',  // Light gray background for even rows
  };

  const modernOddRowStyle: React.CSSProperties = {
    backgroundColor: '#fff',  // White background for odd rows
  };

  return (
    <table style={modernTableStyle}>
      <thead>
        <tr>
          <th style={modernThStyle}>#</th> {/* New column header for row number */}
          <th style={modernThStyle}>Allocation</th>
          <th style={modernThStyle}>Symbol</th>
          <th style={modernThStyle}>Quantity</th>
          <th style={modernThStyle}>Open Date</th>
          <th style={modernThStyle}>Avg Cost</th>
          <th style={modernThStyle}>Value</th>
          <th style={modernThStyle}>Current Price</th>
          <th style={modernThStyle}>Change</th>
        </tr>
      </thead>
      <tbody>
        {positions.map((position: Position, index: number) => (
          <tr
            key={index}
            style={index % 2 === 0 ? modernEvenRowStyle : modernOddRowStyle}
          >
            <td style={modernTdStyle}>{index + 1}</td> {/* Row number */}
            {/* Apply bold style to allocation column */}
            <td style={{ ...modernTdStyle, fontWeight: 'bold' }}>
              {position.allocation} %
            </td>
            <td style={modernTdStyle}>{position.symbol}</td>
            <td style={modernTdStyle}>{position.quantity}</td>
            <td style={modernTdStyle}>{position.open_date}</td>
            <td style={modernTdStyle}>{position.avg_cost}</td>
            <td style={modernTdStyle}>{position.value}</td>
            <td style={modernTdStyle}>{position.current_price}</td>
            {/* Conditional color styling for change */}
            <td
              style={{
                ...modernTdStyle,
                color: position.change < 0 ? 'red' : 'green',
              }}
            >
              {position.change} %
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default PositionTable;
