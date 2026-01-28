/**
 * Chart Editor Component - Entry Point
 * TypeScript implementation of the interactive 2D chart editor
 * @version 2.0.0
 */

import { ChartEditor } from './core/index.js';
import type { ChartConfig } from './types/index.js';
import { onStreamlitRender, setComponentReady, deserializeLines } from './utils/index.js';
import { debugLogger } from './debug/index.js';

/**
 * Initialize the Chart Editor when DOM is ready
 */
function initializeChartEditor(): void {
  debugLogger.log('INIT_START', 'Initializing Chart Editor v2.0.0 (TypeScript)');

  // Get canvas element
  const canvas = document.getElementById('chartCanvas') as HTMLCanvasElement;
  if (!canvas) {
    debugLogger.error('INIT_ERROR', 'Canvas element not found');
    return;
  }

  // Create editor instance
  let editor: ChartEditor;
  try {
    editor = new ChartEditor(canvas);
    debugLogger.log('EDITOR_CREATED', 'ChartEditor instance created');
  } catch (error) {
    debugLogger.error('INIT_ERROR', { error: String(error) });
    return;
  }

  // Setup Streamlit render listener
  const cleanup = onStreamlitRender((args: unknown) => {
    debugLogger.log('STREAMLIT_RENDER', 'Received render event');

    try {
      // Parse and validate config
      const config = args as ChartConfig;

      // Deserialize lines if needed
      if (config.lines) {
        config.lines = deserializeLines(config.lines as unknown as number[][][]);
      }

      // Update editor configuration
      editor.setConfig(config);

      debugLogger.log('CONFIG_APPLIED', {
        lines: config.lines.length,
        xRange: config.xRange,
        yRange: config.yRange
      });
    } catch (error) {
      debugLogger.error('CONFIG_ERROR', { error: String(error) });
    }
  });

  // Wire up UI controls if they exist
  setupUIControls(editor);

  // Notify Streamlit that component is ready
  setComponentReady();
  debugLogger.log('INIT_COMPLETE', 'Chart Editor initialized and ready');

  // Cleanup on unload
  window.addEventListener('beforeunload', () => {
    cleanup();
    debugLogger.log('CLEANUP', 'Cleaned up event listeners');
  });
}

/**
 * Setup UI control event listeners
 */
function setupUIControls(editor: ChartEditor): void {
  // Debug toggle button
  const debugToggle = document.getElementById('btnDebugToggle');
  if (debugToggle) {
    debugToggle.addEventListener('click', () => {
      const enabled = debugLogger.toggle();
      debugToggle.classList.toggle('active', enabled);
      debugLogger.log('DEBUG_TOGGLED', enabled ? 'Enabled' : 'Disabled');
    });
  }

  // Set debug log element
  const debugLog = document.getElementById('debugLog');
  if (debugLog) {
    debugLogger.setLogElement(debugLog);
  }

  // Undo button
  const undoBtn = document.getElementById('btnUndo');
  if (undoBtn) {
    undoBtn.addEventListener('click', () => {
      if (editor.undo()) {
        debugLogger.log('UI_UNDO', 'Undo triggered from UI');
      }
    });
  }

  // Redo button
  const redoBtn = document.getElementById('btnRedo');
  if (redoBtn) {
    redoBtn.addEventListener('click', () => {
      if (editor.redo()) {
        debugLogger.log('UI_REDO', 'Redo triggered from UI');
      }
    });
  }

  // Save button
  const saveBtn = document.getElementById('btnSave');
  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      editor.saveChanges();
      debugLogger.log('UI_SAVE', 'Save triggered from UI');
    });
  }

  debugLogger.log('UI_SETUP', 'UI controls wired up');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeChartEditor);
} else {
  initializeChartEditor();
}

// Export for potential external use
export { ChartEditor } from './core/index.js';
export type { ChartConfig } from './types/index.js';
