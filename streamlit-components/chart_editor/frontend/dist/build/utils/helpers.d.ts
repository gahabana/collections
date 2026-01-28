/**
 * Helper utility functions
 */
import type { Lines, Line, Point, GridSnap, Range } from '../types/index.js';
/**
 * Deep clone a lines array (creates new objects)
 */
export declare function deepCloneLines(lines: Lines): Lines;
/**
 * Deep clone a single line
 */
export declare function deepCloneLine(line: Line): Line;
/**
 * Check if two line arrays are equal (by value)
 */
export declare function areLinesEqual(lines1: Lines, lines2: Lines): boolean;
/**
 * Apply grid snapping to a point
 */
export declare function applyGridSnap(point: Point, xRange: Range, yRange: Range, gridSnap: GridSnap): Point;
/**
 * Check if a point's X coordinate conflicts with existing points in a line
 * (too close to existing X value)
 */
export declare function hasConflictingX(line: Line, x: number, excludeIndex?: number, threshold?: number): boolean;
/**
 * Sort a line by X coordinate (modifies in place)
 */
export declare function sortLineByX(line: Line): Line;
/**
 * Get distance between two points
 */
export declare function distance(p1: Point, p2: Point): number;
/**
 * Clamp a value between min and max
 */
export declare function clamp(value: number, min: number, max: number): number;
/**
 * Linear interpolation between two values
 */
export declare function lerp(start: number, end: number, t: number): number;
/**
 * Convert serialized lines from Python to typed Lines
 */
export declare function deserializeLines(data: number[][][]): Lines;
/**
 * Convert typed Lines to serialized format for Python
 */
export declare function serializeLines(lines: Lines): number[][][];
/**
 * Check if value is a valid number (not NaN or Infinity)
 */
export declare function isValidNumber(value: unknown): value is number;
/**
 * Safely parse a number with fallback
 */
export declare function parseNumberSafe(value: string | number, fallback: number): number;
//# sourceMappingURL=helpers.d.ts.map