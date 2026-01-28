/**
 * Streamlit communication utilities
 */
import type { Lines, RangeTuple } from '../types/index.js';
/**
 * Send a message to Streamlit parent window
 */
export declare function sendMessageToStreamlit(type: string, value: Record<string, unknown>): void;
/**
 * Set the component value (main data output)
 */
export declare function setComponentValue(lines: Lines): void;
/**
 * Send zoom state to Streamlit (includes lines data to prevent data loss)
 */
export declare function sendZoomState(lines: Lines, xRange: RangeTuple, yRange: RangeTuple, zoomLevel: number): void;
/**
 * Notify Streamlit that component height has changed
 */
export declare function setFrameHeight(height: number): void;
/**
 * Set component ready state
 */
export declare function setComponentReady(): void;
/**
 * Check if code is running inside Streamlit iframe
 */
export declare function isInStreamlit(): boolean;
/**
 * Listen for Streamlit render events
 */
export declare function onStreamlitRender(callback: (args: unknown) => void): () => void;
//# sourceMappingURL=streamlit.d.ts.map