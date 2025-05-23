import React from 'react';

// Basic inline styles for simplicity. A CSS module can be used for more complex styling.
const styles = {
  controlsContainer: {
    margin: '10px 0',
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px', // Space between control elements
  },
  button: {
    padding: '8px 15px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    cursor: 'pointer',
    backgroundColor: '#f0f0f0',
  },
  buttonDisabled: {
    padding: '8px 15px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    cursor: 'not-allowed',
    backgroundColor: '#e0e0e0',
    color: '#aaa',
  },
  input: {
    padding: '8px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    width: '80px', // Adjust as needed
  },
  label: {
    marginRight: '5px', // Kept if any label-like text is used
  },
  ruleText: { // Style for the static rule display
    fontSize: '0.9em',
    color: '#333',
    marginLeft: '10px', // Add some space from the last button
  }
};

/**
 * Controls component for managing the cellular automaton simulation.
 *
 * Props:
 * - onStart (function): Callback for the Start button.
 * - onPause (function): Callback for the Pause button.
 * - onReset (function): Callback for the Reset button.
 * - isRunning (boolean): True if the simulation is active.
 */
const Controls = ({
  onStart,
  onPause,
  onReset,
  isRunning,
}) => {
  // handleRuleInputChange and handleBlur are removed as rule input is gone.

  return (
    <div style={styles.controlsContainer}>
      <button
        onClick={onStart}
        style={isRunning ? styles.buttonDisabled : styles.button}
        disabled={isRunning}
      >
        Start
      </button>
      <button
        onClick={onPause}
        style={!isRunning ? styles.buttonDisabled : styles.button}
        disabled={!isRunning}
      >
        Pause
      </button>
      <button
        onClick={onReset}
        style={styles.button}
      >
        Reset
      </button>
      <span style={styles.ruleText}>Rule: Conway's Game of Life</span>
    </div>
  );
};

export default Controls;
