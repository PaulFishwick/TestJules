// Content for automataLogic2D.js

const countLiveNeighbors = (grid, r, c) => {
  let count = 0;
  const numRows = grid.length;
  const numCols = grid[0].length;

  for (let i = -1; i <= 1; i++) {
    for (let j = -1; j <= 1; j++) {
      if (i === 0 && j === 0) continue; // Skip the cell itself

      const nr = (r + i + numRows) % numRows; // Wrap around rows
      const nc = (c + j + numCols) % numCols; // Wrap around columns

      if (grid[nr][nc] === 1) {
        count++;
      }
    }
  }
  return count;
};

const calculateNextGeneration2D = (currentGrid) => {
  if (!currentGrid || currentGrid.length === 0 || !currentGrid[0] || currentGrid[0].length === 0) {
    console.warn("[automataLogic2D] Invalid or empty grid provided.");
    return []; // Or return currentGrid if preferred for empty inputs
  }

  const numRows = currentGrid.length;
  const numCols = currentGrid[0].length;
  const nextGrid = Array(numRows).fill(null).map(() => Array(numCols).fill(0));

  for (let r = 0; r < numRows; r++) {
    for (let c = 0; c < numCols; c++) {
      const liveNeighbors = countLiveNeighbors(currentGrid, r, c);
      const cellIsAlive = currentGrid[r][c] === 1;

      if (cellIsAlive) {
        if (liveNeighbors < 2 || liveNeighbors > 3) {
          nextGrid[r][c] = 0; // Dies (underpopulation or overpopulation)
        } else {
          nextGrid[r][c] = 1; // Lives
        }
      } else {
        if (liveNeighbors === 3) {
          nextGrid[r][c] = 1; // Becomes alive (reproduction)
        } else {
          nextGrid[r][c] = 0; // Stays dead
        }
      }
    }
  }
  return nextGrid;
};

export { calculateNextGeneration2D, countLiveNeighbors }; // Exporting countLiveNeighbors can be useful for other rules later
