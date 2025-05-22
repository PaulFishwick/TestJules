import React, { useState, useCallback, useEffect } from 'react';
import Automaton1DView from './components/Automaton1DView.jsx';
import Controls from './components/Controls.jsx';
import { calculateNextGeneration } from './automataLogic.js';
// import './App.css'; // Remove if styles are now primarily in index.css or component modules

const INITIAL_CELL_COUNT = 51; // Odd number for a clear middle cell
const SIMULATION_SPEED_MS = 200; // Milliseconds

const createInitialGeneration = () => {
  const initial = Array(INITIAL_CELL_COUNT).fill(0);
  if (INITIAL_CELL_COUNT > 0) {
    initial[Math.floor(INITIAL_CELL_COUNT / 2)] = 1; // Middle cell active
  }
  return initial;
};

function App() {
  const [rule, setRule] = useState(30);
  const [isRunning, setIsRunning] = useState(false);
  const [generation, setGeneration] = useState(createInitialGeneration());
  const [generationCount, setGenerationCount] = useState(0);

  const handleStart = useCallback(() => {
    setIsRunning(true);
  }, []);

  const handlePause = useCallback(() => {
    setIsRunning(false);
  }, []);

  const handleReset = useCallback(() => {
    setIsRunning(false);
    setGeneration(createInitialGeneration());
    setGenerationCount(0);
  }, []);

  const handleRuleChange = useCallback((newRule) => {
    // Ensure newRule is a number before setting. Controls.jsx should provide a number or empty string.
    const ruleValue = (newRule === '' || isNaN(parseInt(newRule,10))) ? 0 : parseInt(newRule, 10);
    setRule(Math.max(0, Math.min(255, ruleValue))); // Clamp rule
    handleReset(); // Reset simulation when rule changes
  }, [handleReset]);

  const handleCellClick = useCallback((cellIndex) => {
    if (!isRunning) {
      setGeneration((prevGeneration) => {
        const newGeneration = [...prevGeneration];
        newGeneration[cellIndex] = newGeneration[cellIndex] === 0 ? 1 : 0;
        return newGeneration;
      });
      // Optional: Reset generation count if manual edit is considered a new start point
      // setGenerationCount(0);
    }
  }, [isRunning]);

  useEffect(() => {
    if (!isRunning) {
      return; // Do nothing if not running
    }

    // Check if generation array is valid before starting interval
    if (!generation || generation.length === 0) {
        console.warn("Simulation cannot start with an empty or invalid generation.");
        setIsRunning(false); // Stop running if generation is bad
        return;
    }

    const intervalId = setInterval(() => {
      setGeneration((prevGen) => calculateNextGeneration(prevGen, rule));
      setGenerationCount((prevCount) => prevCount + 1);
    }, SIMULATION_SPEED_MS);

    return () => clearInterval(intervalId); // Cleanup on unmount or if isRunning/rule changes
  }, [isRunning, rule]); // rule is included because calculateNextGeneration depends on it.

  // Define styles that were previously inline or in App.css if they are specific to App.jsx layout
  const appSpecificStyles = {
    appHeader: {
      backgroundColor: '#004085', // A darker blue for header
      padding: '15px',
      color: 'white',
      marginBottom: '25px',
      width: '100%', // Ensure header spans the app-container width
      textAlign: 'center',
      borderRadius: '4px 4px 0 0', // Rounded top corners if app-container has rounded corners
    },
    automatonDisplay: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      marginTop: '20px',
      padding: '10px',
      border: '1px solid #eee',
      borderRadius: '4px',
      backgroundColor: '#fdfdfd',
      width: 'auto', // Fit content, or specify width
      minWidth: '300px', // Ensure it's not too small
      maxWidth: '100%', // Prevent overflow from app-container
    },
    statusText: {
      marginTop: '10px',
      fontSize: '0.9em',
      color: '#555',
    }
  };

  return (
    <div className="app-container"> {/* Use the global .app-container style */}
      <header style={appSpecificStyles.appHeader}>
        <h1>1D Cellular Automaton</h1>
      </header>
      <Controls
        onStart={handleStart}
        onPause={handlePause}
        onReset={handleReset}
        onRuleChange={handleRuleChange}
        currentRule={rule}
        isRunning={isRunning}
      />
      <div style={appSpecificStyles.automatonDisplay}>
        <Automaton1DView
          generation={generation}
          onCellClick={handleCellClick}
        />
        <p style={appSpecificStyles.statusText}>Generation: {generationCount}</p>
        <p style={appSpecificStyles.statusText}>Rule: {rule}</p>
      </div>
    </div>
  );
}

export default App;
