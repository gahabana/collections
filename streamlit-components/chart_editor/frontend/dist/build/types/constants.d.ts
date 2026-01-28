/**
 * Constants and configuration values for Chart Editor
 */
import type { Padding } from './core.js';
/**
 * Canvas padding (space for axes and labels)
 */
export declare const CANVAS_PADDING: Padding;
/**
 * Visual constants
 */
export declare const VISUAL: {
    /** Radius of point dots */
    readonly DOT_RADIUS: 6;
    /** Radius for hover/click detection */
    readonly HOVER_RADIUS: 12;
    /** Line width for drawing */
    readonly LINE_WIDTH: 2;
    /** Grid line dash pattern */
    readonly GRID_DASH: [number, number];
    /** Axis line width */
    readonly AXIS_WIDTH: 2;
    /** Overlap detection threshold (data units) */
    readonly OVERLAP_THRESHOLD: 1;
    /** Number of grid lines */
    readonly GRID_LINES: 10;
};
/**
 * Zoom configuration
 */
export declare const ZOOM: {
    /** Minimum zoom level (5% of original range) */
    readonly MIN_ZOOM_PERCENT: 0.05;
    /** Maximum zoom level */
    readonly MAX_ZOOM_LEVEL: 20;
    /** Zoom step factor for wheel (3% per tick) */
    readonly WHEEL_ZOOM_FACTOR: 0.03;
    /** Zoom step for button zoom (20% of current range) */
    readonly BUTTON_ZOOM_FACTOR: 0.2;
    /** Animation duration in milliseconds */
    readonly ANIMATION_DURATION: 200;
    /** Fit to data padding (10% on each side) */
    readonly FIT_PADDING_PERCENT: 0.1;
};
/**
 * History configuration
 */
export declare const HISTORY: {
    /** Maximum number of undo/redo steps */
    readonly MAX_STACK_SIZE: 50;
};
/**
 * Keyboard navigation
 */
export declare const KEYBOARD: {
    /** Small step size (1% of range) */
    readonly SMALL_STEP_PERCENT: 0.01;
    /** Large step size when Shift is pressed (5% of range) */
    readonly LARGE_STEP_PERCENT: 0.05;
};
/**
 * Colors
 */
export declare const COLORS: {
    /** Grid lines */
    readonly GRID: "#e0e0e0";
    /** Axis lines */
    readonly AXIS: "#333";
    /** Background */
    readonly BACKGROUND: "#fafafa";
    /** Text */
    readonly TEXT: "#333";
    /** Hover effect */
    readonly HOVER: "rgba(0, 0, 0, 0.1)";
    /** Selected point outline */
    readonly SELECTED: "#4ECDC4";
    /** Error flash */
    readonly ERROR: "#FF6B6B";
    /** Overlap badge */
    readonly OVERLAP_BADGE: "#333";
    readonly OVERLAP_TEXT: "#fff";
};
/**
 * Dark mode colors
 */
export declare const DARK_COLORS: {
    readonly GRID: "#444";
    readonly AXIS: "#e0e0e0";
    readonly BACKGROUND: "#1e1e1e";
    readonly TEXT: "#e0e0e0";
    readonly HOVER: "rgba(255, 255, 255, 0.1)";
};
/**
 * Animation easing functions
 */
export declare const EASING: {
    /** Cubic ease-out: starts fast, ends slow */
    readonly easeOutCubic: (t: number) => number;
    /** Quadratic ease-in-out */
    readonly easeInOutQuad: (t: number) => number;
};
/**
 * Timing constants
 */
export declare const TIMING: {
    /** Debounce delay for resize events (ms) */
    readonly RESIZE_DEBOUNCE: 150;
    /** Error flash duration (ms) */
    readonly ERROR_FLASH: 800;
    /** Invalid input highlight duration (ms) */
    readonly INVALID_HIGHLIGHT: 1500;
};
/**
 * Default colors for lines (colorblind-friendly palette)
 */
export declare const DEFAULT_LINE_COLORS: readonly ["#FF6B6B", "#4ECDC4", "#A55EEA", "#45B7D1", "#F7DC6F", "#82E0AA", "#F8B500"];
//# sourceMappingURL=constants.d.ts.map