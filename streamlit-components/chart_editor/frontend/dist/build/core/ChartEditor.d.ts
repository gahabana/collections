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
import type { Lines, ChartConfig, RangeTuple } from '../types/index.js';
/**
 * Main ChartEditor class
 */
export declare class ChartEditor {
    private canvas;
    private ctx;
    private colors;
    private gridSnap;
    private disabled;
    private minPoints;
    private maxPoints;
    private zoomEnabled;
    private readOnly;
    private lines;
    private xRange;
    private yRange;
    private originalXRange;
    private originalYRange;
    private activeLineIndex;
    private hoveredPoint;
    private draggingPoint;
    private selectedPoint;
    private isEditing;
    private isDragging;
    private zoomLevel;
    private isPanning;
    private panStartX;
    private panStartY;
    private panStartXRange;
    private panStartYRange;
    private historyStack;
    private historyIndex;
    private touchState;
    private readonly padding;
    private readonly hoverRadius;
    private onZoomCallback;
    /**
     * Constructor - Initialize the ChartEditor
     */
    constructor(canvas: HTMLCanvasElement);
    /**
     * Attach all event listeners to the canvas
     */
    private attachEventListeners;
    /**
     * Set or update the chart configuration
     */
    setConfig(config: ChartConfig): void;
    /**
     * Get the current lines data
     */
    getLines(): Lines;
    /**
     * Set zoom callback
     */
    setOnZoomCallback(callback: (data: {
        xRange: RangeTuple;
        yRange: RangeTuple;
        zoomLevel: number;
    }) => void): void;
    /**
     * Initialize history with current state
     */
    private initHistory;
    /**
     * Push current state to history
     */
    private pushHistory;
    /**
     * Undo last action
     */
    undo(): boolean;
    /**
     * Redo last undone action
     */
    redo(): boolean;
    /**
     * Check if undo is available
     */
    canUndo(): boolean;
    /**
     * Check if redo is available
     */
    canRedo(): boolean;
    /**
     * Enter edit mode
     */
    private enterEditMode;
    /**
     * Save changes and exit edit mode
     */
    saveChanges(): void;
    /**
     * Main draw method - renders the entire chart
     */
    private draw;
    /**
     * Find point under canvas coordinates
     */
    private findPoint;
    /**
     * Check if canvas coordinates are in chart area
     */
    private isInChartArea;
    private handleMouseMove;
    private handleMouseDown;
    private handleMouseUp;
    private handleMouseLeave;
    /**
     * Add a new point at canvas coordinates
     */
    private addPointAt;
    private startPan;
    private doPan;
    private endPan;
    private handleWheel;
    private setZoomRange;
    private handleKeyDown;
    private handleTouchStart;
    private handleTouchMove;
    private handleTouchEnd;
}
//# sourceMappingURL=ChartEditor.d.ts.map