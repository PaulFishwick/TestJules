import React from 'react';
import styles from './Automaton1DView.module.css';

/**
 * Automaton1DView component renders a single generation of a 1D cellular automaton.
 *
 * Props:
 * - generation (number[]): An array of 0s and 1s representing the state of cells.
 * - onCellClick (function): A callback function that is invoked when a cell is clicked.
 *                           It receives the index of the clicked cell as an argument.
 */
const Automaton1DView = ({ generation, onCellClick }) => {
  if (!generation || !Array.isArray(generation)) {
    // Or render some placeholder/error
    console.error("Automaton1DView: 'generation' prop is missing or not an array.");
    return <div className={styles.automatonRow}>Invalid generation data</div>;
  }

  return (
    <div className={styles.automatonRow}>
      {generation.map((cellState, index) => (
        <div
          key={index}
          className={`${styles.cell} ${cellState === 1 ? styles.cellAlive : styles.cellDead}`}
          onClick={() => onCellClick && onCellClick(index)}
          role="button" // For accessibility
          tabIndex={0} // For accessibility (keyboard focus)
          onKeyPress={(e) => { // For accessibility (keyboard interaction)
            if (e.key === 'Enter' || e.key === ' ') {
              onCellClick && onCellClick(index);
            }
          }}
          title={`Cell ${index} - State: ${cellState}`} // For better UX
        >
          {/* Optionally display cell index or state, though not required by task
          {index} */}
        </div>
      ))}
    </div>
  );
};

export default Automaton1DView;
