import React, { useState } from 'react';

// Define props type for FormComponent
interface FormComponentProps {
  onSubmit: (formData: any) => void;
}

const FormComponent: React.FC<FormComponentProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    symbol: '',
    quantity: 0,
    price: 0,
    selectedOption: '' // Added to store selected radio button value
  });
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState<'success' | 'error'>('success');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;

    // Handle input change based on type and name
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: type === 'radio' ? value : type === 'number' ? parseFloat(value) : value,
      selectedOption: type === 'radio' ? (checked ? value : prevFormData.selectedOption) : prevFormData.selectedOption
    }));
  };

  // Handle form submission to POST new data to the backend
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();


    // Check if selectedOption is not empty
    if (!formData.selectedOption) {
        setMessage('Please select an option.');
        setMessageType('error');
        return; // Exit the function if validation fails
        }
    // Log the form data to see what will be sent
    console.log('Submitting the following data:', formData);

    fetch('http://localhost:8080/api/positions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData), // Send the form data as JSON
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status === 'success') {
            setMessage('Data Submitted Successfully');
            setMessageType('success');
            onSubmit(formData); // Notify parent component
        } else {
            setMessage(`Failed to submit data: ${data.message}`);
            setMessageType('error');
        }
    })
    .catch((error) => {
        console.error('Error submitting data:', error);
        setMessage('Error submitting data');
        setMessageType('error');
    });
};

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <h3 style={headingStyle}>Select an option:</h3>

      <div style={radioContainerStyle}>
        {['Add', 'Trim', 'Exit', 'Entry'].map(option => (
          <label key={option} style={radioLabelStyle}>
            <input
              type="radio"
              name="options"
              value={option}
              checked={formData.selectedOption === option}
              onChange={handleInputChange}
              style={radioInputStyle}
            />
            {option}
          </label>
        ))}
      </div>

      <div style={inputGroupStyle}>
        <label style={labelStyle}>
          Symbol:
          <input
            type="text"
            name="symbol"
            value={formData.symbol}
            onChange={handleInputChange}
            style={inputStyle}
          />
        </label>
      </div>

      <div style={inputGroupStyle}>
        <label style={labelStyle}>
          Quantity:
          <input
            type="number"
            name="quantity"
            value={formData.quantity}
            onChange={handleInputChange}
            style={inputStyle}
          />
        </label>
      </div>

      <div style={inputGroupStyle}>
        <label style={labelStyle}>
          Price:
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleInputChange}
            style={inputStyle}
          />
        </label>
      </div>

      <button type="submit" style={buttonStyle}>Submit</button>
      <p style={{ ...messageStyle, color: messageType === 'success' ? 'green' : 'red' }}>{message}</p>
    </form>
  );
};

// Style objects
const formStyle: React.CSSProperties = {
  maxWidth: '300px',
  marginLeft: '20px',
  padding: '20px',
  borderRadius: '8px',
  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  backgroundColor: '#fff',
};

const headingStyle: React.CSSProperties = {
  fontSize: '1.5rem',
  marginBottom: '10px',
  color: '#333',
};

const radioContainerStyle: React.CSSProperties = {
  display: 'flex',
  gap: '15px',
  marginBottom: '20px',
};

const radioLabelStyle: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  fontSize: '1rem',
};

const radioInputStyle: React.CSSProperties = {
  marginRight: '8px',
};

const inputGroupStyle: React.CSSProperties = {
  marginBottom: '15px',
};

const labelStyle: React.CSSProperties = {
  display: 'block',
  marginBottom: '5px',
  fontSize: '1rem',
  color: '#555',
};

const inputStyle: React.CSSProperties = {
  width: '100%',
  padding: '10px',
  border: '1px solid #ddd',
  borderRadius: '4px',
  fontSize: '1rem',
};

const buttonStyle: React.CSSProperties = {
  display: 'block',
  width: '100%',
  padding: '10px',
  border: 'none',
  borderRadius: '4px',
  backgroundColor: '#007BFF',
  color: '#fff',
  fontSize: '1rem',
  cursor: 'pointer',
  transition: 'background-color 0.3s',
};

const messageStyle: React.CSSProperties = {
  marginTop: '15px',
  fontSize: '1rem',
};

export default FormComponent;
