/**
 * Drawing utilities for ChartEditor
 * Canvas rendering functions
 */
import type { Lines, Point, PointReference, RangeTuple, Padding } from '../types/index.js';
/**
 * Find overlapping points in all lines
 */
export declare function findOverlappingPoints(lines: Lines, xRange: RangeTuple, yRange: RangeTuple): Map<string, PointReference[]>;
/**
 * Draw the grid lines
 */
export declare function drawGrid(ctx: CanvasRenderingContext2D, _xRange: RangeTuple, _yRange: RangeTuple, canvasWidth: number, canvasHeight: number, padding: Padding): void;
/**
 * Draw the axes
 */
export declare function drawAxes(ctx: CanvasRenderingContext2D, xRange: RangeTuple, yRange: RangeTuple, canvasWidth: number, canvasHeight: number, padding: Padding): void;
/**
 * Draw a single line
 */
export declare function drawLine(ctx: CanvasRenderingContext2D, line: Point[], color: string, xRange: RangeTuple, yRange: RangeTuple, canvasWidth: number, canvasHeight: number, padding: Padding): void;
/**
 * Draw a point dot
 */
export declare function drawPoint(ctx: CanvasRenderingContext2D, point: Point, color: string, xRange: RangeTuple, yRange: RangeTuple, canvasWidth: number, canvasHeight: number, padding: Padding, options?: {
    isHovered?: boolean;
    isDragging?: boolean;
    isSelected?: boolean;
    isOverlapping?: boolean;
}): void;
//# sourceMappingURL=drawing.d.ts.map