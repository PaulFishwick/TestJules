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
    marginRight: '5px',
  }
};

/**
 * Controls component for managing the cellular automaton simulation.
 *
 * Props:
 * - onStart (function): Callback for the Start button.
 * - onPause (function): Callback for the Pause button.
 * - onReset (function): Callback for the Reset button.
 * - onRuleChange (function): Callback for when the rule number changes. Receives the new rule as an integer.
 * - currentRule (number|string): The current Wolfram rule number.
 * - isRunning (boolean): True if the simulation is active.
 */
const Controls = ({
  onStart,
  onPause,
  onReset,
  onRuleChange,
  currentRule,
  isRunning,
}) => {
  const handleRuleInputChange = (event) => {
    const newRuleString = event.target.value;
    // Allow empty input for user to clear, but don't call onRuleChange with NaN
    if (newRuleString === '') {
      onRuleChange(''); // Or handle as a specific state if needed
      return;
    }
    const newRule = parseInt(newRuleString, 10);
    if (!isNaN(newRule)) {
      // Clamp value between 0 and 255 before calling onRuleChange
      const clampedRule = Math.max(0, Math.min(255, newRule));
      if (clampedRule !== newRule) {
        // If clamping happened, update the input field visually via currentRule prop
        // (assuming parent component updates currentRule, which then re-renders this one)
         onRuleChange(clampedRule);
      } else {
         onRuleChange(newRule);
      }
    }
  };

  const handleBlur = (event) => {
    // If the input is empty or invalid on blur, reset to a valid default (e.g., 0 or last valid rule)
    // For now, if it's empty string that was passed up, parent might set it.
    // Or, if currentRule is not a number, force a default
    let ruleAsNumber = parseInt(currentRule, 10);
    if (isNaN(ruleAsNumber) || currentRule === '') { // currentRule could be an empty string if user cleared it
        onRuleChange(0); // Default to rule 0 if input is cleared or invalid
    } else if (ruleAsNumber < 0 || ruleAsNumber > 255) {
        onRuleChange(Math.max(0, Math.min(255, ruleAsNumber))); // Clamp if out of bounds
    }
  };


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
      <label htmlFor="ruleInput" style={styles.label}>Rule:</label>
      <input
        type="number"
        id="ruleInput"
        value={currentRule}
        onChange={handleRuleInputChange}
        onBlur={handleBlur} // Handle cases where input might be left empty or invalid
        min="0"
        max="255"
        style={styles.input}
      />
    </div>
  );
};

export default Controls;
