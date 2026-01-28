/**
 * Coordinate transformation utilities
 * Handles conversion between data space and canvas space
 */

import type { Point, CanvasPoint, Padding, RangeTuple } from '../types/index.js';

/**
 * Convert data coordinates to canvas coordinates
 */
export function dataToCanvas(
  dataPoint: Point,
  xRange: RangeTuple,
  yRange: RangeTuple,
  canvasWidth: number,
  canvasHeight: number,
  padding: Padding
): CanvasPoint {
  const chartWidth = canvasWidth - padding.left - padding.right;
  const chartHeight = canvasHeight - padding.top - padding.bottom;

  // Guard against division by zero
  const xRangeSize = xRange[1] - xRange[0];
  const yRangeSize = yRange[1] - yRange[0];

  if (xRangeSize === 0 || yRangeSize === 0) {
    return { x: padding.left, y: padding.top };
  }

  const x = padding.left +
    ((dataPoint.x - xRange[0]) / xRangeSize) * chartWidth;

  const y = canvasHeight - padding.bottom -
    ((dataPoint.y - yRange[0]) / yRangeSize) * chartHeight;

  return { x, y };
}

/**
 * Convert canvas coordinates to data coordinates
 */
export function canvasToData(
  canvasPoint: CanvasPoint,
  xRange: RangeTuple,
  yRange: RangeTuple,
  canvasWidth: number,
  canvasHeight: number,
  padding: Padding
): Point {
  const chartWidth = canvasWidth - padding.left - padding.right;
  const chartHeight = canvasHeight - padding.top - padding.bottom;

  // Guard against division by zero
  if (chartWidth === 0 || chartHeight === 0) {
    return { x: xRange[0], y: yRange[0] };
  }

  const x = xRange[0] +
    ((canvasPoint.x - padding.left) / chartWidth) * (xRange[1] - xRange[0]);

  const y = yRange[0] +
    ((canvasHeight - padding.bottom - canvasPoint.y) / chartHeight) * (yRange[1] - yRange[0]);

  return { x, y };
}

/**
 * Check if canvas coordinates are within the chart area
 */
export function isInChartArea(
  canvasPoint: CanvasPoint,
  canvasWidth: number,
  canvasHeight: number,
  padding: Padding
): boolean {
  return (
    canvasPoint.x >= padding.left &&
    canvasPoint.x <= canvasWidth - padding.right &&
    canvasPoint.y >= padding.top &&
    canvasPoint.y <= canvasHeight - padding.bottom
  );
}

/**
 * Get chart dimensions (excluding padding)
 */
export function getChartDimensions(
  canvasWidth: number,
  canvasHeight: number,
  padding: Padding
): { width: number; height: number } {
  return {
    width: canvasWidth - padding.left - padding.right,
    height: canvasHeight - padding.top - padding.bottom
  };
}

/**
 * Convert mouse/touch event to canvas coordinates
 */
export function eventToCanvasCoords(
  event: { clientX: number; clientY: number },
  canvas: HTMLCanvasElement
): CanvasPoint {
  const rect = canvas.getBoundingClientRect();
  return {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  };
}

/**
 * Get pinch distance between two touch points
 */
export function getPinchDistance(touch1: Touch, touch2: Touch): number {
  const dx = touch2.clientX - touch1.clientX;
  const dy = touch2.clientY - touch1.clientY;
  return Math.sqrt(dx * dx + dy * dy);
}

/**
 * Get center point of a pinch gesture
 */
export function getPinchCenter(
  touch1: Touch,
  touch2: Touch,
  canvas: HTMLCanvasElement
): CanvasPoint {
  const centerX = (touch1.clientX + touch2.clientX) / 2;
  const centerY = (touch1.clientY + touch2.clientY) / 2;
  return eventToCanvasCoords({ clientX: centerX, clientY: centerY }, canvas);
}
