import React, { useState, useCallback, useEffect } from 'react';
import Automaton2DView from './components/Automaton2DView.jsx'; // Changed import
import Controls from './components/Controls.jsx';
import { calculateNextGeneration2D } from './automataLogic2D.js'; // Changed import
// import './App.css';

const SIMULATION_SPEED_MS = 200;
const GRID_ROWS_APP = 50; // Corresponds to GRID_ROWS in Automaton2DView
const GRID_COLS_APP = 50; // Corresponds to GRID_COLS in Automaton2DView

// Creates an initial 2D grid with a glider pattern
const createInitial2DGrid = () => {
  const grid = Array(GRID_ROWS_APP).fill(null).map(() => Array(GRID_COLS_APP).fill(0));
  // Simple Glider
  if (GRID_ROWS_APP > 5 && GRID_COLS_APP > 5) {
    grid[1][2] = 1;
    grid[2][3] = 1;
    grid[3][1] = 1;
    grid[3][2] = 1;
    grid[3][3] = 1;
  }
  return grid;
};

function App() {
  const [isRunning, setIsRunning] = useState(false);
  const [grid2D, setGrid2D] = useState(createInitial2DGrid());
  const [generationCount, setGenerationCount] = useState(0);

  const handleStart = useCallback(() => {
    setIsRunning(true);
  }, []);

  const handlePause = useCallback(() => {
    setIsRunning(false);
  }, []);

  const handleReset = useCallback(() => {
    setIsRunning(false);
    setGrid2D(createInitial2DGrid());
    setGenerationCount(0);
  }, []);

  const handleCellToggle2D = useCallback((rowIndex, colIndex) => {
    if (!isRunning) {
      setGrid2D((prevGrid) => {
        // Create a deep copy of the grid to avoid mutating the previous state directly
        const newGrid = prevGrid.map(row => [...row]);
        // Ensure rowIndex and colIndex are within bounds (though Automaton2DView should also check)
        if (rowIndex >= 0 && rowIndex < newGrid.length && colIndex >= 0 && colIndex < newGrid[0].length) {
          newGrid[rowIndex][colIndex] = newGrid[rowIndex][colIndex] === 0 ? 1 : 0;
        }
        return newGrid;
      });
      // Optionally, reset generation count if manual interaction should restart "history"
      // setGenerationCount(0); 
    }
  }, [isRunning]); // isRunning is a dependency to ensure it only works when paused

  useEffect(() => {
    if (!isRunning) {
      return;
    }

    if (!grid2D || grid2D.length === 0) {
      console.warn("Simulation cannot start with an empty or invalid 2D grid.");
      setIsRunning(false);
      return;
    }

    const intervalId = setInterval(() => {
      setGrid2D((prevGrid) => calculateNextGeneration2D(prevGrid));
      setGenerationCount((prevCount) => prevCount + 1);
    }, SIMULATION_SPEED_MS);

    return () => clearInterval(intervalId);
  }, [isRunning, grid2D]); // grid2D is a dependency to ensure the interval callback uses the latest grid
                            // if not using functional update for setGrid2D, though functional update is used here.
                            // Keeping it can be safer if calculateNextGeneration2D was complex and defined inside App.
                            // For now, this is fine.

  // Styles can be adjusted if needed
  const appSpecificStyles = {
    appHeader: {
      backgroundColor: '#004085',
      padding: '15px',
      color: 'white',
      marginBottom: '25px',
      width: '100%',
      textAlign: 'center',
      borderRadius: '4px 4px 0 0',
    },
    automatonDisplay: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      marginTop: '20px',
      padding: '10px',
      border: '1px solid #eee',
      borderRadius: '4px',
      backgroundColor: '#fdfdfd', // Background for the area containing the canvas
      // width: 'auto', // Let canvas define width or set specific
      // minWidth: '300px', 
      // maxWidth: '100%',
    },
    statusText: {
      marginTop: '10px',
      fontSize: '0.9em',
      color: '#555',
    }
  };

  return (
    <div className="app-container">
      <header style={appSpecificStyles.appHeader}>
        <h1 style={{ color: 'white' }}>2D Cellular Automaton (Game of Life)</h1>
      </header>
      <Controls
        onStart={handleStart}
        onPause={handlePause}
        onReset={handleReset}
        // onRuleChange and currentRule are removed as they are 1D specific for now
        isRunning={isRunning}
      />
      <div style={appSpecificStyles.automatonDisplay}>
        <Automaton2DView
          currentGrid={grid2D}
          onCellToggle={handleCellToggle2D}
          // width and height can be passed to Automaton2DView if needed
          // e.g., width={GRID_COLS_APP * CELL_SIZE_IN_VIEW}
        />
        <p style={appSpecificStyles.statusText}>Generation: {generationCount}</p>
        {/* Rule display removed */}
      </div>
    </div>
  );
}

export default App;
