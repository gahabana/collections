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
export declare class DebugLogger {
    private enabled;
    private logs;
    private maxLogs;
    private logElement;
    /**
     * Enable debug logging
     */
    enable(): void;
    /**
     * Disable debug logging
     */
    disable(): void;
    /**
     * Toggle debug logging
     */
    toggle(): boolean;
    /**
     * Check if logging is enabled
     */
    isEnabled(): boolean;
    /**
     * Log a message
     */
    log(action: string, data?: unknown, level?: LogLevel): void;
    /**
     * Log info message
     */
    info(action: string, data?: unknown): void;
    /**
     * Log warning message
     */
    warn(action: string, data?: unknown): void;
    /**
     * Log error message
     */
    error(action: string, data?: unknown): void;
    /**
     * Get all log entries
     */
    getLogs(): LogEntry[];
    /**
     * Clear all logs
     */
    clear(): void;
    /**
     * Set the HTML element for visual log display
     */
    setLogElement(element: HTMLElement): void;
    /**
     * Update the visual log element
     */
    private updateLogElement;
    /**
     * Format data for display
     */
    private formatData;
    /**
     * Export logs as JSON
     */
    exportLogs(): string;
    /**
     * Download logs as a file
     */
    downloadLogs(): void;
}
/**
 * Global debug logger instance
 */
export declare const debugLogger: DebugLogger;
//# sourceMappingURL=logger.d.ts.map