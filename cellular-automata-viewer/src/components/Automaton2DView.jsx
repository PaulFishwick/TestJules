// Content for components/Automaton2DView.jsx
import React, { useRef, useEffect, useState, useCallback } from 'react';
import * as twgl from 'twgl.js';

const VS_QUAD = `
  attribute vec2 a_position;
  uniform mat4 u_matrix;
  void main() { gl_Position = u_matrix * vec4(a_position, 0.0, 1.0); }
`;
const FS_COLOR = `
  precision mediump float;
  uniform vec4 u_color;
  void main() { gl_FragColor = u_color; }
`;
const ALIVE_COLOR = [0.1, 0.1, 0.1, 1];
const DEAD_COLOR = [0.9, 0.9, 0.9, 1];

const Automaton2DView = ({ width = 500, height = 500, currentGrid, onCellToggle }) => {
  const canvasRef = useRef(null);
  const glRef = useRef(null);
  const programInfoRef = useRef(null);
  const quadBufferInfoRef = useRef(null);
  const [webGLError, setWebGLError] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const lastToggledCellRef = useRef({ r: -1, c: -1 });

  console.log('[View] Automaton2DView rendering/re-rendering');

  const getCellFromMouseEvent = useCallback((event) => {
    // ... (implementation as previously defined and logged) ...
    if (!canvasRef.current || !currentGrid || currentGrid.length === 0) return null;
    const rect = canvasRef.current.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;
    const gl = glRef.current;
    if (!gl) return null;
    const numRows = currentGrid.length;
    const numCols = currentGrid[0].length;
    // console.log('[View] getCellFromMouseEvent: mouseX, mouseY', mouseX, mouseY, 'canvas dims:', gl.canvas.width, gl.canvas.height, 'numCols, numRows:', numCols, numRows);
    const cellWidth = gl.canvas.width / numCols;
    const cellHeight = gl.canvas.height / numRows;
    // console.log('[View] getCellFromMouseEvent: calculated cellWidth, cellHeight', cellWidth, cellHeight);
    const colIndex = Math.floor(mouseX / cellWidth);
    const rowIndex = Math.floor(mouseY / cellHeight);
    // console.log('[View] getCellFromMouseEvent: calculated rowIndex, colIndex', rowIndex, colIndex);
    if (rowIndex >= 0 && rowIndex < numRows && colIndex >= 0 && colIndex < numCols) {
      return { rowIndex, colIndex };
    }
    return null;
  }, [currentGrid]); // Added currentGrid dependency

  const handleMouseDown = useCallback((event) => {
    console.log('[View] handleMouseDown: FIRED');
    setIsDragging(true);
    const cell = getCellFromMouseEvent(event);
    console.log('[View] handleMouseDown: cell from getCellFromMouseEvent', cell);
    if (cell && onCellToggle) {
      onCellToggle(cell.rowIndex, cell.colIndex);
      lastToggledCellRef.current = { r: cell.rowIndex, c: cell.colIndex };
      console.log('[View] handleMouseDown: onCellToggle called with', cell.rowIndex, cell.colIndex);
    }
  }, [onCellToggle, getCellFromMouseEvent]); // Added dependencies

  const handleMouseMove = useCallback((event) => {
    // console.log('[View] handleMouseMove: dragging?', isDragging); // Keep this log minimal for now
    if (!isDragging) return;
    const cell = getCellFromMouseEvent(event);
    // console.log('[View] handleMouseMove: cell', cell);
    if (cell && onCellToggle) {
      if (cell.rowIndex !== lastToggledCellRef.current.r || cell.colIndex !== lastToggledCellRef.current.c) {
        onCellToggle(cell.rowIndex, cell.colIndex);
        lastToggledCellRef.current = { r: cell.rowIndex, c: cell.colIndex };
        // console.log('[View] handleMouseMove: onCellToggle called with', cell.rowIndex, cell.colIndex);
      }
    }
  }, [isDragging, onCellToggle, getCellFromMouseEvent]); // Added dependencies

  const handleMouseUp = useCallback(() => { setIsDragging(false); lastToggledCellRef.current = { r: -1, c: -1 }; }, []);
  const handleMouseLeave = useCallback(() => { setIsDragging(false); lastToggledCellRef.current = { r: -1, c: -1 }; }, []);

  const drawGrid = useCallback(() => {
    // ... (implementation as previously defined, using refs for gl, programInfo, quadBufferInfo) ...
    const gl = glRef.current;
    const programInfo = programInfoRef.current;
    const quadBufferInfo = quadBufferInfoRef.current;
    // console.log('[View] drawGrid: Called. currentGrid dimensions:', currentGrid ? currentGrid.length : 'null', currentGrid && currentGrid[0] ? currentGrid[0].length : 'null');
    if (!gl || !programInfo || !quadBufferInfo || !currentGrid || currentGrid.length === 0) { 
      if (gl) { // Attempt to clear if context is available but other resources are missing
        console.log('[View] drawGrid: Clearing canvas due to missing resources or invalid grid.');
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
      return; 
    }
    twgl.resizeCanvasToDisplaySize(gl.canvas);
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
    gl.clearColor(0.95, 0.95, 0.95, 1);
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
        twgl.setUniforms(programInfo, { u_matrix, u_color });
        twgl.drawBufferInfo(gl, quadBufferInfo);
      }
    }
  }, [currentGrid]); // Keep currentGrid as the main dependency for re-drawing the content

  useEffect(() => {
    console.log('[View] Mount/Resource Setup Effect running.');
    const canvas = canvasRef.current;
    if (!canvas) { console.error('[View] Canvas ref not available on mount.'); return; }
    const gl = canvas.getContext('webgl2');
    if (!gl) { setWebGLError('WebGL2 is not available.'); console.error('[View] Failed to get WebGL2 context.'); return; }
    glRef.current = gl;
    console.log('[View] WebGL context obtained.');
    const localProgramInfo = twgl.createProgramInfo(gl, [VS_QUAD, FS_COLOR]);
    if (!localProgramInfo || !localProgramInfo.program) {
      setWebGLError('Failed to compile/link shader program.');
      const log = gl.getProgramInfoLog(localProgramInfo && localProgramInfo.program); // Get log before potential nullification
      console.error('[View] Shader program creation failed:', log);
      glRef.current = null; return;
    }
    programInfoRef.current = localProgramInfo;
    console.log('[View] Shader program created.');
    const unitQuadVertices = [0,0, 1,0, 0,1,  0,1, 1,0, 1,1];
    quadBufferInfoRef.current = twgl.createBufferInfoFromArrays(gl, { a_position: { numComponents: 2, data: unitQuadVertices } });
    console.log('[View] Quad buffer created.');
    setWebGLError('');
    return () => {
      console.log('[View] Unmount/Resource Cleanup Effect running.');
      const currentGl = glRef.current;
      if (currentGl) {
        if (programInfoRef.current && programInfoRef.current.program) { currentGl.deleteProgram(programInfoRef.current.program); console.log('[View] Program deleted.'); }
        if (quadBufferInfoRef.current && quadBufferInfoRef.current.attribs && quadBufferInfoRef.current.attribs.a_position && quadBufferInfoRef.current.attribs.a_position.buffer) { currentGl.deleteBuffer(quadBufferInfoRef.current.attribs.a_position.buffer); console.log('[View] Buffer deleted.'); }
      }
      programInfoRef.current = null; quadBufferInfoRef.current = null; glRef.current = null; console.log('[View] GL Refs nullified.');
    };
  }, []);

  useEffect(() => {
    // console.log('[View] Drawing Effect triggered. currentGrid:', currentGrid ? `${currentGrid.length}x${currentGrid[0]?.length}` : 'null');
    if (glRef.current && programInfoRef.current && quadBufferInfoRef.current && currentGrid && currentGrid.length > 0) {
      drawGrid(); 
    } else {
      // console.log('[View] Drawing Effect: Not drawing - GL resources or grid not ready/valid.');
      const gl = glRef.current;
      if (gl && (!currentGrid || currentGrid.length === 0)) { /* console.log('[View] Drawing Effect: Clearing canvas due to empty/invalid grid.'); */ gl.clearColor(0.95, 0.95, 0.95, 1); gl.clear(gl.COLOR_BUFFER_BIT); }
    }
  }, [currentGrid, drawGrid]);

  useEffect(() => {
    const canvas = canvasRef.current; // Capture canvasRef.current for stable reference in cleanup
    const handleResize = () => {
      if (glRef.current && programInfoRef.current && quadBufferInfoRef.current && currentGrid && canvas === canvasRef.current) { // Check if canvas instance is the same
        // console.log('[View] Resize handler: Calling drawGrid.'); 
        drawGrid();
      } else { 
        // console.log('[View] Resize handler: Not drawing - GL resources or grid not ready, or canvas changed.');
      }
    };
    window.addEventListener('resize', handleResize);
    if (glRef.current && programInfoRef.current && quadBufferInfoRef.current && currentGrid) { 
      // console.log('[View] Resize useEffect: Initial resize call.'); 
      handleResize(); 
    }
    return () => window.removeEventListener('resize', handleResize);
  }, [drawGrid, currentGrid]);

  if (webGLError) { return <div style={{ width, height, border: '1px solid red', padding: '10px', color: 'red' }}><p>Error: {webGLError}</p></div>; }

  return <canvas ref={canvasRef} width={width} height={height} style={{ border: '1px solid #ccc', display: 'block', cursor: 'pointer' }} onMouseDown={handleMouseDown} onMouseMove={handleMouseMove} onMouseUp={handleMouseUp} onMouseLeave={handleMouseLeave} />;
};
export default Automaton2DView;
