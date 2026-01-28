/**
 * Utilities index
 * Central export point for all utility functions
 */

// Helper functions
export {
  deepCloneLines,
  deepCloneLine,
  areLinesEqual,
  applyGridSnap,
  hasConflictingX,
  sortLineByX,
  distance,
  clamp,
  lerp,
  deserializeLines,
  serializeLines,
  isValidNumber,
  parseNumberSafe
} from './helpers.js';

// Coordinate transformations
export {
  dataToCanvas,
  canvasToData,
  isInChartArea,
  getChartDimensions,
  eventToCanvasCoords,
  getPinchDistance,
  getPinchCenter
} from './coordinates.js';

// Streamlit communication
export {
  sendMessageToStreamlit,
  setComponentValue,
  sendZoomState,
  setFrameHeight,
  setComponentReady,
  isInStreamlit,
  onStreamlitRender
} from './streamlit.js';
