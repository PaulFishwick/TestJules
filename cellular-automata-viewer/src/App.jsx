import React, { useState, useCallback, useEffect } from 'react';

// 1D Automata specific imports
import Automaton1DView from './components/Automaton1DView.jsx';
import Controls1D from './components/Controls1D.jsx';
import { calculateNextGeneration, decimalToBinaryArray } from './automataLogic.js';

// 2D Automata specific imports
import Automaton2DView from './components/Automaton2DView.jsx';
import Controls2D from './components/Controls2D.jsx';
import { calculateNextGeneration2D } from './automataLogic2D.js';

// Shared constants
const SIMULATION_SPEED_MS = 200;

// 1D Constants
const INITIAL_1D_CELL_COUNT = 51;
const MAX_HISTORY_LENGTH_1D = 200;

// 2D Constants
const GRID_ROWS_APP = 50;
const GRID_COLS_APP = 50;

// Helper function for 1D initial generation
const createInitial1DGeneration = (cellCount = INITIAL_1D_CELL_COUNT) => {
  const initial = Array(cellCount).fill(0);
  if (cellCount > 0) {
    initial[Math.floor(cellCount / 2)] = 1; // Middle cell active
  }
  return initial;
};

// Helper function for 2D initial generation (existing)
const createInitial2DGrid = () => {
  const grid = Array(GRID_ROWS_APP).fill(null).map(() => Array(GRID_COLS_APP).fill(0));
  if (GRID_ROWS_APP > 5 && GRID_COLS_APP > 5) { // Simple Glider
    grid[1][2] = 1; grid[2][3] = 1; grid[3][1] = 1; grid[3][2] = 1; grid[3][3] = 1;
  }
  return grid;
};

function App() {
  // View selection state
  const [activeView, setActiveView] = useState('1d'); // Default to '1d'

  // 1D State
  const [rule1D, setRule1D] = useState(30);
  const [generationsHistory, setGenerationsHistory] = useState([createInitial1DGeneration()]);
  const [isRunning1D, setIsRunning1D] = useState(false);
  const [generationCount1D, setGenerationCount1D] = useState(0);

  // 2D State
  const [grid2D, setGrid2D] = useState(createInitial2DGrid());
  const [isRunning2D, setIsRunning2D] = useState(false);
  const [generationCount2D, setGenerationCount2D] = useState(0);

  // --- 1D Handlers ---
  const handleStart1D = useCallback(() => {
    if (activeView === '1d') setIsRunning1D(true);
  }, [activeView]);

  const handlePause1D = useCallback(() => {
    setIsRunning1D(false);
  }, []);

  const handleReset1D = useCallback(() => {
    setIsRunning1D(false);
    setGenerationsHistory([createInitial1DGeneration()]);
    setGenerationCount1D(0);
    // setRule1D(30); // Optionally reset rule to default
  }, []);

  const handleRuleChange1D = useCallback((newRule) => {
    setRule1D(newRule);
    // Reset simulation when rule changes for 1D, as history depends on it
    setIsRunning1D(false);
    setGenerationsHistory([createInitial1DGeneration()]);
    setGenerationCount1D(0);
  }, []);

  const handleCellClick1D = useCallback((rowIndex, cellIndex) => {
    if (!isRunning1D && rowIndex === 0 && generationsHistory.length > 0) {
      setGenerationsHistory((prevHistory) => {
        const newInitialGeneration = [...prevHistory[0]];
        newInitialGeneration[cellIndex] = newInitialGeneration[cellIndex] === 0 ? 1 : 0;
        const newHistory = [...prevHistory];
        newHistory[0] = newInitialGeneration;
        return newHistory; 
      });
    }
  }, [isRunning1D, generationsHistory]);

  // --- 2D Handlers ---
  const handleStart2D = useCallback(() => {
    if (activeView === '2d') setIsRunning2D(true);
  }, [activeView]);

  const handlePause2D = useCallback(() => {
    setIsRunning2D(false);
  }, []);

  const handleReset2D = useCallback(() => {
    setIsRunning2D(false);
    setGrid2D(createInitial2DGrid());
    setGenerationCount2D(0);
  }, []);

  const handleCellToggle2D = useCallback((rowIndex, colIndex) => {
    console.log('[App] handleCellToggle2D: Called with rowIndex, colIndex', rowIndex, colIndex, 'isRunning2D:', isRunning2D);
    if (!isRunning2D) {
      setGrid2D((prevGrid) => {
        console.log('[App] handleCellToggle2D: grid2D state before toggle for cell', rowIndex, colIndex, 'Value:', prevGrid[rowIndex] ? prevGrid[rowIndex][colIndex] : 'undefined');
        const newGrid = prevGrid.map(row => [...row]);
        if (rowIndex >= 0 && rowIndex < newGrid.length && colIndex >= 0 && colIndex < newGrid[0].length) {
          newGrid[rowIndex][colIndex] = newGrid[rowIndex][colIndex] === 0 ? 1 : 0;
          console.log('[App] handleCellToggle2D: newGrid state after toggle for cell', rowIndex, colIndex, 'New Value:', newGrid[rowIndex][colIndex]);
        }
        return newGrid;
      });
    }
  }, [isRunning2D]);


  // --- Simulation useEffect Loops ---

  // 1D Simulation Loop
  useEffect(() => {
    if (activeView !== '1d' || !isRunning1D) {
      return;
    }
    const current1DGen = generationsHistory[generationsHistory.length - 1];
    if (!current1DGen || current1DGen.length === 0) {
      console.warn("1D Simulation: Cannot start with an empty or invalid current generation.");
      setIsRunning1D(false);
      return;
    }
    const intervalId = setInterval(() => {
      setGenerationsHistory((prevHistory) => {
        const currentGen = prevHistory[prevHistory.length - 1];
        const nextGen = calculateNextGeneration(currentGen, rule1D);
        const newHistory = [...prevHistory, nextGen];
        if (newHistory.length > MAX_HISTORY_LENGTH_1D) {
          return newHistory.slice(newHistory.length - MAX_HISTORY_LENGTH_1D);
        }
        return newHistory;
      });
      setGenerationCount1D((prevCount) => prevCount + 1);
    }, SIMULATION_SPEED_MS);
    return () => clearInterval(intervalId);
  }, [activeView, isRunning1D, rule1D, generationsHistory]);

  // 2D Simulation Loop
  useEffect(() => {
    if (activeView !== '2d' || !isRunning2D) {
      return;
    }
    if (!grid2D || grid2D.length === 0) {
      console.warn("2D Simulation: Cannot start with an empty or invalid 2D grid.");
      setIsRunning2D(false);
      return;
    }
    const intervalId = setInterval(() => {
      console.log('[App] 2D Simulation tick: updating grid2D via calculateNextGeneration2D');
      setGrid2D((prevGrid) => calculateNextGeneration2D(prevGrid));
      setGenerationCount2D((prevCount) => prevCount + 1);
    }, SIMULATION_SPEED_MS);
    return () => clearInterval(intervalId);
  }, [activeView, isRunning2D, grid2D]);
  
  // Styles (can be further refined or moved to CSS)
  const appSpecificStyles = {
    appHeader: {
      backgroundColor: '#004085', padding: '15px', color: 'white',
      marginBottom: '10px', width: '100%', textAlign: 'center', borderRadius: '4px 4px 0 0',
    },
    viewSwitcher: {
      margin: '10px 0', display: 'flex', justifyContent: 'center', gap: '10px',
    },
    viewButton: {
      padding: '10px 15px', border: '1px solid #007bff', 
      backgroundColor: 'white', color: '#007bff', borderRadius: '4px', cursor: 'pointer',
    },
    viewButtonActive: {
      backgroundColor: '#007bff', color: 'white',
    },
    automatonDisplay: {
      display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '10px',
      padding: '10px', border: '1px solid #eee', borderRadius: '4px', backgroundColor: '#fdfdfd',
    },
    statusText: { marginTop: '10px', fontSize: '0.9em', color: '#555' }
  };
  
  const handleViewChange = (view) => {
    setIsRunning1D(false); // Pause 1D simulation
    setIsRunning2D(false); // Pause 2D simulation
    setActiveView(view);
  };

  return (
    <div className="app-container">
      <header style={appSpecificStyles.appHeader}>
        <h1 style={{ color: 'white' }}>
          {activeView === '1d' ? '1D Cellular Automaton' : '2D Cellular Automaton (Game of Life)'}
        </h1>
      </header>

      <div style={appSpecificStyles.viewSwitcher}>
        <button 
          onClick={() => handleViewChange('1d')} 
          style={{...appSpecificStyles.viewButton, ...(activeView === '1d' ? appSpecificStyles.viewButtonActive : {})}}
          disabled={activeView === '1d'}
        >
          Show 1D Automata
        </button>
        <button 
          onClick={() => handleViewChange('2d')} 
          style={{...appSpecificStyles.viewButton, ...(activeView === '2d' ? appSpecificStyles.viewButtonActive : {})}}
          disabled={activeView === '2d'}
        >
          Show 2D Automata
        </button>
      </div>

      {/* Conditional rendering for Controls and AutomatonView */}
      {activeView === '1d' ? (
        <>
          <Controls1D
            onStart={handleStart1D}
            onPause={handlePause1D}
            onReset={handleReset1D}
            onRuleChange={handleRuleChange1D}
            currentRule={rule1D}
            isRunning={isRunning1D}
          />
          <div style={appSpecificStyles.automatonDisplay}>
            <Automaton1DView
              generationsHistory={generationsHistory}
              onCellClick={handleCellClick1D}
            />
            <p style={appSpecificStyles.statusText}>Generation: {generationCount1D}</p>
            <p style={appSpecificStyles.statusText}>Rule: {rule1D}</p>
          </div>
        </>
      ) : ( // activeView === '2d'
        <>
          <Controls2D
            onStart={handleStart2D}
            onPause={handlePause2D}
            onReset={handleReset2D}
            isRunning={isRunning2D}
          />
          <div style={appSpecificStyles.automatonDisplay}>
            <Automaton2DView
              currentGrid={grid2D}
              onCellToggle={handleCellToggle2D}
            />
            <p style={appSpecificStyles.statusText}>Generation: {generationCount2D}</p>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
