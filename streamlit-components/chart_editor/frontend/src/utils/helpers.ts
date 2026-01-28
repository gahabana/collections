/**
 * Helper utility functions
 */

import type { Lines, Line, Point, GridSnap, Range } from '../types/index.js';

/**
 * Deep clone a lines array (creates new objects)
 */
export function deepCloneLines(lines: Lines): Lines {
  return lines.map(line =>
    line.map(point => ({ x: point.x, y: point.y }))
  );
}

/**
 * Deep clone a single line
 */
export function deepCloneLine(line: Line): Line {
  return line.map(point => ({ x: point.x, y: point.y }));
}

/**
 * Check if two line arrays are equal (by value)
 */
export function areLinesEqual(lines1: Lines, lines2: Lines): boolean {
  if (lines1.length !== lines2.length) return false;

  for (let i = 0; i < lines1.length; i++) {
    const line1 = lines1[i];
    const line2 = lines2[i];

    if (!line1 || !line2) return false;
    if (line1.length !== line2.length) return false;

    for (let j = 0; j < line1.length; j++) {
      const p1 = line1[j];
      const p2 = line2[j];
      if (!p1 || !p2) return false;
      if (p1.x !== p2.x || p1.y !== p2.y) return false;
    }
  }

  return true;
}

/**
 * Apply grid snapping to a point
 */
export function applyGridSnap(
  point: Point,
  xRange: Range,
  yRange: Range,
  gridSnap: GridSnap
): Point {
  const xRangeSize = xRange.max - xRange.min;
  const yRangeSize = yRange.max - yRange.min;

  const xStep = (gridSnap.x / 100) * xRangeSize;
  const yStep = (gridSnap.y / 100) * yRangeSize;

  return {
    x: xRange.min + Math.round((point.x - xRange.min) / xStep) * xStep,
    y: yRange.min + Math.round((point.y - yRange.min) / yStep) * yStep
  };
}

/**
 * Check if a point's X coordinate conflicts with existing points in a line
 * (too close to existing X value)
 */
export function hasConflictingX(
  line: Line,
  x: number,
  excludeIndex: number = -1,
  threshold: number = 1
): boolean {
  for (let i = 0; i < line.length; i++) {
    if (i === excludeIndex) continue;
    const point = line[i];
    if (!point) continue;
    if (Math.abs(point.x - x) < threshold) {
      return true;
    }
  }
  return false;
}

/**
 * Sort a line by X coordinate (modifies in place)
 */
export function sortLineByX(line: Line): Line {
  return line.sort((a, b) => a.x - b.x);
}

/**
 * Get distance between two points
 */
export function distance(p1: Point, p2: Point): number {
  return Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
}

/**
 * Clamp a value between min and max
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

/**
 * Linear interpolation between two values
 */
export function lerp(start: number, end: number, t: number): number {
  return start + (end - start) * t;
}

/**
 * Convert serialized lines from Python to typed Lines
 */
export function deserializeLines(data: number[][][]): Lines {
  return data.map(line =>
    line.map(coords => ({
      x: coords[0] ?? 0,
      y: coords[1] ?? 0
    }))
  );
}

/**
 * Convert typed Lines to serialized format for Python
 */
export function serializeLines(lines: Lines): number[][][] {
  return lines.map(line =>
    line.map(point => [point.x, point.y])
  );
}

/**
 * Check if value is a valid number (not NaN or Infinity)
 */
export function isValidNumber(value: unknown): value is number {
  return typeof value === 'number' && isFinite(value);
}

/**
 * Safely parse a number with fallback
 */
export function parseNumberSafe(value: string | number, fallback: number): number {
  const parsed = typeof value === 'string' ? parseFloat(value) : value;
  return isValidNumber(parsed) ? parsed : fallback;
}
