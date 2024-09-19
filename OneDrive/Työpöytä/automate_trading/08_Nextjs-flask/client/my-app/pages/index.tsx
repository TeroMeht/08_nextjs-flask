import React from 'react';
import FormComponent from '../ui/formComponent'; // Adjust import path as necessary
import BarChart from '../ui/barChartComponent';  // Import the BarChart component
import PositionTable from '../ui/tableComponent'; // Adjust import path as necessary

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
  const [positions, setPositions] = React.useState<Position[]>([]);
  const [symbols, setSymbols] = React.useState<string[]>([]);
  const [allocations, setAllocations] = React.useState<number[]>([]);

  const handleDataFetched = (data: Position[]) => {
    setPositions(data);

    // Update symbols and allocations based on fetched data
    const fetchedSymbols = data.map((position: Position) => position.symbol);
    const fetchedAllocations = data.map((position: Position) => position.allocation);

    setSymbols(fetchedSymbols);
    setAllocations(fetchedAllocations);
  };

  const handleFormSubmit = (formData: any) => {
    // Your form submission logic here
  };

  return (
    <div className="App">
      <div style={{ textAlign: 'center', fontSize: '2rem', fontWeight: 'bold', margin: '20px 0' }}>
        Investment Overview
      </div>
      <PositionTable onDataFetched={handleDataFetched} />

      {positions.length > 0 ? (
        <div>
          {/* PositionTable and BarChart side by side */}
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '20px', marginTop: '20px', overflow: 'auto' }}>
            {/* BarChart container */}
            <div style={{ flex: 1, minWidth: '200px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
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
