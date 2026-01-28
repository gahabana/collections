/**
 * Core data types for the Chart Editor component
 */

/**
 * A single point in 2D space
 */
export interface Point {
  x: number;
  y: number;
}

/**
 * A line is an array of points
 */
export type Line = Point[];

/**
 * Multiple lines
 */
export type Lines = Line[];

/**
 * A range with min and max values
 */
export interface Range {
  min: number;
  max: number;
}

/**
 * Alternative range representation as tuple
 */
export type RangeTuple = [number, number];

/**
 * Grid snap configuration as percentages
 */
export interface GridSnap {
  x: number; // X-axis snap percentage
  y: number; // Y-axis snap percentage
}

/**
 * Alternative grid snap as tuple
 */
export type GridSnapTuple = [number, number];

/**
 * Color string (hex format)
 */
export type Color = string;

/**
 * Array of colors for multiple lines
 */
export type ColorList = Color[];

/**
 * Canvas padding configuration
 */
export interface Padding {
  top: number;
  right: number;
  bottom: number;
  left: number;
}

/**
 * Point reference (line index + point index)
 */
export interface PointReference {
  lineIndex: number;
  pointIndex: number;
}

/**
 * Canvas coordinates
 */
export interface CanvasPoint {
  x: number;
  y: number;
}

/**
 * Mouse/Touch position
 */
export interface Position {
  clientX: number;
  clientY: number;
}
