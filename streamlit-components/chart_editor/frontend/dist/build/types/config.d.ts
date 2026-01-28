/**
 * Configuration types for Chart Editor initialization and updates
 */
import type { Lines, RangeTuple, GridSnapTuple, ColorList } from './core.js';
/**
 * Complete configuration for the Chart Editor
 */
export interface ChartConfig {
    /** Chart data - array of lines */
    lines: Lines;
    /** X-axis range [min, max] */
    xRange: RangeTuple;
    /** Y-axis range [min, max] */
    yRange: RangeTuple;
    /** Colors for each line (hex format) */
    colors: ColorList;
    /** Grid snap configuration [x%, y%] or null for no snapping */
    gridSnap: GridSnapTuple | null;
    /** Chart title */
    title: string;
    /** X-axis label */
    xLabel: string;
    /** Y-axis label */
    yLabel: string;
    /** Canvas width in pixels */
    width: number;
    /** Canvas height in pixels */
    height: number;
    /** If true, chart is displayed but not editable */
    disabled: boolean;
    /** Minimum points required per line */
    minPoints: number;
    /** Maximum points allowed per line (null = unlimited) */
    maxPoints: number | null;
    /** If true, enables zoom and pan functionality */
    zoomEnabled: boolean;
    /** If true, chart is view-only (cannot edit points) */
    readOnly: boolean;
}
/**
 * Zoom state information sent to Python
 */
export interface ZoomState {
    type: 'zoom';
    lines: number[][];
    xRange: RangeTuple;
    yRange: RangeTuple;
    zoomLevel: number;
}
/**
 * Zoom callback data
 */
export interface ZoomCallbackData {
    xRange: RangeTuple;
    yRange: RangeTuple;
    zoomLevel: number;
}
/**
 * Message sent to Streamlit
 */
export interface StreamlitMessage {
    type: string;
    value: Lines | ZoomState;
}
/**
 * Streamlit render event data
 */
export interface StreamlitRenderEvent {
    type: 'streamlit:render';
    args: ChartConfig;
}
//# sourceMappingURL=config.d.ts.map