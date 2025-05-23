import React, { useRef, useEffect } from 'react';
import styles from './Automaton1DView.module.css';

/**
 * Automaton1DView component renders a history of generations for a 1D cellular automaton.
 *
 * Props:
 * - generationsHistory (number[][]): An array of generation arrays. Each inner array
 *                                    consists of 0s and 1s representing cell states.
 * - onCellClick (function): A callback function invoked when a cell is clicked.
 *                           It receives `(rowIndex, cellIndex)` as arguments.
 */
const Automaton1DView = ({ generationsHistory, onCellClick }) => {
  if (!generationsHistory || !Array.isArray(generationsHistory) || generationsHistory.length === 0) {
    console.error("Automaton1DView: 'generationsHistory' prop is missing, not an array, or empty.");
    return <div style={{ padding: '10px', border: '1px solid #ccc' }}>No generation history to display.</div>;
  }

  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [generationsHistory]);

  // Style for the main container of all rows
  const historyContainerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center', // Center rows if they have varying intrinsic widths
    maxHeight: '500px',   // Max height for the scrollable area
    overflowY: 'auto',   // Enable vertical scrolling when content exceeds max height
    border: '1px solid #ddd', // Visually delineate the scrollable area
    padding: '5px',          // Some padding inside the scroll area
    minHeight: '50px', // Ensure it has some height even if empty initially (though handled by check)
    width: '100%', // Take available width from parent
  };

  return (
    <div ref={scrollRef} style={historyContainerStyle} className="automaton-history-container">
      {generationsHistory.map((generation, rowIndex) => (
        // Add a margin to automatonRow for spacing within the scrollable container if needed
        // Or adjust padding on historyContainerStyle
        <div key={rowIndex} className={styles.automatonRow} style={{ marginBottom: '2px' }}>
          {generation.map((cellState, cellIndex) => (
            <div
              key={cellIndex}
              className={`${styles.cell} ${cellState === 1 ? styles.cellAlive : styles.cellDead}`}
              onClick={() => onCellClick && onCellClick(rowIndex, cellIndex)}
              role="button"
              tabIndex={0}
              onKeyPress={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  onCellClick && onCellClick(rowIndex, cellIndex);
                }
              }}
              title={`Row ${rowIndex}, Cell ${cellIndex} - State: ${cellState}`}
            >
              {/* Cell content removed as per previous implementation */}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default Automaton1DView;
