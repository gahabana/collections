/**
 * Internal state types for Chart Editor component
 */

import type { Lines, Point, PointReference, RangeTuple } from './core.js';

/**
 * Touch interaction state for pinch-to-zoom
 */
export interface TouchState {
  touches: Touch[];
  initialPinchDistance: number | null;
  initialZoomLevel: number;
  initialXRange: RangeTuple | null;
  initialYRange: RangeTuple | null;
  pinchCenter: Point | null;
}

/**
 * Range selector (zoom brush) state
 */
export interface RangeSelectorState {
  enabled: boolean;
  dragging: 'viewport' | 'left' | 'right' | null;
  dragStartX: number;
  dragStartLeft: number;
  dragStartWidth: number;
}

/**
 * History entry for undo/redo
 */
export interface HistoryEntry {
  lines: Lines;
  timestamp: number;
}

/**
 * Editor state flags
 */
export interface EditorFlags {
  isEditing: boolean;
  isDragging: boolean;
  isPanning: boolean;
}

/**
 * Pan state
 */
export interface PanState {
  panStartX: number;
  panStartY: number;
  panStartXRange: RangeTuple;
  panStartYRange: RangeTuple;
}

/**
 * Animation state
 */
export interface AnimationState {
  zoomAnimationId: number | null;
  animating: boolean;
}

/**
 * Mouse/keyboard interaction state
 */
export interface InteractionState {
  hoveredPoint: PointReference | null;
  draggingPoint: PointReference | null;
  selectedPoint: PointReference | null;
}

/**
 * Complete internal state of the Chart Editor
 */
export interface ChartEditorState extends EditorFlags, InteractionState, AnimationState {
  // Data
  lines: Lines;
  savedLines: Lines;

  // Ranges
  xRange: RangeTuple;
  yRange: RangeTuple;
  originalXRange: RangeTuple;
  originalYRange: RangeTuple;

  // Active line
  activeLineIndex: number;

  // Zoom
  zoomLevel: number;

  // History
  historyStack: Lines[];
  historyIndex: number;

  // Touch
  touchState: TouchState;

  // Range selector
  rangeSelector: RangeSelectorState;

  // Pan
  panState: PanState | null;
}
