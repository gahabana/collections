/**
 * Type definitions index
 * Central export point for all TypeScript types
 */

// Core types
export type {
  Point,
  Line,
  Lines,
  Range,
  RangeTuple,
  GridSnap,
  GridSnapTuple,
  Color,
  ColorList,
  Padding,
  PointReference,
  CanvasPoint,
  Position
} from './core.js';

// Configuration types
export type {
  ChartConfig,
  ZoomState,
  ZoomCallbackData,
  StreamlitMessage,
  StreamlitRenderEvent
} from './config.js';

// State types
export type {
  TouchState,
  RangeSelectorState,
  HistoryEntry,
  EditorFlags,
  PanState,
  AnimationState,
  InteractionState,
  ChartEditorState
} from './state.js';

// Constants
export {
  CANVAS_PADDING,
  VISUAL,
  ZOOM,
  HISTORY,
  KEYBOARD,
  COLORS,
  DARK_COLORS,
  EASING,
  TIMING,
  DEFAULT_LINE_COLORS
} from './constants.js';
