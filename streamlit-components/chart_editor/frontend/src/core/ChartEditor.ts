/**
 * ChartEditor - Main class for the interactive chart editor component
 *
 * This class manages:
 * - Canvas rendering and drawing
 * - User interactions (mouse, touch, keyboard)
 * - Zoom and pan functionality
 * - Undo/redo history
 * - State management and Streamlit communication
 */

import type {
  Lines,
  Line,
  Point,
  PointReference,
  ChartConfig,
  RangeTuple,
  GridSnapTuple,
  ColorList
} from '../types/index.js';

import {
  CANVAS_PADDING,
  VISUAL,
  ZOOM,
  HISTORY,
  KEYBOARD,
  COLORS,
  EASING
} from '../types/index.js';

import {
  deepCloneLines,
  applyGridSnap,
  hasConflictingX,
  sortLineByX,
  areLinesEqual,
  dataToCanvas,
  canvasToData,
  isInChartArea,
  eventToCanvasCoords,
  getPinchDistance,
  getPinchCenter,
  setComponentValue,
  sendZoomState
} from '../utils/index.js';

import { debugLogger } from '../debug/index.js';
import { findOverlappingPoints, drawGrid, drawAxes, drawLine, drawPoint } from './drawing.js';

/**
 * Main ChartEditor class
 */
export class ChartEditor {
  // DOM elements
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;

  // Configuration
  private colors: ColorList = [];
  private gridSnap: GridSnapTuple | null = null;
  private disabled: boolean = false;
  private minPoints: number = 0;
  private maxPoints: number | null = null;
  private zoomEnabled: boolean = false;
  private readOnly: boolean = false;

  // Data state
  private lines: Lines = [];
  private savedLines: Lines = [];

  // Ranges
  private xRange: RangeTuple = [0, 100];
  private yRange: RangeTuple = [0, 1000];
  private originalXRange: RangeTuple = [0, 100];
  private originalYRange: RangeTuple = [0, 1000];

  // Active line
  private activeLineIndex: number = 0;

  // Interaction state
  private hoveredPoint: PointReference | null = null;
  private draggingPoint: PointReference | null = null;
  private selectedPoint: PointReference | null = null;

  // Edit state
  private isEditing: boolean = false;
  private isDragging: boolean = false;

  // Zoom state
  private zoomLevel: number = 1;
  private zoomAnimationId: number | null = null;

  // Pan state
  private isPanning: boolean = false;
  private panStartX: number = 0;
  private panStartY: number = 0;
  private panStartXRange: RangeTuple = [0, 0];
  private panStartYRange: RangeTuple = [0, 0];

  // History (undo/redo)
  private historyStack: Lines[] = [];
  private historyIndex: number = -1;

  // Touch state
  private touchState = {
    touches: [] as Touch[],
    initialPinchDistance: null as number | null,
    initialZoomLevel: 1,
    initialXRange: null as RangeTuple | null,
    initialYRange: null as RangeTuple | null,
    pinchCenter: null as { x: number; y: number } | null
  };

  // Range selector state
  private rangeSelector = {
    enabled: false,
    dragging: null as 'viewport' | 'left' | 'right' | null,
    dragStartX: 0,
    dragStartLeft: 0,
    dragStartWidth: 0
  };

  // Visual constants
  private readonly padding = CANVAS_PADDING;
  private readonly dotRadius = VISUAL.DOT_RADIUS;
  private readonly hoverRadius = VISUAL.HOVER_RADIUS;

  // Callbacks
  private onZoomCallback: ((data: { xRange: RangeTuple; yRange: RangeTuple; zoomLevel: number }) => void) | null = null;

  /**
   * Constructor - Initialize the ChartEditor
   */
  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    const context = canvas.getContext('2d');

    if (!context) {
      throw new Error('Failed to get 2D context from canvas');
    }

    this.ctx = context;

    debugLogger.log('EDITOR_INIT', 'ChartEditor initialized');

    // Bind event handlers
    this.handleMouseMove = this.handleMouseMove.bind(this);
    this.handleMouseDown = this.handleMouseDown.bind(this);
    this.handleMouseUp = this.handleMouseUp.bind(this);
    this.handleMouseLeave = this.handleMouseLeave.bind(this);
    this.handleWheel = this.handleWheel.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.handleTouchStart = this.handleTouchStart.bind(this);
    this.handleTouchMove = this.handleTouchMove.bind(this);
    this.handleTouchEnd = this.handleTouchEnd.bind(this);

    // Attach event listeners
    this.attachEventListeners();
  }

  /**
   * Attach all event listeners to the canvas
   */
  private attachEventListeners(): void {
    this.canvas.addEventListener('mousemove', this.handleMouseMove);
    this.canvas.addEventListener('mousedown', this.handleMouseDown);
    this.canvas.addEventListener('mouseup', this.handleMouseUp);
    this.canvas.addEventListener('mouseleave', this.handleMouseLeave);
    this.canvas.addEventListener('wheel', this.handleWheel, { passive: false });

    // Touch events
    this.canvas.addEventListener('touchstart', this.handleTouchStart, { passive: false });
    this.canvas.addEventListener('touchmove', this.handleTouchMove, { passive: false });
    this.canvas.addEventListener('touchend', this.handleTouchEnd, { passive: false });

    // Keyboard events
    this.canvas.setAttribute('tabindex', '0');
    this.canvas.addEventListener('keydown', this.handleKeyDown);

    debugLogger.log('EVENTS_ATTACHED', 'Event listeners attached to canvas');
  }

  /**
   * Set or update the chart configuration
   */
  setConfig(config: ChartConfig): void {
    debugLogger.log('CONFIG_UPDATE', {
      lines: config.lines.length,
      xRange: config.xRange,
      yRange: config.yRange
    });

    // Update data
    this.lines = config.lines.map(line =>
      line.map(p => ({ x: p.x, y: p.y }))
    );
    this.savedLines = deepCloneLines(this.lines);

    // Ensure at least one line exists
    if (this.lines.length === 0) {
      this.lines.push([]);
    }

    // Update ranges
    this.xRange = [...config.xRange];
    this.yRange = [...config.yRange];
    this.originalXRange = [...config.xRange];
    this.originalYRange = [...config.yRange];

    // Update configuration
    this.colors = config.colors;
    this.gridSnap = config.gridSnap;
    this.disabled = config.disabled;
    this.minPoints = config.minPoints;
    this.maxPoints = config.maxPoints;
    this.zoomEnabled = config.zoomEnabled;
    this.readOnly = config.readOnly;

    // Update canvas size
    this.canvas.width = config.width;
    this.canvas.height = config.height;

    // Reset zoom level
    this.zoomLevel = 1;

    // Initialize history
    this.initHistory();

    // Initial draw
    this.draw();
  }

  /**
   * Get the current lines data
   */
  getLines(): Lines {
    return deepCloneLines(this.lines);
  }

  /**
   * Set zoom callback
   */
  setOnZoomCallback(callback: (data: { xRange: RangeTuple; yRange: RangeTuple; zoomLevel: number }) => void): void {
    this.onZoomCallback = callback;
  }

  // ============================================
  // HISTORY SYSTEM (Undo/Redo)
  // ============================================

  /**
   * Initialize history with current state
   */
  private initHistory(): void {
    this.historyStack = [deepCloneLines(this.lines)];
    this.historyIndex = 0;
    debugLogger.log('HISTORY_INIT', { stackSize: 1 });
  }

  /**
   * Push current state to history
   */
  private pushHistory(): void {
    // Remove any redo states
    if (this.historyIndex < this.historyStack.length - 1) {
      this.historyStack = this.historyStack.slice(0, this.historyIndex + 1);
    }

    // Add current state
    this.historyStack.push(deepCloneLines(this.lines));
    this.historyIndex = this.historyStack.length - 1;

    // Limit history size
    if (this.historyStack.length > HISTORY.MAX_STACK_SIZE) {
      this.historyStack.shift();
      this.historyIndex--;
    }

    debugLogger.log('HISTORY_PUSH', {
      index: this.historyIndex,
      stackSize: this.historyStack.length
    });
  }

  /**
   * Undo last action
   */
  undo(): boolean {
    if (this.historyIndex <= 0) return false;

    this.historyIndex--;
    const historyEntry = this.historyStack[this.historyIndex];
    if (!historyEntry) return false;

    this.lines = deepCloneLines(historyEntry);
    this.draw();

    debugLogger.log('UNDO', {
      historyIndex: this.historyIndex,
      stackSize: this.historyStack.length
    });

    return true;
  }

  /**
   * Redo last undone action
   */
  redo(): boolean {
    if (this.historyIndex >= this.historyStack.length - 1) return false;

    this.historyIndex++;
    const historyEntry = this.historyStack[this.historyIndex];
    if (!historyEntry) return false;

    this.lines = deepCloneLines(historyEntry);
    this.draw();

    debugLogger.log('REDO', {
      historyIndex: this.historyIndex,
      stackSize: this.historyStack.length
    });

    return true;
  }

  /**
   * Check if undo is available
   */
  canUndo(): boolean {
    return this.historyIndex > 0;
  }

  /**
   * Check if redo is available
   */
  canRedo(): boolean {
    return this.historyIndex < this.historyStack.length - 1;
  }

  /**
   * Enter edit mode
   */
  private enterEditMode(): void {
    if (this.isEditing) return;
    this.isEditing = true;
    this.canvas.classList.add('editing');
    debugLogger.log('EDIT_MODE', 'Entered edit mode');
  }

  /**
   * Save changes and exit edit mode
   */
  saveChanges(): void {
    const serialized = this.lines.map(line => line.map(p => [p.x, p.y]));
    setComponentValue(this.lines);
    this.savedLines = deepCloneLines(this.lines);
    this.isEditing = false;
    this.canvas.classList.remove('editing');
    debugLogger.log('CHANGES_SAVED', { lines: this.lines.length });
  }

  // ============================================
  // DRAWING
  // ============================================

  /**
   * Main draw method - renders the entire chart
   */
  private draw(): void {
    const { width, height } = this.canvas;
    const ctx = this.ctx;

    // Clear canvas
    ctx.fillStyle = COLORS.BACKGROUND;
    ctx.fillRect(0, 0, width, height);

    // Setup clipping region for chart area
    const chartWidth = width - this.padding.left - this.padding.right;
    const chartHeight = height - this.padding.top - this.padding.bottom;

    // Draw grid
    drawGrid(ctx, this.xRange, this.yRange, width, height, this.padding);

    // Draw axes
    drawAxes(ctx, this.xRange, this.yRange, width, height, this.padding);

    // Find overlapping points
    const overlaps = findOverlappingPoints(this.lines, this.xRange, this.yRange);
    const overlappingSet = new Set<string>();
    overlaps.forEach(points => {
      points.forEach(p => overlappingSet.add(`${p.lineIndex},${p.pointIndex}`));
    });

    // Clip drawing to chart area
    ctx.save();
    ctx.beginPath();
    ctx.rect(
      this.padding.left,
      this.padding.top,
      chartWidth,
      chartHeight
    );
    ctx.clip();

    // Draw all lines and points
    this.lines.forEach((line, lineIndex) => {
      if (line.length === 0) return;

      const color = this.colors[lineIndex] || COLORS.TEXT;
      const isActive = lineIndex === this.activeLineIndex;

      // Draw line with reduced opacity if not active
      ctx.globalAlpha = isActive ? 1 : 0.3;
      drawLine(ctx, line, color, this.xRange, this.yRange, width, height, this.padding);
      ctx.globalAlpha = 1;

      // Draw points
      line.forEach((point, pointIndex) => {
        const isHovered = this.hoveredPoint?.lineIndex === lineIndex &&
                         this.hoveredPoint?.pointIndex === pointIndex;
        const isDragging = this.draggingPoint?.lineIndex === lineIndex &&
                          this.draggingPoint?.pointIndex === pointIndex;
        const isSelected = this.selectedPoint?.lineIndex === lineIndex &&
                          this.selectedPoint?.pointIndex === pointIndex;
        const isOverlapping = overlappingSet.has(`${lineIndex},${pointIndex}`);

        drawPoint(ctx, point, color, this.xRange, this.yRange, width, height, this.padding, {
          isHovered,
          isDragging,
          isSelected,
          isOverlapping
        });
      });
    });

    ctx.restore();
  }

  /**
   * Find point under canvas coordinates
   */
  private findPoint(canvasX: number, canvasY: number): PointReference | null {
    // Check active line first (priority)
    const activeLine = this.lines[this.activeLineIndex];
    if (activeLine) {
      for (let pointIndex = 0; pointIndex < activeLine.length; pointIndex++) {
        const point = activeLine[pointIndex];
        if (!point) continue;

        const canvasPoint = dataToCanvas(
          point,
          this.xRange,
          this.yRange,
          this.canvas.width,
          this.canvas.height,
          this.padding
        );

        const dist = Math.sqrt(
          Math.pow(canvasX - canvasPoint.x, 2) +
          Math.pow(canvasY - canvasPoint.y, 2)
        );

        if (dist <= this.hoverRadius) {
          return { lineIndex: this.activeLineIndex, pointIndex };
        }
      }
    }

    // Check other lines
    for (let lineIndex = 0; lineIndex < this.lines.length; lineIndex++) {
      if (lineIndex === this.activeLineIndex) continue;

      const line = this.lines[lineIndex];
      if (!line) continue;

      for (let pointIndex = 0; pointIndex < line.length; pointIndex++) {
        const point = line[pointIndex];
        if (!point) continue;

        const canvasPoint = dataToCanvas(
          point,
          this.xRange,
          this.yRange,
          this.canvas.width,
          this.canvas.height,
          this.padding
        );

        const dist = Math.sqrt(
          Math.pow(canvasX - canvasPoint.x, 2) +
          Math.pow(canvasY - canvasPoint.y, 2)
        );

        if (dist <= this.hoverRadius) {
          return { lineIndex, pointIndex };
        }
      }
    }

    return null;
  }

  /**
   * Check if canvas coordinates are in chart area
   */
  private isInChartArea(canvasX: number, canvasY: number): boolean {
    return isInChartArea(
      { x: canvasX, y: canvasY },
      this.canvas.width,
      this.canvas.height,
      this.padding
    );
  }

  // ============================================
  // MOUSE EVENT HANDLERS
  // ============================================

  private handleMouseMove(e: MouseEvent): void {
    if (this.disabled) return;

    const { x: canvasX, y: canvasY } = eventToCanvasCoords(e, this.canvas);

    // Handle dragging point
    if (this.draggingPoint && !this.readOnly) {
      this.isDragging = true;
      const dataPos = canvasToData(
        { x: canvasX, y: canvasY },
        this.xRange,
        this.yRange,
        this.canvas.width,
        this.canvas.height,
        this.padding
      );

      const line = this.lines[this.draggingPoint.lineIndex];
      if (!line) return;

      const point = line[this.draggingPoint.pointIndex];
      if (!point) return;

      // Apply grid snap if enabled
      let newPoint = dataPos;
      if (this.gridSnap) {
        newPoint = applyGridSnap(
          dataPos,
          { min: this.xRange[0], max: this.xRange[1] },
          { min: this.yRange[0], max: this.yRange[1] },
          { x: this.gridSnap[0], y: this.gridSnap[1] }
        );
      }

      // Check for X conflicts
      if (!hasConflictingX(line, newPoint.x, this.draggingPoint.pointIndex, VISUAL.OVERLAP_THRESHOLD)) {
        point.x = newPoint.x;
        point.y = newPoint.y;

        // Re-sort line and update dragging index
        sortLineByX(line);
        const newIndex = line.indexOf(point);
        this.draggingPoint.pointIndex = newIndex;

        this.draw();
      }

      return;
    }

    // Handle panning
    if (this.isPanning && this.zoomEnabled) {
      this.doPan(canvasX, canvasY);
      return;
    }

    // Update hovered point
    const hoveredPoint = this.findPoint(canvasX, canvasY);
    if (hoveredPoint !== this.hoveredPoint) {
      this.hoveredPoint = hoveredPoint;
      this.draw();
    }
  }

  private handleMouseDown(e: MouseEvent): void {
    if (this.disabled) return;

    this.canvas.focus();

    const { x: canvasX, y: canvasY } = eventToCanvasCoords(e, this.canvas);
    const clickedPoint = this.findPoint(canvasX, canvasY);

    // Start panning (Ctrl+drag or read-only mode)
    if (this.zoomEnabled && (e.ctrlKey || e.metaKey || this.readOnly)) {
      if (this.isInChartArea(canvasX, canvasY)) {
        this.startPan(canvasX, canvasY);
      }
      return;
    }

    if (this.readOnly) return;

    // Start dragging existing point
    if (clickedPoint) {
      this.draggingPoint = clickedPoint;
      this.enterEditMode();
      return;
    }

    // Add new point if in chart area
    if (this.isInChartArea(canvasX, canvasY)) {
      this.addPointAt(canvasX, canvasY);
    }
  }

  private handleMouseUp(_e: MouseEvent): void {
    // Finish dragging
    if (this.draggingPoint && this.isDragging) {
      this.pushHistory();
      this.draw();
    }

    this.draggingPoint = null;
    this.isDragging = false;

    // Finish panning
    if (this.isPanning) {
      this.endPan();
    }
  }

  private handleMouseLeave(_e: MouseEvent): void {
    this.hoveredPoint = null;
    this.draw();
  }

  /**
   * Add a new point at canvas coordinates
   */
  private addPointAt(canvasX: number, canvasY: number): void {
    const dataPos = canvasToData(
      { x: canvasX, y: canvasY },
      this.xRange,
      this.yRange,
      this.canvas.width,
      this.canvas.height,
      this.padding
    );

    // Apply grid snap if enabled
    let newPoint = dataPos;
    if (this.gridSnap) {
      newPoint = applyGridSnap(
        dataPos,
        { min: this.xRange[0], max: this.xRange[1] },
        { min: this.yRange[0], max: this.yRange[1] },
        { x: this.gridSnap[0], y: this.gridSnap[1] }
      );
    }

    // Ensure active line exists
    while (this.lines.length <= this.activeLineIndex) {
      this.lines.push([]);
    }

    const activeLine = this.lines[this.activeLineIndex];
    if (!activeLine) return;

    // Check max points constraint
    if (this.maxPoints !== null && activeLine.length >= this.maxPoints) {
      debugLogger.warn('ADD_BLOCKED', {
        reason: 'Max points reached',
        maxPoints: this.maxPoints
      });
      return;
    }

    // Check for X conflicts
    if (hasConflictingX(activeLine, newPoint.x, -1, VISUAL.OVERLAP_THRESHOLD)) {
      debugLogger.warn('ADD_BLOCKED', {
        reason: 'X coordinate too close to existing point',
        x: newPoint.x
      });
      return;
    }

    // Add point
    activeLine.push(newPoint);
    sortLineByX(activeLine);

    this.enterEditMode();
    this.pushHistory();
    this.draw();

    debugLogger.log('POINT_ADDED', {
      coords: { x: newPoint.x.toFixed(2), y: newPoint.y.toFixed(2) },
      totalPoints: activeLine.length
    });
  }

  // ============================================
  // ZOOM & PAN
  // ============================================

  private startPan(canvasX: number, canvasY: number): void {
    this.isPanning = true;
    this.panStartX = canvasX;
    this.panStartY = canvasY;
    this.panStartXRange = [...this.xRange];
    this.panStartYRange = [...this.yRange];
    this.canvas.classList.add('panning');
    debugLogger.log('PAN_START', { x: canvasX, y: canvasY });
  }

  private doPan(canvasX: number, canvasY: number): void {
    if (!this.isPanning) return;

    const chartWidth = this.canvas.width - this.padding.left - this.padding.right;
    const chartHeight = this.canvas.height - this.padding.top - this.padding.bottom;

    const xRangeSize = this.panStartXRange[1] - this.panStartXRange[0];
    const yRangeSize = this.panStartYRange[1] - this.panStartYRange[0];

    // Calculate shift in data space
    const dataXShift = -((canvasX - this.panStartX) / chartWidth) * xRangeSize;
    const dataYShift = ((canvasY - this.panStartY) / chartHeight) * yRangeSize;

    // Apply shift
    this.xRange = [
      this.panStartXRange[0] + dataXShift,
      this.panStartXRange[1] + dataXShift
    ];
    this.yRange = [
      this.panStartYRange[0] + dataYShift,
      this.panStartYRange[1] + dataYShift
    ];

    // Constrain to original bounds
    const xSize = this.xRange[1] - this.xRange[0];
    const ySize = this.yRange[1] - this.yRange[0];

    if (this.xRange[0] < this.originalXRange[0]) {
      this.xRange = [this.originalXRange[0], this.originalXRange[0] + xSize];
    }
    if (this.xRange[1] > this.originalXRange[1]) {
      this.xRange = [this.originalXRange[1] - xSize, this.originalXRange[1]];
    }
    if (this.yRange[0] < this.originalYRange[0]) {
      this.yRange = [this.originalYRange[0], this.originalYRange[0] + ySize];
    }
    if (this.yRange[1] > this.originalYRange[1]) {
      this.yRange = [this.originalYRange[1] - ySize, this.originalYRange[1]];
    }

    this.draw();
  }

  private endPan(): void {
    this.isPanning = false;
    this.canvas.classList.remove('panning');

    if (this.zoomEnabled) {
      sendZoomState(this.lines, this.xRange, this.yRange, this.zoomLevel);
    }

    debugLogger.log('PAN_END', {
      xRange: this.xRange,
      yRange: this.yRange
    });
  }

  private handleWheel(e: WheelEvent): void {
    if (!this.zoomEnabled) return;

    e.preventDefault();

    const { x: canvasX, y: canvasY } = eventToCanvasCoords(e, this.canvas);

    // Only zoom if cursor is in chart area
    if (!this.isInChartArea(canvasX, canvasY)) return;

    // Get data position under cursor
    const dataPos = canvasToData(
      { x: canvasX, y: canvasY },
      this.xRange,
      this.yRange,
      this.canvas.width,
      this.canvas.height,
      this.padding
    );

    // Zoom factor (3% per tick)
    const zoomFactor = e.deltaY < 0 ? (1 - ZOOM.WHEEL_ZOOM_FACTOR) : (1 + ZOOM.WHEEL_ZOOM_FACTOR);

    // Calculate new ranges
    const xRangeSize = this.xRange[1] - this.xRange[0];
    const yRangeSize = this.yRange[1] - this.yRange[0];

    // Guard against division by zero
    if (xRangeSize === 0 || yRangeSize === 0) return;

    const newXSize = xRangeSize * zoomFactor;
    const newYSize = yRangeSize * zoomFactor;

    // Calculate new ranges centered on cursor
    const xFraction = (dataPos.x - this.xRange[0]) / xRangeSize;
    const yFraction = (dataPos.y - this.yRange[0]) / yRangeSize;

    const newXMin = dataPos.x - xFraction * newXSize;
    const newXMax = newXMin + newXSize;
    const newYMin = dataPos.y - yFraction * newYSize;
    const newYMax = newYMin + newYSize;

    this.setZoomRange(newXMin, newXMax, newYMin, newYMax);
  }

  private setZoomRange(xMin: number, xMax: number, yMin: number, yMax: number, notify: boolean = true): void {
    // Enforce minimum zoom (5% of original range)
    const originalXSize = this.originalXRange[1] - this.originalXRange[0];
    const originalYSize = this.originalYRange[1] - this.originalYRange[0];

    // Guard against zero original range
    if (originalXSize === 0 || originalYSize === 0) return;

    const minXRange = originalXSize * ZOOM.MIN_ZOOM_PERCENT;
    const minYRange = originalYSize * ZOOM.MIN_ZOOM_PERCENT;

    const currentXSize = xMax - xMin;
    const currentYSize = yMax - yMin;

    if (currentXSize < minXRange) {
      const center = (xMin + xMax) / 2;
      xMin = center - minXRange / 2;
      xMax = center + minXRange / 2;
    }
    if (currentYSize < minYRange) {
      const center = (yMin + yMax) / 2;
      yMin = center - minYRange / 2;
      yMax = center + minYRange / 2;
    }

    // Constrain to original bounds
    if (xMin < this.originalXRange[0]) {
      const shift = this.originalXRange[0] - xMin;
      xMin += shift;
      xMax += shift;
    }
    if (xMax > this.originalXRange[1]) {
      const shift = xMax - this.originalXRange[1];
      xMin -= shift;
      xMax -= shift;
    }
    if (yMin < this.originalYRange[0]) {
      const shift = this.originalYRange[0] - yMin;
      yMin += shift;
      yMax += shift;
    }
    if (yMax > this.originalYRange[1]) {
      const shift = yMax - this.originalYRange[1];
      yMin -= shift;
      yMax -= shift;
    }

    // Update ranges
    this.xRange = [xMin, xMax];
    this.yRange = [yMin, yMax];

    // Calculate zoom level
    this.zoomLevel = originalXSize / (xMax - xMin);

    this.draw();

    // Send zoom state
    if (notify && this.zoomEnabled) {
      sendZoomState(this.lines, this.xRange, this.yRange, this.zoomLevel);

      if (this.onZoomCallback) {
        this.onZoomCallback({
          xRange: this.xRange,
          yRange: this.yRange,
          zoomLevel: this.zoomLevel
        });
      }
    }

    debugLogger.log('ZOOM_CHANGED', {
      xRange: [xMin.toFixed(2), xMax.toFixed(2)],
      yRange: [yMin.toFixed(2), yMax.toFixed(2)],
      zoomLevel: this.zoomLevel.toFixed(2)
    });
  }

  // Placeholder methods (keyboard and touch handlers next)
  private handleKeyDown(_e: KeyboardEvent): void { /* TODO */ }
  private handleTouchStart(_e: TouchEvent): void { /* TODO */ }
  private handleTouchMove(_e: TouchEvent): void { /* TODO */ }
  private handleTouchEnd(_e: TouchEvent): void { /* TODO */ }
}
