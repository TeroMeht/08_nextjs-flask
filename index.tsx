import React, { useState, useEffect } from 'react';
import FormComponent from '../ui/formComponent'; // Adjust import path as necessary
import BarChart from '../ui/barChartComponent';  // Import the BarChart component
import PositionTable from '../ui/tableComponent';

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

function App() {
  const [positions, setPositions] = useState<Position[]>([]);
  const [message, setMessage] = useState<string>('');
  const symbols = positions.map((position: Position) => position.symbol);
  const allocations = positions.map((position: Position) => position.allocation);

  useEffect(() => {
    fetch('http://localhost:8080/api/home')
      .then((response) => response.json())
      .then((data) => {
        setPositions(data.data);
        console.log('Fetched data:', data.data);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setMessage('Error loading data');
      });
  }, []);

  const handleFormSubmit = (formData: any) => {
    // Your form submission logic here
  };

  // Flexbox container for PositionTable and BarChart
  const tableAndChartContainerStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'flex-start', // Align both items to the top
    gap: '20px', // Space between the table and chart
    marginTop: '20px',
    overflow: 'auto',
  };

  const tableContainerStyle: React.CSSProperties = {
    flex: 1, // Table takes available space
    minWidth: '300px', // Ensure table has a minimum width
  };

  const chartContainerStyle: React.CSSProperties = {
    flex: 1, // Chart takes available space
    minWidth: '200px', // Ensure chart has a minimum width
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  };

  return (
    <div className="App">
      <div style={{ textAlign: 'center', fontSize: '2rem', fontWeight: 'bold', margin: '20px 0' }}>
        Investment Overview
      </div>
      {positions.length > 0 ? (
        <div>
          {/* PositionTable and BarChart side by side */}
          <div style={tableAndChartContainerStyle}>
            {/* PositionTable container */}
            <div style={tableContainerStyle}>
            <div style={{ textAlign: 'center', marginBottom: '10px' }}>
                Portfolio
              </div>
              <PositionTable positions={positions} />
            </div>

            {/* BarChart container */}
            <div style={chartContainerStyle}>
              <div style={{ textAlign: 'center', marginBottom: '10px' }}>
                Allocation vs. Ticker
              </div>
              <BarChart symbols={symbols} allocations={allocations} />
            </div>
          </div>

          {/* FormComponent container */}
          <div style={{ marginTop: '10px' }}>
            <FormComponent onSubmit={handleFormSubmit} />
          </div>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;