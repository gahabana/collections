/**
 * Coordinate transformation utilities
 * Handles conversion between data space and canvas space
 */
import type { Point, CanvasPoint, Padding, RangeTuple } from '../types/index.js';
/**
 * Convert data coordinates to canvas coordinates
 */
export declare function dataToCanvas(dataPoint: Point, xRange: RangeTuple, yRange: RangeTuple, canvasWidth: number, canvasHeight: number, padding: Padding): CanvasPoint;
/**
 * Convert canvas coordinates to data coordinates
 */
export declare function canvasToData(canvasPoint: CanvasPoint, xRange: RangeTuple, yRange: RangeTuple, canvasWidth: number, canvasHeight: number, padding: Padding): Point;
/**
 * Check if canvas coordinates are within the chart area
 */
export declare function isInChartArea(canvasPoint: CanvasPoint, canvasWidth: number, canvasHeight: number, padding: Padding): boolean;
/**
 * Get chart dimensions (excluding padding)
 */
export declare function getChartDimensions(canvasWidth: number, canvasHeight: number, padding: Padding): {
    width: number;
    height: number;
};
/**
 * Convert mouse/touch event to canvas coordinates
 */
export declare function eventToCanvasCoords(event: {
    clientX: number;
    clientY: number;
}, canvas: HTMLCanvasElement): CanvasPoint;
/**
 * Get pinch distance between two touch points
 */
export declare function getPinchDistance(touch1: Touch, touch2: Touch): number;
/**
 * Get center point of a pinch gesture
 */
export declare function getPinchCenter(touch1: Touch, touch2: Touch, canvas: HTMLCanvasElement): CanvasPoint;
//# sourceMappingURL=coordinates.d.ts.map