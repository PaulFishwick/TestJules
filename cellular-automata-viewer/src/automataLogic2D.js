/**
 * Counts the number of live neighbors for a cell in a 2D grid with periodic boundary conditions.
 *
 * @param {number[][]} grid The current generation grid.
 * @param {number} r The row index of the cell.
 * @param {number} c The column index of the cell.
 * @param {number} numRows The total number of rows in the grid.
 * @param {number} numCols The total number of columns in the grid.
 * @returns {number} The count of live neighbors.
 */
function countLiveNeighbors(grid, r, c, numRows, numCols) {
  let liveNeighbors = 0;
  for (let i = -1; i <= 1; i++) {
    for (let j = -1; j <= 1; j++) {
      if (i === 0 && j === 0) {
        continue; // Skip the cell itself
      }
      // Calculate neighbor coordinates with periodic boundary conditions
      const neighborRow = (r + i + numRows) % numRows;
      const neighborCol = (c + j + numCols) % numCols;
      liveNeighbors += grid[neighborRow][neighborCol];
    }
  }
  return liveNeighbors;
}

/**
 * Calculates the next generation of a 2D cellular automaton based on Conway's Game of Life rules.
 *
 * @param {number[][]} currentGrid A 2D array representing the current state (0 for dead, 1 for alive).
 * @returns {number[][]} A new 2D array representing the next generation's state.
 *                       Returns an empty array if the input grid is invalid.
 */
export function calculateNextGeneration2D(currentGrid) {
  if (!currentGrid || currentGrid.length === 0 || !Array.isArray(currentGrid[0])) {
    console.warn("Invalid or empty grid provided to calculateNextGeneration2D.");
    return []; // Return empty array for invalid input
  }

  const numRows = currentGrid.length;
  const numCols = currentGrid[0].length;

  // Check for non-rectangular grid (all rows should have the same length as the first row)
  for (let r = 1; r < numRows; r++) {
    if (!currentGrid[r] || currentGrid[r].length !== numCols) {
      console.warn("Non-rectangular grid provided. All rows must have the same number of columns.");
      return []; // Or return currentGrid;
    }
  }

  // Create a new grid initialized with 0s
  const newGrid = Array(numRows).fill(null).map(() => Array(numCols).fill(0));

  for (let r = 0; r < numRows; r++) {
    for (let c = 0; c < numCols; c++) {
      const liveNeighbors = countLiveNeighbors(currentGrid, r, c, numRows, numCols);
      const cellState = currentGrid[r][c];

      if (cellState === 1) { // Cell is ALIVE
        if (liveNeighbors < 2) {
          newGrid[r][c] = 0; // Dies (underpopulation)
        } else if (liveNeighbors === 2 || liveNeighbors === 3) {
          newGrid[r][c] = 1; // Lives
        } else {
          newGrid[r][c] = 0; // Dies (overpopulation)
        }
      } else { // Cell is DEAD
        if (liveNeighbors === 3) {
          newGrid[r][c] = 1; // Becomes ALIVE (reproduction)
        } else {
          newGrid[r][c] = 0; // Stays DEAD
        }
      }
    }
  }

  return newGrid;
}

/*
// --- Example Usage & Testing ---

console.log("--- Testing calculateNextGeneration2D ---");

// Example 1: Blinker (period 2 oscillator)
let blinker_gen0 = [
  [0, 1, 0],
  [0, 1, 0],
  [0, 1, 0]
];
console.log("Blinker Gen 0:");
blinker_gen0.forEach(row => console.log(row.join(' ')));

let blinker_gen1 = calculateNextGeneration2D(blinker_gen0);
console.log("Blinker Gen 1 (Expected: 000, 111, 000):");
blinker_gen1.forEach(row => console.log(row.join(' ')));

let blinker_gen2 = calculateNextGeneration2D(blinker_gen1);
console.log("Blinker Gen 2 (Expected: back to Gen 0):");
blinker_gen2.forEach(row => console.log(row.join(' ')));


// Example 2: Block (stable)
let block_gen0 = [
  [0, 0, 0, 0],
  [0, 1, 1, 0],
  [0, 1, 1, 0],
  [0, 0, 0, 0]
];
console.log("\nBlock Gen 0:");
block_gen0.forEach(row => console.log(row.join(' ')));

let block_gen1 = calculateNextGeneration2D(block_gen0);
console.log("Block Gen 1 (Expected: same as Gen 0):");
block_gen1.forEach(row => console.log(row.join(' ')));


// Example 3: Glider (moves diagonally)
// (Needs a larger grid to see movement without hitting boundary effects too soon if not handled by periodic)
let glider_grid = [
  [0, 1, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [1, 1, 1, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0]
];

console.log("\nGlider Gen 0:");
glider_grid.forEach(row => console.log(row.join(" ")));

for (let i = 0; i < 5; i++) {
    glider_grid = calculateNextGeneration2D(glider_grid);
    console.log(`Glider Gen ${i + 1}:`);
    glider_grid.forEach(row => console.log(row.join(" ")));
}

// Test with empty grid
console.log("\nTest with empty grid:", calculateNextGeneration2D([])); // Expected: []

// Test with non-rectangular grid
console.log("\nTest with non-rectangular grid:", calculateNextGeneration2D([[0,1],[0]])); // Expected: []
*/

/**
 * How to test this file:
 * 1. Save as `automataLogic2D.js`.
 * 2. Uncomment the example usage section.
 * 3. Run with Node.js: `node path/to/automataLogic2D.js`
 * 4. Observe the console output and verify against expected Game of Life patterns.
 */
