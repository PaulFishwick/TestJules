import React, { useRef, useEffect, useState, useCallback } from 'react';
import * as twgl from 'twgl.js'; // Or import specific functions: import { m4, createProgramInfo, ... } from 'twgl.js';

// Shader definitions
const VS_QUAD = `
  attribute vec2 a_position; // Vertices for a unit quad (e.g., 0,0 to 1,1)
  uniform mat4 u_matrix;     // Transforms the unit quad to the correct cell
  
  void main() {
    gl_Position = u_matrix * vec4(a_position, 0.0, 1.0);
  }
`;

const FS_COLOR = `
  precision mediump float;
  uniform vec4 u_color;
  
  void main() {
    gl_FragColor = u_color; // gl_FragColor for WebGL1 compat, TWGL might handle outColor
  }
`;

// Color constants
const ALIVE_COLOR = [0.1, 0.1, 0.1, 1]; // Dark grey
const DEAD_COLOR = [0.9, 0.9, 0.9, 1];  // Light grey

/**
 * Automaton2DView component uses WebGL (via TWGL.js) to render a 2D cellular automaton.
 *
 * Props:
 * - width (number): The width of the canvas. Defaults to 500.
 * - height (number): The height of the canvas. Defaults to 500.
 * - currentGrid (number[][]): The 2D grid state to render.
 * - onCellToggle (function): Callback when a cell should be toggled. Receives (rowIndex, colIndex).
 */
const Automaton2DView = ({
  width = 500,
  height = 500,
  currentGrid,
  onCellToggle,
}) => {
  const canvasRef = useRef(null);
  const glRef = useRef(null);
  const programInfoRef = useRef(null);
  const quadBufferInfoRef = useRef(null);
  const [webGLError, setWebGLError] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const lastToggledCellRef = useRef({ r: -1, c: -1 });

  const getCellFromMouseEvent = (event) => {
    if (!canvasRef.current || !currentGrid || currentGrid.length === 0) return null;

    const rect = canvasRef.current.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    const gl = glRef.current;
    if (!gl) return null;

    const numRows = currentGrid.length;
    const numCols = currentGrid[0].length;
    console.log('[View] getCellFromMouseEvent: mouseX, mouseY', mouseX, mouseY, 'canvas dims:', gl.canvas.width, gl.canvas.height, 'numCols, numRows:', numCols, numRows);

    const cellWidth = gl.canvas.width / numCols;
    const cellHeight = gl.canvas.height / numRows;
    console.log('[View] getCellFromMouseEvent: calculated cellWidth, cellHeight', cellWidth, cellHeight);

    const colIndex = Math.floor(mouseX / cellWidth);
    const rowIndex = Math.floor(mouseY / cellHeight);
    console.log('[View] getCellFromMouseEvent: calculated rowIndex, colIndex', rowIndex, colIndex);

    if (rowIndex >= 0 && rowIndex < numRows && colIndex >= 0 && colIndex < numCols) {
      return { rowIndex, colIndex };
    }
    return null;
  };

  const handleMouseDown = (event) => {
    console.log('[View] handleMouseDown: event', event.nativeEvent.offsetX, event.nativeEvent.offsetY);
    setIsDragging(true);
    const cell = getCellFromMouseEvent(event);
    console.log('[View] handleMouseDown: cell', cell);
    if (cell && onCellToggle) {
      onCellToggle(cell.rowIndex, cell.colIndex);
      lastToggledCellRef.current = { r: cell.rowIndex, c: cell.colIndex };
      console.log('[View] handleMouseDown: onCellToggle called with', cell.rowIndex, cell.colIndex);
    }
  };

  const handleMouseMove = (event) => {
    console.log('[View] handleMouseMove: dragging?', isDragging);
    if (!isDragging) return;
    const cell = getCellFromMouseEvent(event);
    console.log('[View] handleMouseMove: cell', cell);
    if (cell && onCellToggle) {
      if (cell.rowIndex !== lastToggledCellRef.current.r || cell.colIndex !== lastToggledCellRef.current.c) {
        onCellToggle(cell.rowIndex, cell.colIndex);
        lastToggledCellRef.current = { r: cell.rowIndex, c: cell.colIndex };
        console.log('[View] handleMouseMove: onCellToggle called with', cell.rowIndex, cell.colIndex);
      }
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    lastToggledCellRef.current = { r: -1, c: -1 }; // Reset last toggled cell
  };

  const handleMouseLeave = () => {
    setIsDragging(false); // Stop dragging if mouse leaves canvas
    lastToggledCellRef.current = { r: -1, c: -1 };
  };

  const drawGrid = useCallback(() => {
    const gl = glRef.current;
    const programInfo = programInfoRef.current;
    const quadBufferInfo = quadBufferInfoRef.current;

    console.log('[View] drawGrid: Called. currentGrid dimensions:', currentGrid ? currentGrid.length : 'null', currentGrid && currentGrid[0] ? currentGrid[0].length : 'null');

    if (!gl || !programInfo || !quadBufferInfo || !currentGrid || currentGrid.length === 0) {
      if (gl) {
        gl.clearColor(0.95, 0.95, 0.95, 1); 
        gl.clear(gl.COLOR_BUFFER_BIT);
      }
      return;
    }

    const numRows = currentGrid.length;
    const numCols = currentGrid[0].length;

    if (numRows === 0 || numCols === 0) {
        if (gl) {
            gl.clearColor(0.95, 0.95, 0.95, 1); 
            gl.clear(gl.COLOR_BUFFER_BIT);
        }
        return; // Nothing to draw
    }
    
    // It's important to resize the canvas before calculating cellWidth/cellHeight
    // if the canvas drawingBuffer size doesn't match the CSS display size.
    // twgl.resizeCanvasToDisplaySize handles this.
    twgl.resizeCanvasToDisplaySize(gl.canvas);
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
    
    gl.clearColor(0.95, 0.95, 0.95, 1); // Light background for the grid area
    gl.clear(gl.COLOR_BUFFER_BIT);

    gl.useProgram(programInfo.program);
    twgl.setBuffersAndAttributes(gl, programInfo, quadBufferInfo);

    const cellWidth = gl.canvas.width / numCols;
    const cellHeight = gl.canvas.height / numRows;
    
    const projectionMatrix = twgl.m4.ortho(0, gl.canvas.width, gl.canvas.height, 0, -1, 1);

    for (let r = 0; r < numRows; r++) {
      for (let c = 0; c < numCols; c++) {
        const modelMatrix = twgl.m4.identity();
        twgl.m4.translate(modelMatrix, [c * cellWidth, r * cellHeight, 0], modelMatrix);
        twgl.m4.scale(modelMatrix, [cellWidth, cellHeight, 1], modelMatrix);
        
        const u_matrix = twgl.m4.multiply(projectionMatrix, modelMatrix);
        const u_color = currentGrid[r][c] === 1 ? ALIVE_COLOR : DEAD_COLOR;

        twgl.setUniforms(programInfo, {
          u_matrix,
          u_color,
        });
        twgl.drawBufferInfo(gl, quadBufferInfo);
      }
    }
  }, [currentGrid]); // Depends on currentGrid

  useEffect(() => {
    // This effect handles both initialization and re-drawing when currentGrid changes.
    console.log('[View] Main useEffect: currentGrid changed or drawGrid recreated. Calling drawGrid.');
    if (!canvasRef.current) return;

    // Initialize GL context and resources if not already done
    if (!glRef.current) {
      const gl = canvasRef.current.getContext('webgl2');
      if (!gl) {
        setWebGLError('WebGL2 is not available. Please use a compatible browser.');
        return;
      }
      glRef.current = gl;
      console.log('[View] WebGL context obtained.');

      programInfoRef.current = twgl.createProgramInfo(gl, [VS_QUAD, FS_COLOR]);
       if (!programInfoRef.current || !programInfoRef.current.program) {
        setWebGLError('Failed to compile/link shader program.');
        console.error('[View] Shader program error:', gl.getProgramInfoLog(programInfoRef.current && programInfoRef.current.program));
        return;
      }
      console.log('[View] Shader program compiled and linked.');

      const unitQuadVertices = [0,0, 1,0, 0,1,  0,1, 1,0, 1,1];
      quadBufferInfoRef.current = twgl.createBufferInfoFromArrays(gl, {
        a_position: { numComponents: 2, data: unitQuadVertices },
      });
      console.log('[View] Quad buffer created.');
    }
    
    drawGrid();

    // Cleanup function for GL resources on unmount
    return () => {
      if (glRef.current) {
        if (programInfoRef.current && programInfoRef.current.program) {
          glRef.current.deleteProgram(programInfoRef.current.program);
        }
        if (quadBufferInfoRef.current) {
          if (quadBufferInfoRef.current.attribs && quadBufferInfoRef.current.attribs.a_position && quadBufferInfoRef.current.attribs.a_position.buffer) {
             glRef.current.deleteBuffer(quadBufferInfoRef.current.attribs.a_position.buffer);
          }
          if (quadBufferInfoRef.current.indices) { // Though not used for this quad, good practice
             glRef.current.deleteBuffer(quadBufferInfoRef.current.indices);
          }
        }
        console.log('Automaton2DView unmounted, WebGL resources potentially cleaned up.');
        // Do not nullify glRef.current here if other effects might still use it during unmount phase,
        // or ensure this is the last cleanup. For this setup, it's likely fine.
        // glRef.current = null; // Or manage this more carefully if multiple effects clean up GL state.
      }
    };
  }, [currentGrid, drawGrid]); // Re-run effect if currentGrid or drawGrid changes.

  // Resize handler - separate effect for clarity
  useEffect(() => {
    const handleResize = () => {
      // glRef.current check is implicitly handled by drawGrid
      drawGrid(); // Redraw on resize
    };
    window.addEventListener('resize', handleResize);
    
    // Call handleResize once initially to set correct canvas size based on CSS
    // This ensures that the first drawGrid call in the main effect uses correct canvas dimensions.
    // However, drawGrid itself calls resizeCanvasToDisplaySize, so this might be redundant
    // if the initial canvas dimensions are correctly set by width/height props.
    // For safety, especially if CSS influences size:
    if (glRef.current) { // Ensure GL is initialized before first resize draw
        handleResize();
    }

    return () => window.removeEventListener('resize', handleResize);
  }, [drawGrid]); // drawGrid is the dependency

  if (webGLError) {
    return (
      <div style={{ width, height, border: '1px solid red', padding: '10px', color: 'red' }}>
        <p>Error: {webGLError}</p>
      </div>
    );
  }

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      style={{ border: '1px solid #ccc', display: 'block', cursor: 'pointer' }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseLeave}
    />
  );
};

export default Automaton2DView;
