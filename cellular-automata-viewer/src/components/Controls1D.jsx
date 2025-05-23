// Content for components/Controls1D.jsx
import React, { useState, useEffect, useCallback } from 'react'; // Added useEffect
// Optional: import a shared CSS module if styles are very similar to Controls.jsx
// import styles from './Controls.module.css'; 

const Controls1D = ({ onStart, onPause, onReset, onRuleChange, currentRule, isRunning }) => {
  const [ruleInputValue, setRuleInputValue] = useState(currentRule.toString());

  useEffect(() => { // Keep input in sync if currentRule prop changes from App.jsx
    setRuleInputValue(currentRule.toString());
  }, [currentRule]);

  const handleRuleInputChange = useCallback((event) => {
    const value = event.target.value;
    setRuleInputValue(value);
    const numericValue = parseInt(value, 10);
    if (!isNaN(numericValue) && numericValue >= 0 && numericValue <= 255) {
      if (onRuleChange) onRuleChange(numericValue);
    } else if (value === '') {
      // Allow empty input, maybe default to rule 0 or keep last valid
      if (onRuleChange) onRuleChange(0); // Or some other default
    }
  }, [onRuleChange]);
  
  // Basic inline styles or use a CSS module
  const controlStyles = {
    controlsContainer: {
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      padding: '10px',
      marginBottom: '20px',
      flexWrap: 'wrap', // Allow controls to wrap on smaller screens
      justifyContent: 'center',
    },
    label: { marginRight: '5px' },
    input: { 
      width: '60px', 
      padding: '8px',
      border: '1px solid #ccc',
      borderRadius: '4px',
    },
    button: {
      padding: '8px 15px',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      backgroundColor: '#007bff',
      color: 'white',
    },
    buttonDisabled: {
      backgroundColor: '#6c757d',
    },
    ruleText: {
        marginLeft: '10px',
        fontSize: '0.9em',
        color: '#555',
    }
  };

  return (
    <div style={controlStyles.controlsContainer}>
      <label htmlFor="ruleNumber" style={controlStyles.label}>Rule:</label>
      <input
        type="number"
        id="ruleNumber"
        value={ruleInputValue}
        onChange={handleRuleInputChange}
        min="0"
        max="255"
        style={controlStyles.input}
        disabled={isRunning}
      />
      <button onClick={onStart} disabled={isRunning} style={{...controlStyles.button, ...(isRunning && controlStyles.buttonDisabled)}}>Start</button>
      <button onClick={onPause} disabled={!isRunning} style={{...controlStyles.button, ...(!isRunning && controlStyles.buttonDisabled)}}>Pause</button>
      <button onClick={onReset} style={controlStyles.button}>Reset</button>
      {/* <span style={controlStyles.ruleText}>Current Rule: {currentRule}</span> */}
    </div>
  );
};

export default Controls1D;
