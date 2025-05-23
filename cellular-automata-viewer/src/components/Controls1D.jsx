// Content for components/Controls1D.jsx
import React, { useState, useEffect, useCallback } from 'react';

const Controls1D = ({ onStart, onPause, onReset, onRuleChange, currentRule, isRunning }) => {
  const [ruleInputValue, setRuleInputValue] = useState(currentRule.toString());

  useEffect(() => {
    setRuleInputValue(currentRule.toString());
  }, [currentRule]);

  const handleRuleInputChangeInternal = useCallback((event) => {
    const value = event.target.value;
    setRuleInputValue(value);
    const numericValue = parseInt(value, 10);
    if (!isNaN(numericValue) && numericValue >= 0 && numericValue <= 255) {
      if (onRuleChange) onRuleChange(numericValue);
    } else if (value === '') {
      if (onRuleChange) onRuleChange(0); 
    }
  }, [onRuleChange]);
  
  const controlStyles = { /* ... (styles as defined in previous restore step) ... */ 
    controlsContainer: { display: 'flex', alignItems: 'center', gap: '10px', padding: '10px', marginBottom: '20px', flexWrap: 'wrap', justifyContent: 'center' },
    label: { marginRight: '5px' },
    input: { width: '60px', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' },
    button: { padding: '8px 15px', border: 'none', borderRadius: '4px', cursor: 'pointer', backgroundColor: '#007bff', color: 'white' },
    buttonDisabled: { backgroundColor: '#6c757d' }
  };

  return (
    <div style={controlStyles.controlsContainer}>
      <label htmlFor="ruleNumber" style={controlStyles.label}>Rule:</label>
      <input type="number" id="ruleNumber" value={ruleInputValue} onChange={handleRuleInputChangeInternal} min="0" max="255" style={controlStyles.input} disabled={isRunning} />
      <button onClick={onStart} disabled={isRunning} style={{...controlStyles.button, ...(isRunning && controlStyles.buttonDisabled)}}>Start</button>
      <button onClick={onPause} disabled={!isRunning} style={{...controlStyles.button, ...(!isRunning && controlStyles.buttonDisabled)}}>Pause</button>
      <button onClick={onReset} style={controlStyles.button}>Reset</button>
    </div>
  );
};
export default Controls1D;
