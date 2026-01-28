# TypeScript Migration Plan - Chart Editor Component

**Target**: Migrate `chart_editor/frontend/index.html` (2,731 lines) to TypeScript
**Strategy**: Commit both TypeScript source + compiled JavaScript (Option 2)
**Timeline**: 2-3 days for initial setup + 1-2 weeks for full migration
**Estimated Effort**: ~40 hours total

---

## Phase 0: Pre-Migration Preparation (1 hour)

### Step 0.1: Create Feature Branch

```bash
cd /Users/zh/gd/git/collections/streamlit-components
git checkout -b feature/typescript-migration
git push -u origin feature/typescript-migration
```

### Step 0.2: Backup Current State

```bash
# Create backup of working code
cp chart_editor/frontend/index.html chart_editor/frontend/index.html.backup
git add chart_editor/frontend/index.html.backup
git commit -m "Backup: Save working vanilla JS version before TS migration"
```

### Step 0.3: Document Current Functionality

```bash
# Test current component works
streamlit run demo.py &
DEMO_PID=$!

# Take screenshots / test all features
# - Add/remove/drag points
# - Zoom with wheel
# - Keyboard navigation
# - Touch gestures (if available)
# - Undo/redo

kill $DEMO_PID
```

---

## Phase 1: Project Setup (2-3 hours)

### Step 1.1: Initialize Node.js Project

```bash
cd chart_editor/frontend

# Initialize package.json
npm init -y

# Edit package.json to add metadata
```

**File**: `chart_editor/frontend/package.json`
```json
{
  "name": "chart-editor-component",
  "version": "2.0.0",
  "description": "TypeScript-based interactive chart editor for Streamlit",
  "main": "dist/bundle.js",
  "types": "dist/types/index.d.ts",
  "scripts": {
    "build": "npm run clean && npm run compile && npm run bundle",
    "compile": "tsc",
    "bundle": "rollup -c",
    "watch": "concurrently \"tsc --watch\" \"rollup -c -w\"",
    "clean": "rm -rf dist",
    "typecheck": "tsc --noEmit",
    "lint": "eslint src/**/*.ts",
    "precommit": "npm run build",
    "test": "echo \"Tests coming soon\" && exit 0"
  },
  "keywords": ["streamlit", "chart", "editor", "typescript"],
  "author": "Your Name",
  "license": "MIT",
  "devDependencies": {
    "@rollup/plugin-node-resolve": "^15.2.3",
    "@rollup/plugin-typescript": "^11.1.5",
    "@typescript-eslint/eslint-plugin": "^6.15.0",
    "@typescript-eslint/parser": "^6.15.0",
    "concurrently": "^8.2.2",
    "eslint": "^8.56.0",
    "rollup": "^4.9.1",
    "rollup-plugin-terser": "^7.0.2",
    "tslib": "^2.6.2",
    "typescript": "^5.3.3"
  }
}
```

### Step 1.2: Install Dependencies

```bash
npm install --save-dev \
  typescript@^5.3.3 \
  @typescript-eslint/eslint-plugin@^6.15.0 \
  @typescript-eslint/parser@^6.15.0 \
  eslint@^8.56.0 \
  rollup@^4.9.1 \
  @rollup/plugin-typescript@^11.1.5 \
  @rollup/plugin-node-resolve@^15.2.3 \
  rollup-plugin-terser@^7.0.2 \
  tslib@^2.6.2 \
  concurrently@^8.2.2

# Verify installation
npm list --depth=0
```

### Step 1.3: Configure TypeScript

**File**: `chart_editor/frontend/tsconfig.json`
```json
{
  "compilerOptions": {
    /* Language and Environment */
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],

    /* Modules */
    "module": "ESNext",
    "moduleResolution": "node",
    "resolveJsonModule": true,

    /* Emit */
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "removeComments": false,

    /* Interop Constraints */
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,

    /* Type Checking */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,

    /* Completeness */
    "skipLibCheck": true,

    /* Advanced */
    "incremental": true,
    "tsBuildInfoFile": "./dist/.tsbuildinfo"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts"]
}
```

Create the file:
```bash
cat > tsconfig.json << 'EOF'
[paste content above]
EOF
```

### Step 1.4: Configure Rollup

**File**: `chart_editor/frontend/rollup.config.js`
```javascript
import typescript from '@rollup/plugin-typescript';
import resolve from '@rollup/plugin-node-resolve';
import { terser } from 'rollup-plugin-terser';

const production = process.env.NODE_ENV === 'production';

export default {
  input: 'src/main.ts',
  output: {
    file: 'dist/bundle.js',
    format: 'iife',
    name: 'ChartEditor',
    sourcemap: true,
    banner: '/* Chart Editor Component - TypeScript Version */'
  },
  plugins: [
    resolve(),
    typescript({
      tsconfig: './tsconfig.json',
      sourceMap: true,
      inlineSources: !production
    }),
    production && terser({
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    })
  ].filter(Boolean)
};
```

Create the file:
```bash
cat > rollup.config.js << 'EOF'
[paste content above]
EOF
```

### Step 1.5: Configure ESLint

**File**: `chart_editor/frontend/.eslintrc.json`
```json
{
  "root": true,
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "plugins": ["@typescript-eslint"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/explicit-function-return-type": "off",
    "@typescript-eslint/no-explicit-any": "warn",
    "no-console": ["warn", { "allow": ["warn", "error"] }]
  },
  "env": {
    "browser": true,
    "es2020": true
  }
}
```

Create the file:
```bash
cat > .eslintrc.json << 'EOF'
[paste content above]
EOF
```

### Step 1.6: Configure Git

**File**: `chart_editor/frontend/.gitignore`
```
# Dependencies
node_modules/
package-lock.json

# Build artifacts (we WILL commit dist/bundle.js, but ignore temp files)
dist/.tsbuildinfo
*.tsbuildinfo

# Editor
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
```

Create the file:
```bash
cat > .gitignore << 'EOF'
[paste content above]
EOF
```

**File**: `chart_editor/frontend/.gitattributes`
```
# Mark TypeScript as primary language
*.ts linguist-language=TypeScript

# Mark compiled JavaScript as generated (lower importance in diffs)
dist/bundle.js linguist-generated=true
dist/bundle.js.map linguist-generated=true

# Ensure consistent line endings
*.ts text eol=lf
*.js text eol=lf
*.json text eol=lf
*.md text eol=lf
```

Create the file:
```bash
cat > .gitattributes << 'EOF'
[paste content above]
EOF
```

### Step 1.7: Create Source Directory Structure

```bash
# Create directory structure
mkdir -p src/{types,utils,components,debug,events}
mkdir -p dist

# Verify structure
tree -L 2 .
# Should show:
# .
# ├── dist/
# ├── src/
# │   ├── components/
# │   ├── debug/
# │   ├── events/
# │   ├── types/
# │   └── utils/
# ├── index.html
# ├── package.json
# ├── rollup.config.js
# ├── tsconfig.json
# └── .gitignore
```

### Step 1.8: Setup Pre-Commit Hook

**File**: `.git/hooks/pre-commit`
```bash
#!/bin/bash

# Auto-build TypeScript on commit
cd chart_editor/frontend

if [ -f "package.json" ]; then
    echo "Building TypeScript..."
    npm run build

    if [ $? -ne 0 ]; then
        echo "❌ TypeScript build failed!"
        exit 1
    fi

    # Stage built files
    git add dist/bundle.js dist/bundle.js.map
    echo "✅ TypeScript built and staged"
fi
```

Create and enable the hook:
```bash
cat > ../../.git/hooks/pre-commit << 'EOF'
[paste content above]
EOF

chmod +x ../../.git/hooks/pre-commit
```

### Step 1.9: Commit Initial Setup

```bash
cd ../.. # Back to repo root
git add chart_editor/frontend/package.json
git add chart_editor/frontend/tsconfig.json
git add chart_editor/frontend/rollup.config.js
git add chart_editor/frontend/.eslintrc.json
git add chart_editor/frontend/.gitignore
git add chart_editor/frontend/.gitattributes
git add .git/hooks/pre-commit

git commit -m "Setup: TypeScript build infrastructure

- Add package.json with build scripts
- Configure TypeScript compiler (ES2020, strict mode)
- Configure Rollup bundler with terser
- Configure ESLint for TypeScript
- Add pre-commit hook for auto-build
- Configure git attributes for generated files"
```

---

## Phase 2: Type Definitions (4-6 hours)

### Step 2.1: Create Core Type Definitions

**File**: `chart_editor/frontend/src/types/index.ts`
```typescript
/**
 * Core type definitions for Chart Editor component
 */

/** A point in 2D space with (x, y) coordinates */
export interface Point {
    x: number;
    y: number;
}

/** A line is an array of points, sorted by X coordinate */
export type Line = Point[];

/** Multiple lines make up the chart data */
export type Lines = Line[];

/** RGB color string (hex format like "#FF6B6B") */
export type Color = string;

/** Axis range tuple [min, max] */
export type Range = [number, number];

/** Grid snap percentage [x%, y%] */
export type GridSnap = [number, number];

/** Canvas padding in pixels */
export interface Padding {
    top: number;
    right: number;
    bottom: number;
    left: number;
}

/** Reference to a specific point on a specific line */
export interface PointReference {
    lineIndex: number;
    pointIndex: number;
}

/** Configuration received from Python/Streamlit */
export interface ChartConfig {
    lines: number[][][];  // [[x, y], ...] format from Python
    xRange: [number, number];
    yRange: [number, number];
    colors?: Color[];
    gridSnap?: GridSnap | null;
    title?: string;
    xLabel?: string;
    yLabel?: string;
    width: number;
    height: number;
    disabled: boolean;
    readOnly: boolean;
    minPoints: number;
    maxPoints: number | null;
    zoomEnabled: boolean;
}

/** Chart editor state */
export interface EditorState {
    lines: Lines;
    savedLines: Lines;
    isEditing: boolean;
    activeLineIndex: number;
    hoveredPoint: PointReference | null;
    draggingPoint: PointReference | null;
    selectedPoint: PointReference | null;
    isDragging: boolean;
    xRange: Range;
    yRange: Range;
    originalXRange: Range;
    originalYRange: Range;
    zoomLevel: number;
}

/** Zoom state sent to Python */
export interface ZoomState {
    type: 'zoom';
    lines: number[][][];
    xRange: Range;
    yRange: Range;
    zoomLevel: number;
}

/** Touch state for pinch-to-zoom gestures */
export interface TouchState {
    touches: Touch[];
    initialPinchDistance: number | null;
    initialZoomLevel: number;
    initialXRange: Range | null;
    initialYRange: Range | null;
    pinchCenter: { x: number; y: number } | null;
}

/** Range selector state */
export interface RangeSelectorState {
    enabled: boolean;
    dragging: 'left' | 'right' | 'viewport' | null;
    startX: number;
    startLeft: number;
    startWidth: number;
}

/** History entry for undo/redo */
export type HistoryEntry = Lines;

/** Debug log entry type */
export type LogType = 'action' | 'data' | 'info' | 'warn' | 'error';

/** Debug log entry */
export interface LogEntry {
    timestamp: string;
    action: string;
    data?: unknown;
    type: LogType;
}
```

Create the file:
```bash
cat > src/types/index.ts << 'EOF'
[paste content above]
EOF
```

### Step 2.2: Create Configuration Constants

**File**: `chart_editor/frontend/src/types/constants.ts`
```typescript
/**
 * Configuration constants extracted from magic numbers
 */

export const CONFIG = {
    /** Point hit detection radius in pixels */
    POINT_HIT_RADIUS: 12,

    /** X-coordinate conflict tolerance (1% of range) */
    X_CONFLICT_TOLERANCE: 0.01,

    /** Maximum undo/redo history size */
    MAX_HISTORY_SIZE: 50,

    /** Wheel zoom sensitivity (3% per tick) */
    ZOOM_SENSITIVITY: 0.03,

    /** Minimum zoom level (5% of original range) */
    MIN_ZOOM_PERCENT: 0.05,

    /** Dot radius in pixels */
    DOT_RADIUS: 5,

    /** Line width in pixels */
    LINE_WIDTH: 2,

    /** Active line extra width */
    ACTIVE_LINE_WIDTH: 3,

    /** Zoom animation duration in milliseconds */
    ZOOM_ANIMATION_DURATION: 200,

    /** Quick click threshold in milliseconds (for remove on click) */
    QUICK_CLICK_THRESHOLD: 300,

    /** Error flash duration in milliseconds */
    ERROR_FLASH_DURATION: 800,

    /** Zoom event debounce delay in milliseconds */
    ZOOM_DEBOUNCE_DELAY: 150,

    /** Maximum debug log entries */
    MAX_DEBUG_LOG_ENTRIES: 50,

    /** Canvas padding */
    PADDING: {
        TOP: 20,
        RIGHT: 20,
        BOTTOM: 30,
        LEFT: 50
    } as const,

    /** Default colors (colorblind-friendly palette) */
    DEFAULT_COLORS: [
        "#FF6B6B",  // Coral Red
        "#4ECDC4",  // Teal
        "#A55EEA",  // Purple
        "#45B7D1",  // Sky Blue
        "#F7DC6F",  // Yellow
        "#82E0AA",  // Green
        "#F8B500",  // Orange
    ] as const
} as const;

/** Type-safe configuration access */
export type ConfigType = typeof CONFIG;
```

Create the file:
```bash
cat > src/types/constants.ts << 'EOF'
[paste content above]
EOF
```

### Step 2.3: Commit Type Definitions

```bash
git add chart_editor/frontend/src/types/
git commit -m "Types: Add comprehensive TypeScript type definitions

- Core types (Point, Line, Range, etc.)
- Configuration interfaces
- State management types
- Extract magic numbers to CONFIG constants
- Add JSDoc comments for all types"
```

---

## Phase 3: Utilities Migration (3-4 hours)

### Step 3.1: Utility Functions

**File**: `chart_editor/frontend/src/utils/helpers.ts`
```typescript
import type { Point, Line, Lines } from '../types';

/**
 * Deep clone lines array to prevent mutation
 */
export function deepCloneLines(lines: Lines): Lines {
    return lines.map(line =>
        line.map(point => ({ x: point.x, y: point.y }))
    );
}

/**
 * Check if two points are equal
 */
export function pointsEqual(p1: Point, p2: Point): boolean {
    return p1.x === p2.x && p1.y === p2.y;
}

/**
 * Calculate distance between two points
 */
export function distance(p1: Point, p2: Point): number {
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    return Math.sqrt(dx * dx + dy * dy);
}

/**
 * Sort line by X coordinate
 */
export function sortLine(line: Line): Line {
    return [...line].sort((a, b) => a.x - b.x);
}

/**
 * Debounce function (for zoom events)
 */
export function debounce<T extends (...args: any[]) => void>(
    func: T,
    wait: number
): (...args: Parameters<T>) => void {
    let timeout: number | undefined;

    return function(this: any, ...args: Parameters<T>) {
        const later = () => {
            timeout = undefined;
            func.apply(this, args);
        };

        if (timeout !== undefined) {
            clearTimeout(timeout);
        }
        timeout = window.setTimeout(later, wait);
    };
}

/**
 * Clamp value between min and max
 */
export function clamp(value: number, min: number, max: number): number {
    return Math.max(min, Math.min(max, value));
}

/**
 * Linear interpolation
 */
export function lerp(start: number, end: number, t: number): number {
    return start + (end - start) * t;
}

/**
 * Ease out cubic easing function
 */
export function easeOutCubic(t: number): number {
    return 1 - Math.pow(1 - t, 3);
}

/**
 * Format number with fixed decimals
 */
export function formatNumber(value: number, decimals: number = 2): string {
    return value.toFixed(decimals);
}
```

Create the file:
```bash
cat > src/utils/helpers.ts << 'EOF'
[paste content above]
EOF
```

### Step 3.2: Coordinate Transformation Utilities

**File**: `chart_editor/frontend/src/utils/coordinates.ts`
```typescript
import type { Point, Range, Padding } from '../types';

/**
 * Convert data coordinates to canvas pixel coordinates
 */
export function dataToCanvas(
    point: Point,
    xRange: Range,
    yRange: Range,
    canvasWidth: number,
    canvasHeight: number,
    padding: Padding
): Point {
    const chartWidth = canvasWidth - padding.left - padding.right;
    const chartHeight = canvasHeight - padding.top - padding.bottom;

    // Guard against division by zero
    const xRangeSize = xRange[1] - xRange[0];
    const yRangeSize = yRange[1] - yRange[0];

    if (xRangeSize === 0 || yRangeSize === 0) {
        return { x: padding.left, y: padding.top };
    }

    const canvasX = padding.left +
        ((point.x - xRange[0]) / xRangeSize) * chartWidth;
    const canvasY = padding.top +
        (1 - (point.y - yRange[0]) / yRangeSize) * chartHeight;

    return { x: canvasX, y: canvasY };
}

/**
 * Convert canvas pixel coordinates to data coordinates
 */
export function canvasToData(
    canvasPoint: Point,
    xRange: Range,
    yRange: Range,
    canvasWidth: number,
    canvasHeight: number,
    padding: Padding,
    gridSnap?: [number, number] | null
): Point {
    const chartWidth = canvasWidth - padding.left - padding.right;
    const chartHeight = canvasHeight - padding.top - padding.bottom;

    // Guard against division by zero
    if (chartWidth === 0 || chartHeight === 0) {
        return { x: xRange[0], y: yRange[0] };
    }

    let x = xRange[0] +
        ((canvasPoint.x - padding.left) / chartWidth) * (xRange[1] - xRange[0]);
    let y = yRange[0] +
        (1 - (canvasPoint.y - padding.top) / chartHeight) * (yRange[1] - yRange[0]);

    // Apply grid snapping if enabled
    if (gridSnap) {
        const xStep = (xRange[1] - xRange[0]) * gridSnap[0] / 100;
        const yStep = (yRange[1] - yRange[0]) * gridSnap[1] / 100;

        if (xStep > 0) x = Math.round(x / xStep) * xStep;
        if (yStep > 0) y = Math.round(y / yStep) * yStep;
    }

    // Clamp to range
    x = Math.max(xRange[0], Math.min(xRange[1], x));
    y = Math.max(yRange[0], Math.min(yRange[1], y));

    return { x, y };
}

/**
 * Check if canvas point is within chart area
 */
export function isInChartArea(
    canvasPoint: Point,
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
```

Create the file:
```bash
cat > src/utils/coordinates.ts << 'EOF'
[paste content above]
EOF
```

### Step 3.3: Streamlit Communication Utilities

**File**: `chart_editor/frontend/src/utils/streamlit.ts`
```typescript
import type { Lines, ZoomState } from '../types';

/**
 * Send message to Streamlit parent window
 */
export function sendMessageToStreamlit(type: string, data: unknown): void {
    window.parent.postMessage(
        {
            isStreamlitMessage: true,
            type: type,
            ...data
        },
        "*"
    );
}

/**
 * Notify Streamlit that component is ready
 */
export function setComponentReady(): void {
    sendMessageToStreamlit("streamlit:componentReady", { apiVersion: 1 });
}

/**
 * Adjust iframe height dynamically
 */
export function setFrameHeight(height: number): void {
    sendMessageToStreamlit("streamlit:setFrameHeight", { height });
}

/**
 * Send line data to Python
 */
export function setComponentValue(lines: Lines): void {
    const data = lines.map(line => line.map(p => [p.x, p.y]));
    sendMessageToStreamlit("streamlit:setComponentValue", { value: data });
}

/**
 * Send zoom state to Python (includes lines to prevent data loss)
 */
export function sendZoomState(
    lines: Lines,
    xRange: [number, number],
    yRange: [number, number],
    zoomLevel: number
): void {
    const linesData = lines.map(line => line.map(p => [p.x, p.y]));
    const zoomState: ZoomState = {
        type: 'zoom',
        lines: linesData,
        xRange,
        yRange,
        zoomLevel
    };
    sendMessageToStreamlit("streamlit:setComponentValue", { value: zoomState });
}
```

Create the file:
```bash
cat > src/utils/streamlit.ts << 'EOF'
[paste content above]
EOF
```

### Step 3.4: Commit Utilities

```bash
git add chart_editor/frontend/src/utils/
git commit -m "Utils: Add typed utility functions

- Helper functions (clone, sort, debounce, etc.)
- Coordinate transformation (data <-> canvas)
- Streamlit communication (messaging, height, data)
- All functions fully typed with JSDoc"
```

---

## Phase 4: Debug System Migration (2 hours)

**File**: `chart_editor/frontend/src/debug/logger.ts`
```typescript
import type { LogEntry, LogType } from '../types';
import { CONFIG } from '../types/constants';

export class DebugLogger {
    private entries: LogEntry[] = [];
    private container: HTMLElement | null = null;
    private isVisible: boolean = false;

    constructor() {
        this.container = document.getElementById('debugLog');
    }

    log(action: string, data?: unknown, type: LogType = 'action'): void {
        const entry: LogEntry = {
            timestamp: new Date().toLocaleTimeString(),
            action,
            data,
            type
        };

        this.entries.push(entry);

        // Limit entries
        if (this.entries.length > CONFIG.MAX_DEBUG_LOG_ENTRIES) {
            this.entries.shift();
        }

        this.render();
    }

    private render(): void {
        if (!this.container) return;

        this.container.innerHTML = this.entries
            .map(entry => {
                const dataHTML = entry.data !== undefined
                    ? `<span class="data">${this.formatData(entry.data)}</span>`
                    : '';

                return `
                    <div class="log-entry ${entry.type}">
                        <span class="timestamp">[${entry.timestamp}]</span>
                        <span class="action">${entry.action}</span>
                        ${dataHTML}
                    </div>
                `;
            })
            .join('');

        // Auto-scroll to bottom
        this.container.scrollTop = this.container.scrollHeight;
    }

    private formatData(data: unknown): string {
        if (typeof data === 'object' && data !== null) {
            return JSON.stringify(data, null, 2);
        }
        return String(data);
    }

    toggle(): void {
        const logEl = document.getElementById('debugLog');
        const toggleBtn = document.getElementById('debugToggle');

        if (!logEl || !toggleBtn) return;

        this.isVisible = !this.isVisible;

        if (this.isVisible) {
            logEl.classList.remove('hidden');
            toggleBtn.textContent = 'Hide Debug Log';
            toggleBtn.classList.add('active');
        } else {
            logEl.classList.add('hidden');
            toggleBtn.textContent = 'Show Debug Log';
            toggleBtn.classList.remove('active');
        }
    }

    clear(): void {
        this.entries = [];
        this.render();
    }
}

// Export singleton instance
export const debugLog = new DebugLogger();
```

Create the file:
```bash
cat > src/debug/logger.ts << 'EOF'
[paste content above]
EOF

git add chart_editor/frontend/src/debug/
git commit -m "Debug: Migrate debug logging system to TypeScript

- Create DebugLogger class with type safety
- Typed log entries and log types
- Export singleton instance for global use"
```

---

## Phase 5: Main Class Migration (2-3 days)

This is the largest piece - the ChartEditor class. Due to length, I'll provide the structure and first methods.

**File**: `chart_editor/frontend/src/components/ChartEditor.ts` (Part 1)

```typescript
import type {
    ChartConfig,
    EditorState,
    Point,
    Line,
    Lines,
    PointReference,
    Range,
    Padding,
    TouchState,
    RangeSelectorState
} from '../types';
import { CONFIG } from '../types/constants';
import { deepCloneLines, debounce, clamp, lerp, easeOutCubic } from '../utils/helpers';
import { dataToCanvas, canvasToData, isInChartArea } from '../utils/coordinates';
import { setComponentValue, sendZoomState } from '../utils/streamlit';
import { debugLog } from '../debug/logger';

export class ChartEditor {
    // Canvas and context
    private canvas: HTMLCanvasElement;
    private ctx: CanvasRenderingContext2D;

    // State
    private state: EditorState;

    // Configuration
    private colors: string[] = [...CONFIG.DEFAULT_COLORS];
    private gridSnap: [number, number] | null = null;
    private disabled: boolean = false;
    private readOnly: boolean = false;
    private minPoints: number = 0;
    private maxPoints: number | null = null;
    private zoomEnabled: boolean = false;

    // Padding
    private padding: Padding = { ...CONFIG.PADDING };

    // Interaction tracking
    private clickStartTime: number = 0;
    private dragOriginalPos: Point | null = null;

    // Panning
    private isPanning: boolean = false;
    private panStartX: number = 0;
    private panStartY: number = 0;
    private panStartXRange: Range = [0, 0];
    private panStartYRange: Range = [0, 0];

    // History (undo/redo)
    private historyStack: Lines[] = [];
    private historyIndex: number = -1;

    // Animation
    private zoomAnimationId: number | null = null;

    // Touch state
    private touchState: TouchState = {
        touches: [],
        initialPinchDistance: null,
        initialZoomLevel: 1,
        initialXRange: null,
        initialYRange: null,
        pinchCenter: null
    };

    // Range selector
    private rangeSelector: RangeSelectorState = {
        enabled: false,
        dragging: null,
        startX: 0,
        startLeft: 0,
        startWidth: 0
    };

    // Debounced zoom callback
    private sendZoomStateDebounced: () => void;

    constructor(canvas: HTMLCanvasElement) {
        this.canvas = canvas;
        const ctx = canvas.getContext('2d');
        if (!ctx) {
            throw new Error('Failed to get 2D context from canvas');
        }
        this.ctx = ctx;

        // Initialize state
        this.state = {
            lines: [],
            savedLines: [],
            isEditing: false,
            activeLineIndex: 0,
            hoveredPoint: null,
            draggingPoint: null,
            selectedPoint: null,
            isDragging: false,
            xRange: [0, 100],
            yRange: [0, 1000],
            originalXRange: [0, 100],
            originalYRange: [0, 1000],
            zoomLevel: 1
        };

        // Setup debounced zoom callback
        this.sendZoomStateDebounced = debounce(() => {
            sendZoomState(
                this.state.lines,
                this.state.xRange,
                this.state.yRange,
                this.state.zoomLevel
            );
        }, CONFIG.ZOOM_DEBOUNCE_DELAY);

        // Bind methods
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

        debugLog.log('EDITOR_INIT', 'ChartEditor initialized');
    }

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

        // Keyboard
        this.canvas.setAttribute('tabindex', '0');
        this.canvas.addEventListener('keydown', this.handleKeyDown);
    }

    /**
     * Clean up event listeners (prevent memory leaks)
     */
    destroy(): void {
        this.canvas.removeEventListener('mousemove', this.handleMouseMove);
        this.canvas.removeEventListener('mousedown', this.handleMouseDown);
        this.canvas.removeEventListener('mouseup', this.handleMouseUp);
        this.canvas.removeEventListener('mouseleave', this.handleMouseLeave);
        this.canvas.removeEventListener('wheel', this.handleWheel);

        this.canvas.removeEventListener('touchstart', this.handleTouchStart);
        this.canvas.removeEventListener('touchmove', this.handleTouchMove);
        this.canvas.removeEventListener('touchend', this.handleTouchEnd);

        this.canvas.removeEventListener('keydown', this.handleKeyDown);

        if (this.zoomAnimationId !== null) {
            cancelAnimationFrame(this.zoomAnimationId);
        }

        debugLog.log('EDITOR_DESTROYED', 'ChartEditor cleaned up');
    }

    /**
     * Configure chart from Python data
     */
    setConfig(config: ChartConfig): void {
        debugLog.log('RECEIVED_FROM_PYTHON', { lines: config.lines }, 'info');

        // Parse incoming lines
        const incomingLines: Lines = config.lines.map(line =>
            line.map(p => ({ x: p[0], y: p[1] }))
        );

        // Only accept new data if NOT in editing mode
        if (!this.state.isEditing) {
            this.state.lines = incomingLines;
            this.state.savedLines = deepCloneLines(incomingLines);
            debugLog.log('DATA_APPLIED', 'Applied data from Python (not editing)', 'info');
        } else {
            debugLog.log('DATA_IGNORED', 'Ignored Python data (currently editing)', 'warn');
        }

        // Update configuration
        if (config.xRange) this.state.xRange = config.xRange;
        if (config.yRange) this.state.yRange = config.yRange;
        if (config.colors) this.colors = config.colors;
        if (config.gridSnap) this.gridSnap = config.gridSnap;

        this.canvas.width = config.width;
        this.canvas.height = config.height;

        this.disabled = config.disabled;
        this.readOnly = config.readOnly;
        this.minPoints = config.minPoints;
        this.maxPoints = config.maxPoints;
        this.zoomEnabled = config.zoomEnabled;

        // Set original ranges for zoom
        if (!this.state.originalXRange || this.state.originalXRange[0] === 0) {
            this.state.originalXRange = [...this.state.xRange];
            this.state.originalYRange = [...this.state.yRange];
        }

        // Apply disabled/read-only styles
        if (this.disabled) {
            this.canvas.classList.add('disabled');
        } else {
            this.canvas.classList.remove('disabled');
        }

        if (this.readOnly) {
            this.canvas.classList.add('read-only');
        } else {
            this.canvas.classList.remove('read-only');
        }

        // Setup zoom controls if enabled
        if (this.zoomEnabled) {
            const rangeSelector = document.getElementById('rangeSelector');
            if (rangeSelector) {
                rangeSelector.classList.remove('hidden');
                this.setupRangeSelector();
            }
        }

        // Update UI
        this.updateRangeInputs();
        this.updateLineSelector();
        this.draw();

        // Initialize history
        this.initHistory();
    }

    // ... (more methods to follow in next parts)
}
```

Due to length constraints, I'll provide the migration plan overview for the rest:

### Step 5.1: Create Main Class File

```bash
# Start with the foundation above
cat > src/components/ChartEditor.ts << 'EOF'
[paste ChartEditor class part 1]
EOF
```

### Step 5.2: Add Method Sections (Split into parts)

Create these additional method files:

```bash
# Create method modules
touch src/components/drawing.ts      # draw(), drawGrid(), drawAxes()
touch src/components/interaction.ts  # mouse handlers
touch src/components/keyboard.ts     # keyboard handlers
touch src/components/touch.ts        # touch handlers
touch src/components/zoom.ts         # zoom methods
touch src/components/history.ts      # undo/redo
```

Each file exports functions that take `ChartEditor` instance as first param.

### Step 5.3: Incremental Commit Strategy

Don't migrate all 2,000 lines at once! Do it in phases:

```bash
# Phase A: Core structure (Day 1)
- ChartEditor class skeleton
- State management
- Configuration methods

# Phase B: Drawing (Day 1)
- draw() method
- drawGrid()
- drawAxes()
- Rendering pipeline

# Phase C: Mouse interaction (Day 2)
- handleMouseMove()
- handleMouseDown()
- handleMouseUp()
- Point detection

# Phase D: Keyboard & Touch (Day 2)
- handleKeyDown()
- Touch handlers
- Mobile gestures

# Phase E: Zoom & Pan (Day 3)
- Zoom methods
- Pan methods
- Range selector
- Animation

# Phase F: History & Utilities (Day 3)
- Undo/redo
- Helper methods
- Final integration
```

Commit after each phase:
```bash
git add src/components/
git commit -m "Migrate: [Phase X] - [Description]"
```

---

## Phase 6: Main Entry Point (1 hour)

**File**: `chart_editor/frontend/src/main.ts`
```typescript
/**
 * Main entry point for Chart Editor component
 */

import { ChartEditor } from './components/ChartEditor';
import { setComponentReady, setFrameHeight } from './utils/streamlit';
import { debugLog } from './debug/logger';
import type { ChartConfig } from './types';

// Initialize when DOM is ready
function init(): void {
    debugLog.log('INIT', 'Starting component initialization');

    const canvas = document.getElementById('chartCanvas') as HTMLCanvasElement;
    if (!canvas) {
        console.error('Canvas element not found');
        return;
    }

    const editor = new ChartEditor(canvas);

    // Setup debug toggle button
    const debugToggle = document.getElementById('debugToggle');
    if (debugToggle) {
        debugToggle.addEventListener('click', () => {
            debugLog.toggle();
        });
    }

    // Setup Save/Cancel buttons
    const btnSave = document.getElementById('btnSave');
    const btnCancel = document.getElementById('btnCancel');

    if (btnSave) {
        btnSave.addEventListener('click', () => {
            editor.saveChanges();
        });
    }

    if (btnCancel) {
        btnCancel.addEventListener('click', () => {
            editor.cancelChanges();
        });
    }

    // Setup Undo/Redo buttons
    const btnUndo = document.getElementById('btnUndo');
    const btnRedo = document.getElementById('btnRedo');

    if (btnUndo) {
        btnUndo.addEventListener('click', () => {
            editor.undo();
        });
    }

    if (btnRedo) {
        btnRedo.addEventListener('click', () => {
            editor.redo();
        });
    }

    // Setup zoom buttons
    const btnZoomIn = document.getElementById('btnZoomIn');
    const btnZoomOut = document.getElementById('btnZoomOut');
    const btnFitToData = document.getElementById('btnFitToData');
    const btnResetZoom = document.getElementById('btnResetZoom');

    if (btnZoomIn) btnZoomIn.addEventListener('click', () => editor.zoomIn());
    if (btnZoomOut) btnZoomOut.addEventListener('click', () => editor.zoomOut());
    if (btnFitToData) btnFitToData.addEventListener('click', () => editor.fitToData());
    if (btnResetZoom) btnResetZoom.addEventListener('click', () => editor.resetZoom());

    // Setup range inputs
    const xMinInput = document.getElementById('xMin') as HTMLInputElement;
    const xMaxInput = document.getElementById('xMax') as HTMLInputElement;
    const yMinInput = document.getElementById('yMin') as HTMLInputElement;
    const yMaxInput = document.getElementById('yMax') as HTMLInputElement;

    if (xMinInput) {
        xMinInput.addEventListener('change', (e) => {
            editor.updateRange('x', 'min', (e.target as HTMLInputElement).value, e.target as HTMLInputElement);
        });
    }
    // ... similar for other inputs

    // Listen for messages from Streamlit
    window.addEventListener('message', (event) => {
        if (event.data.type === 'streamlit:render') {
            debugLog.log('STREAMLIT_RENDER', 'Received render message from Streamlit');

            const args = event.data.args as ChartConfig;
            editor.setConfig(args);

            // Auto-adjust height
            setFrameHeight(document.body.scrollHeight);
        }
    });

    // Notify Streamlit we're ready
    setComponentReady();

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        editor.destroy();
    });
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
```

Create the file:
```bash
cat > src/main.ts << 'EOF'
[paste content above]
EOF
```

---

## Phase 7: Update HTML (30 minutes)

**File**: `chart_editor/frontend/index.html` (simplified)

The new HTML just loads the compiled bundle:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chart Editor</title>

    <!-- Load compiled CSS (extract from current HTML lines 7-580) -->
    <link rel="stylesheet" href="dist/styles.css">
</head>
<body>
    <!-- Keep all HTML structure (lines 584-644) -->
    <div class="chart-container">
        <!-- ... existing HTML ... -->
    </div>

    <!-- Load compiled TypeScript bundle -->
    <script src="dist/bundle.js"></script>
</body>
</html>
```

**Action**: Extract CSS to separate file:
```bash
# Extract CSS from current index.html
sed -n '7,580p' index.html > dist/styles.css

# Update index.html to reference it
# (manually edit to remove <style> block and add <link>)
```

---

## Phase 8: Testing & Verification (1 day)

### Step 8.1: Build and Test

```bash
# Build TypeScript
npm run build

# Check output
ls -lh dist/
# Should see: bundle.js, bundle.js.map, types/

# Run tests
npm run typecheck  # Should pass with 0 errors

# Test in Streamlit
cd ../..
streamlit run demo.py
```

### Step 8.2: Regression Testing Checklist

Test all features work identically:

```
□ Add point by clicking
□ Remove point by clicking on it
□ Drag point to new position
□ Multiple lines (switch with buttons)
□ Grid snapping works
□ Zoom with mouse wheel
□ Pan with Ctrl+drag
□ Range selector (zoom brush)
□ Keyboard navigation (Tab, arrows)
□ Undo/redo (Ctrl+Z/Ctrl+Shift+Z)
□ Touch gestures (if mobile available)
□ Dark mode toggle
□ Save/Cancel buttons
□ Error messages (try invalid actions)
□ Constraints (min/max points)
□ Read-only mode
□ Disabled mode
```

### Step 8.3: Performance Testing

```bash
# Test with large dataset
python -c "
import streamlit as st
from chart_editor import chart_editor

# 1000 points
lines = [[(i, i*2) for i in range(1000)]]
chart_editor(lines=lines, x_range=(0, 1000), y_range=(0, 2000))
" | streamlit run /dev/stdin

# Measure FPS during drag
# Should be >30 FPS
```

---

## Phase 9: Documentation & Cleanup (2-3 hours)

### Step 9.1: Add Migration Notes to README

Add section to `README.md`:

```markdown
## Development

### TypeScript Build

This component is written in TypeScript and compiled to JavaScript.

**Prerequisites**:
- Node.js 16+ and npm

**Build**:
```bash
cd chart_editor/frontend
npm install
npm run build
```

**Development** (watch mode):
```bash
npm run watch
```

**Type checking**:
```bash
npm run typecheck
```

### File Structure

```
frontend/
├── src/              # TypeScript source (edit these)
│   ├── components/   # Main ChartEditor class
│   ├── types/        # Type definitions
│   ├── utils/        # Utilities
│   ├── debug/        # Debug logger
│   └── main.ts       # Entry point
├── dist/             # Compiled output (committed to git)
│   ├── bundle.js     # Compiled JavaScript
│   └── bundle.js.map # Source maps
├── index.html        # HTML template
└── package.json      # Dependencies
```
```

### Step 9.2: Create CHANGELOG

**File**: `chart_editor/CHANGELOG.md`
```markdown
# Changelog

## [2.0.0] - 2026-01-XX

### Added
- TypeScript migration with full type safety
- Exported type definitions for users
- Memory leak fix (event listener cleanup)
- Zoom event debouncing (performance improvement)
- Extract magic numbers to CONFIG constants

### Changed
- Build process now requires Node.js
- Pre-commit hook auto-builds TypeScript

### Fixed
- Memory leak on component unmount
- Performance issue with rapid zoom events

### Breaking Changes
- None (compiled output is backwards compatible)
```

### Step 9.3: Commit Final Migration

```bash
git add .
git commit -m "Migrate: Complete TypeScript migration (v2.0.0)

Major changes:
- Fully typed TypeScript codebase
- Separated concerns (types, utils, components)
- Added memory leak fixes
- Added zoom debouncing
- Extracted configuration constants
- Improved maintainability

Build process:
- npm run build compiles TS to JS
- Both source and compiled output committed
- Pre-commit hook ensures they stay in sync

Testing:
- All existing features work identically
- Performance tested with 1000 points
- Regression tests passed

See TYPESCRIPT-MIGRATION-PLAN.md for details."
```

---

## Phase 10: Rollback Plan (Just In Case)

If migration fails, you can quickly rollback:

```bash
# Restore backup
git checkout chart_editor/frontend/index.html.backup
mv chart_editor/frontend/index.html.backup chart_editor/frontend/index.html

# Remove TypeScript files
rm -rf chart_editor/frontend/src
rm -rf chart_editor/frontend/node_modules
rm chart_editor/frontend/package.json
rm chart_editor/frontend/tsconfig.json
rm chart_editor/frontend/rollup.config.js

# Commit rollback
git add chart_editor/frontend/
git commit -m "Rollback: Revert TypeScript migration"
```

---

## Timeline Summary

| Phase | Task | Estimated Time |
|-------|------|---------------|
| 0 | Pre-Migration Prep | 1 hour |
| 1 | Project Setup | 2-3 hours |
| 2 | Type Definitions | 4-6 hours |
| 3 | Utilities Migration | 3-4 hours |
| 4 | Debug System | 2 hours |
| 5 | Main Class Migration | 2-3 days |
| 6 | Main Entry Point | 1 hour |
| 7 | Update HTML | 30 minutes |
| 8 | Testing & Verification | 1 day |
| 9 | Documentation | 2-3 hours |
| **Total** | | **~40 hours (5 days)** |

---

## Next Steps

1. **Review this plan** - Any questions or concerns?
2. **Schedule migration** - Block out 1 week
3. **Create feature branch** - `git checkout -b feature/typescript-migration`
4. **Start with Phase 0** - Follow step-by-step
5. **Commit frequently** - After each major section
6. **Test continuously** - Don't wait until the end

---

## Questions & Troubleshooting

### Q: Should I migrate everything at once?
**A**: No! Do it incrementally:
1. Setup (Phases 0-1)
2. Types & Utils (Phases 2-4)
3. Main class in small pieces (Phase 5)
4. Integration & testing (Phases 6-8)

### Q: What if TypeScript errors are overwhelming?
**A**: Use `// @ts-ignore` temporarily:
```typescript
// @ts-ignore - TODO: Fix this type error
const value = someComplexFunction();
```

Then fix later. Goal is working code first, perfect types second.

### Q: How do I debug bundle issues?
**A**:
```bash
# Check bundle size
ls -lh dist/bundle.js

# Test bundle in browser console
npm run build
open index.html  # In browser
# Check console for errors
```

### Q: What if build is too slow?
**A**: Disable source maps in production:
```javascript
// rollup.config.js
output: {
    sourcemap: !production  // Only in dev
}
```

---

## Success Criteria

Migration is complete when:

✅ All TypeScript files compile without errors (`npm run typecheck`)
✅ Bundle size is <200KB (unminified)
✅ All features work identically to vanilla JS version
✅ Regression tests pass 100%
✅ Performance is equal or better (FPS, memory)
✅ Git history is clean with meaningful commits
✅ Documentation updated (README, CHANGELOG)
✅ Pre-commit hook works automatically

---

**Ready to start?** Let me know and I'll help with each phase!
