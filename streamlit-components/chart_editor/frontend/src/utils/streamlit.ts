/**
 * Streamlit communication utilities
 */

import type { Lines, RangeTuple } from '../types/index.js';
import { serializeLines } from './helpers.js';

/**
 * Send a message to Streamlit parent window
 */
export function sendMessageToStreamlit(type: string, value: Record<string, unknown>): void {
  window.parent.postMessage({
    type,
    ...value
  }, '*');
}

/**
 * Set the component value (main data output)
 */
export function setComponentValue(lines: Lines): void {
  const serialized = serializeLines(lines);
  sendMessageToStreamlit('streamlit:setComponentValue', { value: serialized });
}

/**
 * Send zoom state to Streamlit (includes lines data to prevent data loss)
 */
export function sendZoomState(
  lines: Lines,
  xRange: RangeTuple,
  yRange: RangeTuple,
  zoomLevel: number
): void {
  const serializedLines = serializeLines(lines);

  const state = {
    type: 'zoom',
    lines: serializedLines,
    xRange,
    yRange,
    zoomLevel
  };

  sendMessageToStreamlit('streamlit:setComponentValue', { value: state });
}

/**
 * Notify Streamlit that component height has changed
 */
export function setFrameHeight(height: number): void {
  sendMessageToStreamlit('streamlit:setFrameHeight', { height });
}

/**
 * Set component ready state
 */
export function setComponentReady(): void {
  sendMessageToStreamlit('streamlit:componentReady', {});
}

/**
 * Check if code is running inside Streamlit iframe
 */
export function isInStreamlit(): boolean {
  return window.parent !== window;
}

/**
 * Listen for Streamlit render events
 */
export function onStreamlitRender(
  callback: (args: unknown) => void
): () => void {
  const handler = (event: MessageEvent): void => {
    if (event.data.type === 'streamlit:render') {
      callback(event.data.args);
    }
  };

  window.addEventListener('message', handler);

  // Return cleanup function
  return () => window.removeEventListener('message', handler);
}
