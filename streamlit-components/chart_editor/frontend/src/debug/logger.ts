/**
 * Debug logging system
 * Provides structured logging with timestamps and log levels
 */

/**
 * Log levels
 */
export type LogLevel = 'info' | 'warn' | 'error';

/**
 * Log entry structure
 */
export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  action: string;
  data?: unknown;
  message?: string;
}

/**
 * Debug logger class
 */
export class DebugLogger {
  private enabled: boolean = false;
  private logs: LogEntry[] = [];
  private maxLogs: number = 100;
  private logElement: HTMLElement | null = null;

  /**
   * Enable debug logging
   */
  enable(): void {
    this.enabled = true;
    console.log('[DebugLogger] Enabled');
  }

  /**
   * Disable debug logging
   */
  disable(): void {
    this.enabled = false;
    console.log('[DebugLogger] Disabled');
  }

  /**
   * Toggle debug logging
   */
  toggle(): boolean {
    this.enabled = !this.enabled;
    console.log(`[DebugLogger] ${this.enabled ? 'Enabled' : 'Disabled'}`);
    return this.enabled;
  }

  /**
   * Check if logging is enabled
   */
  isEnabled(): boolean {
    return this.enabled;
  }

  /**
   * Log a message
   */
  log(action: string, data?: unknown, level: LogLevel = 'info'): void {
    if (!this.enabled) return;

    const entry: LogEntry = {
      timestamp: new Date().toISOString().substr(11, 12),
      level,
      action,
      data,
      message: this.formatData(data)
    };

    this.logs.push(entry);

    // Limit log size
    if (this.logs.length > this.maxLogs) {
      this.logs.shift();
    }

    // Console output
    const consoleMethod = level === 'error' ? console.error :
                         level === 'warn' ? console.warn :
                         console.log;

    if (data !== undefined) {
      consoleMethod(`[${entry.timestamp}] ${action}:`, data);
    } else {
      consoleMethod(`[${entry.timestamp}] ${action}`);
    }

    // Update visual log if element exists
    this.updateLogElement();
  }

  /**
   * Log info message
   */
  info(action: string, data?: unknown): void {
    this.log(action, data, 'info');
  }

  /**
   * Log warning message
   */
  warn(action: string, data?: unknown): void {
    this.log(action, data, 'warn');
  }

  /**
   * Log error message
   */
  error(action: string, data?: unknown): void {
    this.log(action, data, 'error');
  }

  /**
   * Get all log entries
   */
  getLogs(): LogEntry[] {
    return [...this.logs];
  }

  /**
   * Clear all logs
   */
  clear(): void {
    this.logs = [];
    console.clear();
    this.updateLogElement();
  }

  /**
   * Set the HTML element for visual log display
   */
  setLogElement(element: HTMLElement): void {
    this.logElement = element;
    this.updateLogElement();
  }

  /**
   * Update the visual log element
   */
  private updateLogElement(): void {
    if (!this.logElement) return;

    const html = this.logs
      .slice(-50) // Show last 50 logs
      .map(entry => {
        const levelClass = entry.level;
        const dataStr = entry.message || '';
        return `
          <div class="log-entry">
            <span class="timestamp">${entry.timestamp}</span>
            <span class="action ${levelClass}">${entry.action}</span>
            ${dataStr ? `<span class="data">${dataStr}</span>` : ''}
          </div>
        `;
      })
      .join('');

    this.logElement.innerHTML = html || '<div class="log-entry">No logs yet</div>';

    // Auto-scroll to bottom
    this.logElement.scrollTop = this.logElement.scrollHeight;
  }

  /**
   * Format data for display
   */
  private formatData(data: unknown): string {
    if (data === undefined) return '';
    if (typeof data === 'string') return data;
    if (typeof data === 'number' || typeof data === 'boolean') return String(data);

    try {
      return JSON.stringify(data, null, 0);
    } catch (e) {
      return String(data);
    }
  }

  /**
   * Export logs as JSON
   */
  exportLogs(): string {
    return JSON.stringify(this.logs, null, 2);
  }

  /**
   * Download logs as a file
   */
  downloadLogs(): void {
    const blob = new Blob([this.exportLogs()], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chart-editor-logs-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }
}

/**
 * Global debug logger instance
 */
export const debugLogger = new DebugLogger();
