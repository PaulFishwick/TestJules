/**
 * Converts a decimal number (Wolfram rule) into its binary representation as an array of 0s and 1s.
 *
 * @param {number} decimalRule The Wolfram rule number (0-255).
 * @param {number} [numBits=8] The number of bits for the binary representation.
 * @returns {number[]} An array of 0s and 1s representing the binary rule, padded with leading zeros.
 *                     Returns an empty array if the input is invalid or numBits is non-positive.
 */
export function decimalToBinaryArray(decimalRule, numBits = 8) {
  if (
    typeof decimalRule !== 'number' ||
    decimalRule < 0 ||
    decimalRule > 255 || // Wolfram rules are typically 0-255 for 3-neighbor systems
    typeof numBits !== 'number' ||
    numBits <= 0
  ) {
    console.error("Invalid input to decimalToBinaryArray. Rule must be 0-255, numBits must be positive.");
    // For Wolfram rules (3 neighbors), 2^3 = 8 possible states for neighbors, so rule is 8 bits.
    // If numBits is not 8, the rule interpretation might be different.
    // However, the function is made generic for numBits.
    if (numBits !== 8 && decimalRule > (2**numBits -1) ) {
        console.warn(`decimalRule ${decimalRule} might be too large for ${numBits} bits.`);
    }
    // Fallback or error handling: return empty or throw error
    // For now, returning an array of zeros of length numBits or an empty array if numBits is problematic
     return Array(numBits > 0 ? numBits : 0).fill(0);
  }

  const binaryString = decimalRule.toString(2);
  const binaryArray = binaryString.padStart(numBits, '0').split('').map(Number);
  return binaryArray;
}

/**
 * Calculates the next generation of a 1D cellular automaton based on the current generation and a Wolfram rule.
 *
 * @param {number[]} currentGeneration An array of 0s and 1s representing the current state.
 * @param {number} ruleNumber The Wolfram rule number (0-255).
 * @returns {number[]} A new array representing the next generation. Returns an empty array if inputs are invalid.
 */
export function calculateNextGeneration(currentGeneration, ruleNumber) {
  if (!Array.isArray(currentGeneration) || currentGeneration.some(cell => cell !== 0 && cell !== 1)) {
    console.error("Invalid currentGeneration: Must be an array of 0s and 1s.");
    return [];
  }
  if (typeof ruleNumber !== 'number' || ruleNumber < 0 || ruleNumber > 255) {
    console.error("Invalid ruleNumber: Must be a number between 0 and 255.");
    return [];
  }
  if (currentGeneration.length === 0) {
    return [];
  }

  const ruleBinary = decimalToBinaryArray(ruleNumber, 8); // Standard 8-bit rule for 3 neighbors
  const nextGeneration = [];
  const len = currentGeneration.length;

  for (let i = 0; i < len; i++) {
    const leftNeighbor = currentGeneration[(i - 1 + len) % len];
    const currentCell = currentGeneration[i];
    const rightNeighbor = currentGeneration[(i + 1) % len];

    // Convert the 3-cell neighborhood (left, current, right) to a decimal index (0-7)
    // The binary string "abc" corresponds to decimal a*4 + b*2 + c*1
    const neighborhoodPattern = `${leftNeighbor}${currentCell}${rightNeighbor}`;
    const ruleIndex = parseInt(neighborhoodPattern, 2);

    // The ruleBinary array is indexed from left to right (most significant to least significant bit).
    // A common convention for Wolfram rules is that the rule's binary bits correspond to patterns
    // 111, 110, 101, 100, 011, 010, 001, 000.
    // So, ruleBinary[0] is for "111", ruleBinary[7] is for "000".
    // Our ruleIndex is calculated as 7 for "111" and 0 for "000".
    // Therefore, we need to use `ruleBinary[7 - ruleIndex]`.
    nextGeneration[i] = ruleBinary[7 - ruleIndex];
  }

  return nextGeneration;
}

/*
// --- Example Usage & Testing ---

// Test decimalToBinaryArray
console.log("--- Testing decimalToBinaryArray ---");
console.log("Rule 30 (8 bits):", decimalToBinaryArray(30)); // Expected: [0,0,0,1,1,1,1,0]
console.log("Rule 90 (8 bits):", decimalToBinaryArray(90)); // Expected: [0,1,0,1,1,0,1,0]
console.log("Rule 0 (8 bits):", decimalToBinaryArray(0));   // Expected: [0,0,0,0,0,0,0,0]
console.log("Rule 255 (8 bits):", decimalToBinaryArray(255)); // Expected: [1,1,1,1,1,1,1,1]
console.log("Rule 5 (4 bits):", decimalToBinaryArray(5, 4)); // Expected: [0,1,0,1]
console.log("Rule 30 (invalid bits):", decimalToBinaryArray(30, -1)); // Expected: [] or error + default array
console.log("Rule 300 (invalid rule):", decimalToBinaryArray(300)); // Expected: [] or error + default array

// Test calculateNextGeneration
console.log("\n--- Testing calculateNextGeneration ---");

// Rule 30:
// Binary: 00011110
// Patterns (Neighborhood -> Output):
// 111 -> 0
// 110 -> 0
// 101 -> 0
// 100 -> 1
// 011 -> 1
// 010 -> 1
// 001 -> 1
// 000 -> 0

let generation0 = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]; // Single '1' in the middle
console.log("Initial Generation (single 1):", generation0);

let generation1_rule30 = calculateNextGeneration(generation0, 30);
// Expected for Rule 30 from single 1: [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0] (approx)
// Let's trace for center '1':
// ...0,0,0... neighborhood for the '1' is 010. Rule index 2. Output ruleBinary[7-2] = ruleBinary[5] = 1.
// ...0,0,1... neighborhood for cell left of '1' is 001. Rule index 1. Output ruleBinary[7-1] = ruleBinary[6] = 1.
// ...1,0,0... neighborhood for cell right of '1' is 100. Rule index 4. Output ruleBinary[7-4] = ruleBinary[3] = 1.
console.log("Next Gen (Rule 30):", generation1_rule30);

let generation2_rule30 = calculateNextGeneration(generation1_rule30, 30);
console.log("Next Gen^2 (Rule 30):", generation2_rule30);


// Rule 90:
// Binary: 01011010
// Patterns (Neighborhood -> Output):
// 111 -> 0
// 110 -> 1
// 101 -> 0
// 100 -> 1
// 011 -> 1
// 010 -> 0
// 001 -> 1
// 000 -> 0
// Known as "XOR" rule or Sierpinski triangle pattern from a single '1'
let generation1_rule90 = calculateNextGeneration(generation0, 90);
// Expected for Rule 90 from single 1:
// Center 1 (010) -> ruleBinary[7-2] = ruleBinary[5] ('0' from 01011*0*10) -> 0
// Left of center 1 (001) -> ruleBinary[7-1] = ruleBinary[6] ('1' from 010110*1*0) -> 1
// Right of center 1 (100) -> ruleBinary[7-4] = ruleBinary[3] ('1' from 010*1*1010) -> 1
// So, [...,0,1,0,1,0,...]
console.log("Next Gen (Rule 90):", generation1_rule90);

let generation2_rule90 = calculateNextGeneration(generation1_rule90, 90);
console.log("Next Gen^2 (Rule 90):", generation2_rule90);

// Test with an empty generation
console.log("Empty generation:", calculateNextGeneration([], 30)); // Expected: []

// Test with invalid generation
console.log("Invalid generation:", calculateNextGeneration([0, 1, 2], 30)); // Expected: [] + error

// Test with invalid rule
console.log("Invalid rule:", calculateNextGeneration([0,1,0], 300)); // Expected: [] + error
*/

/**
 * How to test these functions:
 *
 * 1. Manual Testing (as shown above):
 *    - Uncomment the example usage section.
 *    - Run this file with Node.js: `node cellular-automata-viewer/src/automataLogic.js`
 *    - Observe the console output and verify against expected results for various rules and initial states.
 *
 * 2. Unit Testing (Recommended for robust applications):
 *    - Use a JavaScript testing framework like Jest, Mocha, or Vitest (which comes with Vite).
 *    - Create a corresponding test file (e.g., `automataLogic.test.js`).
 *    - Import the functions into your test file.
 *    - Write individual test cases for:
 *      - `decimalToBinaryArray`:
 *        - Correct conversion for common rules (0, 30, 90, 110, 255).
 *        - Correct padding with leading zeros.
 *        - Handling of different `numBits` values.
 *        - Handling of edge cases and invalid inputs (negative numbers, non-numbers, rule > 255, non-positive numBits).
 *      - `calculateNextGeneration`:
 *        - Correct next generation for known rules and simple initial states (e.g., single '1', alternating '0's and '1's).
 *        - Correct application of periodic boundary conditions (test edges of the array).
 *        - Handling of empty `currentGeneration`.
 *        - Handling of invalid `currentGeneration` (e.g., contains non-0/1 values).
 *        - Handling of invalid `ruleNumber`.
 *
 * Example (using Jest/Vitest syntax for `automataLogic.test.js`):
 *
 * ```javascript
 * import { decimalToBinaryArray, calculateNextGeneration } from './automataLogic';
 *
 * describe('decimalToBinaryArray', () => {
 *   test('should convert rule 30 to binary array', () => {
 *     expect(decimalToBinaryArray(30)).toEqual([0,0,0,1,1,1,1,0]);
 *   });
 *   // ... more test cases
 * });
 *
 * describe('calculateNextGeneration', () => {
 *   test('should calculate next generation for rule 30 with a single 1', () => {
 *     const current = [0,0,0,1,0,0,0];
 *     // Rule 30: 00011110
 *     // 000 -> 0 (ruleBinary[7])
 *     // 001 -> 1 (ruleBinary[6])
 *     // 010 -> 1 (ruleBinary[5])
 *     // 100 -> 1 (ruleBinary[3])
 *     // For [0,0,0,1,0,0,0]
 *     // i=0 (000): (0+0+0)%7 = 0. neighborhood 000. index 0. output ruleBinary[7-0]=0.
 *     // i=1 (001): (0+0+0)%7 = 0. neighborhood 001. index 1. output ruleBinary[7-1]=1.
 *     // i=2 (010): (0+0+1)%7 = 1. neighborhood 010. index 2. output ruleBinary[7-2]=1.
 *     // i=3 (100): (0+1+0)%7 = 1. neighborhood 100. index 4. output ruleBinary[7-4]=1.
 *     // i=4 (000): (1+0+0)%7 = 1. neighborhood 000. index 0. output ruleBinary[7-0]=0.
 *     // i=5 (000): (0+0+0)%7 = 0. neighborhood 000. index 0. output ruleBinary[7-0]=0.
 *     // i=6 (000): (0+0+0)%7 = 0. neighborhood 000. index 0. output ruleBinary[7-0]=0.
 *     // Expected: [0,1,1,1,1,0,0] (Error in manual trace above, let's re-verify rule 30 application)
 *     // Rule 30 (00011110):
 *     // 111(7)->0, 110(6)->0, 101(5)->0, 100(4)->1, 011(3)->1, 010(2)->1, 001(1)->1, 000(0)->0
 *     // Current: [0,0,0,1,0,0,0] (len=7)
 *     // i=0, N=current[6],C=0,R=current[1] => 000. Index 0. ruleBinary[7-0]=0. nextGen[0]=0
 *     // i=1, N=current[0],C=0,R=current[2] => 000. Index 0. ruleBinary[7-0]=0. nextGen[1]=0
 *     // i=2, N=current[1],C=0,R=current[3] => 001. Index 1. ruleBinary[7-1]=1. nextGen[2]=1
 *     // i=3, N=current[2],C=1,R=current[4] => 010. Index 2. ruleBinary[7-2]=1. nextGen[3]=1
 *     // i=4, N=current[3],C=0,R=current[5] => 100. Index 4. ruleBinary[7-4]=1. nextGen[4]=1
 *     // i=5, N=current[4],C=0,R=current[6] => 000. Index 0. ruleBinary[7-0]=0. nextGen[5]=0
 *     // i=6, N=current[5],C=0,R=current[0] => 000. Index 0. ruleBinary[7-0]=0. nextGen[6]=0
 *     expect(calculateNextGeneration(current, 30)).toEqual([0,0,1,1,1,0,0]);
 *   });
 *   // ... more test cases
 * });
 * ```
 */
