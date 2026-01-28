/**
 * Drawing utilities for ChartEditor
 * Canvas rendering functions
 */

import type { Lines, Point, PointReference, RangeTuple, Padding, ColorList } from '../types/index.js';
import { VISUAL, COLORS } from '../types/index.js';
import { dataToCanvas } from '../utils/index.js';

/**
 * Find overlapping points in all lines
 */
export function findOverlappingPoints(
  lines: Lines,
  xRange: RangeTuple,
  yRange: RangeTuple
): Map<string, PointReference[]> {
  const overlaps = new Map<string, PointReference[]>();

  // Grid cell size for grouping (1% of range)
  const xRangeSize = xRange[1] - xRange[0];
  const yRangeSize = yRange[1] - yRange[0];

  // Guard against zero range - use fallback cell sizes
  const xCell = xRangeSize > 0 ? xRangeSize * 0.01 : 1;
  const yCell = yRangeSize > 0 ? yRangeSize * 0.01 : 1;

  // Group points into grid cells
  lines.forEach((line, lineIndex) => {
    line.forEach((point, pointIndex) => {
      const cellX = Math.floor(point.x / xCell);
      const cellY = Math.floor(point.y / yCell);
      const key = `${cellX},${cellY}`;

      const group = overlaps.get(key) || [];
      group.push({ lineIndex, pointIndex });
      overlaps.set(key, group);
    });
  });

  // Filter out non-overlapping groups
  const result = new Map<string, PointReference[]>();
  overlaps.forEach((group, key) => {
    if (group.length > 1) {
      result.set(key, group);
    }
  });

  return result;
}

/**
 * Draw the grid lines
 */
export function drawGrid(
  ctx: CanvasRenderingContext2D,
  xRange: RangeTuple,
  yRange: RangeTuple,
  canvasWidth: number,
  canvasHeight: number,
  padding: Padding
): void {
  const chartWidth = canvasWidth - padding.left - padding.right;
  const chartHeight = canvasHeight - padding.top - padding.bottom;

  ctx.strokeStyle = COLORS.GRID;
  ctx.lineWidth = 1;
  ctx.setLineDash(VISUAL.GRID_DASH);

  // Vertical grid lines
  for (let i = 0; i <= VISUAL.GRID_LINES; i++) {
    const x = padding.left + (chartWidth / VISUAL.GRID_LINES) * i;
    ctx.beginPath();
    ctx.moveTo(x, padding.top);
    ctx.lineTo(x, canvasHeight - padding.bottom);
    ctx.stroke();
  }

  // Horizontal grid lines
  for (let i = 0; i <= VISUAL.GRID_LINES; i++) {
    const y = padding.top + (chartHeight / VISUAL.GRID_LINES) * i;
    ctx.beginPath();
    ctx.moveTo(padding.left, y);
    ctx.lineTo(canvasWidth - padding.right, y);
    ctx.stroke();
  }

  ctx.setLineDash([]);
}

/**
 * Draw the axes
 */
export function drawAxes(
  ctx: CanvasRenderingContext2D,
  xRange: RangeTuple,
  yRange: RangeTuple,
  canvasWidth: number,
  canvasHeight: number,
  padding: Padding
): void {
  const chartWidth = canvasWidth - padding.left - padding.right;
  const chartHeight = canvasHeight - padding.top - padding.bottom;

  ctx.strokeStyle = COLORS.AXIS;
  ctx.fillStyle = COLORS.TEXT;
  ctx.lineWidth = VISUAL.AXIS_WIDTH;
  ctx.font = '12px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';

  // Y-axis
  ctx.beginPath();
  ctx.moveTo(padding.left, padding.top);
  ctx.lineTo(padding.left, canvasHeight - padding.bottom);
  ctx.stroke();

  // X-axis
  ctx.beginPath();
  ctx.moveTo(padding.left, canvasHeight - padding.bottom);
  ctx.lineTo(canvasWidth - padding.right, canvasHeight - padding.bottom);
  ctx.stroke();

  // Y-axis labels
  ctx.textAlign = 'right';
  ctx.textBaseline = 'middle';
  for (let i = 0; i <= VISUAL.GRID_LINES; i++) {
    const y = padding.top + (chartHeight / VISUAL.GRID_LINES) * i;
    const value = yRange[1] - ((yRange[1] - yRange[0]) / VISUAL.GRID_LINES) * i;
    ctx.fillText(value.toFixed(0), padding.left - 8, y);
  }

  // X-axis labels
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';
  for (let i = 0; i <= VISUAL.GRID_LINES; i++) {
    const x = padding.left + (chartWidth / VISUAL.GRID_LINES) * i;
    const value = xRange[0] + ((xRange[1] - xRange[0]) / VISUAL.GRID_LINES) * i;
    ctx.fillText(value.toFixed(0), x, canvasHeight - padding.bottom + 8);
  }
}

/**
 * Draw a single line
 */
export function drawLine(
  ctx: CanvasRenderingContext2D,
  line: Point[],
  color: string,
  xRange: RangeTuple,
  yRange: RangeTuple,
  canvasWidth: number,
  canvasHeight: number,
  padding: Padding
): void {
  if (line.length === 0) return;

  ctx.strokeStyle = color;
  ctx.lineWidth = VISUAL.LINE_WIDTH;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';

  ctx.beginPath();
  const firstCanvas = dataToCanvas(line[0]!, xRange, yRange, canvasWidth, canvasHeight, padding);
  ctx.moveTo(firstCanvas.x, firstCanvas.y);

  for (let i = 1; i < line.length; i++) {
    const point = line[i];
    if (!point) continue;
    const canvasPoint = dataToCanvas(point, xRange, yRange, canvasWidth, canvasHeight, padding);
    ctx.lineTo(canvasPoint.x, canvasPoint.y);
  }

  ctx.stroke();
}

/**
 * Draw a point dot
 */
export function drawPoint(
  ctx: CanvasRenderingContext2D,
  point: Point,
  color: string,
  xRange: RangeTuple,
  yRange: RangeTuple,
  canvasWidth: number,
  canvasHeight: number,
  padding: Padding,
  options: {
    isHovered?: boolean;
    isDragging?: boolean;
    isSelected?: boolean;
    isOverlapping?: boolean;
  } = {}
): void {
  const canvasPoint = dataToCanvas(point, xRange, yRange, canvasWidth, canvasHeight, padding);
  const radius = VISUAL.DOT_RADIUS;

  // Selected indicator (keyboard navigation)
  if (options.isSelected) {
    ctx.beginPath();
    ctx.arc(canvasPoint.x, canvasPoint.y, radius + 8, 0, Math.PI * 2);
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.setLineDash([4, 4]);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // Hover background
  if (options.isHovered || options.isDragging) {
    ctx.beginPath();
    ctx.arc(canvasPoint.x, canvasPoint.y, radius + 4, 0, Math.PI * 2);
    ctx.fillStyle = COLORS.HOVER;
    ctx.fill();
  }

  // Main dot
  ctx.beginPath();
  ctx.arc(canvasPoint.x, canvasPoint.y, radius, 0, Math.PI * 2);
  ctx.fillStyle = options.isDragging ? '#fff' : color;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.fill();
  ctx.stroke();

  // Overlap badge
  if (options.isOverlapping) {
    const badgeX = canvasPoint.x + radius + 4;
    const badgeY = canvasPoint.y - radius - 4;

    ctx.beginPath();
    ctx.arc(badgeX, badgeY, 8, 0, Math.PI * 2);
    ctx.fillStyle = COLORS.OVERLAP_BADGE;
    ctx.fill();

    ctx.fillStyle = COLORS.OVERLAP_TEXT;
    ctx.font = 'bold 11px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('!', badgeX, badgeY);
  }
}
