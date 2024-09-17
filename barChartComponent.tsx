// BarChart.tsx
import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

// Register components for Chart.js
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface BarChartProps {
  symbols: string[];
  allocations: number[];
}

const BarChart: React.FC<BarChartProps> = ({ symbols, allocations }) => {
  // Define background and border colors for each symbol
  const backgroundColors = symbols.map(symbol =>
    symbol.toLowerCase() === 'cash' ? 'rgba(0, 255, 0, 0.6)' : 'rgba(0, 123, 255, 0.6)'
  );

  const borderColors = symbols.map(symbol =>
    symbol.toLowerCase() === 'cash' ? 'rgba(0, 255, 0, 1)' : 'rgba(0, 123, 255, 1)'
  );

  const chartData = {
    labels: symbols,
    datasets: [
      {
        label: 'Allocation',
        data: allocations,
        backgroundColor: backgroundColors, // Individual colors based on symbol
        borderColor: borderColors, // Individual border colors based on symbol
        borderWidth: 1,
      },
    ],
  };
  const chartOptions = {
    plugins: {
        legend: {
          display: false, // Hide the legend
        },
        title: {
          display: false, // Optionally hide the title
        },
      },
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };
  // Inline styles for the chart container
  const chartContainerStyle: React.CSSProperties = {
    width: '90%', // Full width
    height: '500px', // Fixed height
    padding: '20px', // Padding around the chart
    boxSizing: 'border-box', // Ensure padding is included in the width/height calculation
  };
  

  return (
    <div style={chartContainerStyle}>
      <Bar data={chartData} options={chartOptions} />
    </div>
  );
};


export default BarChart;
