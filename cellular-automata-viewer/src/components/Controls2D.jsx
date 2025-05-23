// Content for components/Controls2D.jsx
import React from 'react';
// Optional: import styles from './Controls.module.css'; // if a shared module exists

const Controls2D = ({ onStart, onPause, onReset, isRunning }) => {
  // Basic inline styles or use a CSS module
  const controlStyles = { /* ... (styles as defined previously for 2D controls) ... */ 
    controlsContainer: { display: 'flex', alignItems: 'center', gap: '10px', padding: '10px', marginBottom: '20px', flexWrap: 'wrap', justifyContent: 'center' },
    button: { padding: '8px 15px', border: 'none', borderRadius: '4px', cursor: 'pointer', backgroundColor: '#28a745', color: 'white' }, // Green for 2D
    buttonDisabled: { backgroundColor: '#6c757d' },
    ruleText: { fontSize: '1em', color: '#333', fontWeight: 'bold' } // Adjusted style
  };
  
  return (
    <div style={controlStyles.controlsContainer}>
      <button onClick={onStart} disabled={isRunning} style={{...controlStyles.button, ...(isRunning && controlStyles.buttonDisabled)}}>Start</button>
      <button onClick={onPause} disabled={!isRunning} style={{...controlStyles.button, ...(!isRunning && controlStyles.buttonDisabled)}}>Pause</button>
      <button onClick={onReset} style={controlStyles.button}>Reset</button>
      <span style={controlStyles.ruleText}>Rule: Conway's Game of Life</span>
    </div>
  );
};
export default Controls2D;
