/**
 * Constants and configuration values for Chart Editor
 */

import type { Padding } from './core.js';

/**
 * Canvas padding (space for axes and labels)
 */
export const CANVAS_PADDING: Padding = {
  top: 40,
  right: 20,
  bottom: 50,
  left: 60
};

/**
 * Visual constants
 */
export const VISUAL = {
  /** Radius of point dots */
  DOT_RADIUS: 6,

  /** Radius for hover/click detection */
  HOVER_RADIUS: 12,

  /** Line width for drawing */
  LINE_WIDTH: 2,

  /** Grid line dash pattern */
  GRID_DASH: [5, 5] as [number, number],

  /** Axis line width */
  AXIS_WIDTH: 2,

  /** Overlap detection threshold (data units) */
  OVERLAP_THRESHOLD: 1,

  /** Number of grid lines */
  GRID_LINES: 10
} as const;

/**
 * Zoom configuration
 */
export const ZOOM = {
  /** Minimum zoom level (5% of original range) */
  MIN_ZOOM_PERCENT: 0.05,

  /** Maximum zoom level */
  MAX_ZOOM_LEVEL: 20,

  /** Zoom step factor for wheel (3% per tick) */
  WHEEL_ZOOM_FACTOR: 0.03,

  /** Zoom step for button zoom (20% of current range) */
  BUTTON_ZOOM_FACTOR: 0.2,

  /** Animation duration in milliseconds */
  ANIMATION_DURATION: 200,

  /** Fit to data padding (10% on each side) */
  FIT_PADDING_PERCENT: 0.1
} as const;

/**
 * History configuration
 */
export const HISTORY = {
  /** Maximum number of undo/redo steps */
  MAX_STACK_SIZE: 50
} as const;

/**
 * Keyboard navigation
 */
export const KEYBOARD = {
  /** Small step size (1% of range) */
  SMALL_STEP_PERCENT: 0.01,

  /** Large step size when Shift is pressed (5% of range) */
  LARGE_STEP_PERCENT: 0.05
} as const;

/**
 * Colors
 */
export const COLORS = {
  /** Grid lines */
  GRID: '#e0e0e0',

  /** Axis lines */
  AXIS: '#333',

  /** Background */
  BACKGROUND: '#fafafa',

  /** Text */
  TEXT: '#333',

  /** Hover effect */
  HOVER: 'rgba(0, 0, 0, 0.1)',

  /** Selected point outline */
  SELECTED: '#4ECDC4',

  /** Error flash */
  ERROR: '#FF6B6B',

  /** Overlap badge */
  OVERLAP_BADGE: '#333',
  OVERLAP_TEXT: '#fff'
} as const;

/**
 * Dark mode colors
 */
export const DARK_COLORS = {
  GRID: '#444',
  AXIS: '#e0e0e0',
  BACKGROUND: '#1e1e1e',
  TEXT: '#e0e0e0',
  HOVER: 'rgba(255, 255, 255, 0.1)'
} as const;

/**
 * Animation easing functions
 */
export const EASING = {
  /** Cubic ease-out: starts fast, ends slow */
  easeOutCubic: (t: number): number => 1 - Math.pow(1 - t, 3),

  /** Quadratic ease-in-out */
  easeInOutQuad: (t: number): number =>
    t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2
} as const;

/**
 * Timing constants
 */
export const TIMING = {
  /** Debounce delay for resize events (ms) */
  RESIZE_DEBOUNCE: 150,

  /** Error flash duration (ms) */
  ERROR_FLASH: 800,

  /** Invalid input highlight duration (ms) */
  INVALID_HIGHLIGHT: 1500
} as const;

/**
 * Default colors for lines (colorblind-friendly palette)
 */
export const DEFAULT_LINE_COLORS = [
  '#FF6B6B',  // Coral Red
  '#4ECDC4',  // Teal
  '#A55EEA',  // Purple
  '#45B7D1',  // Sky Blue
  '#F7DC6F',  // Yellow
  '#82E0AA',  // Green
  '#F8B500'   // Orange
] as const;
