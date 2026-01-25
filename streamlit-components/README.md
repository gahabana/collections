# Streamlit Chart Editor Component

An interactive 2D chart editor for Streamlit that allows users to create and edit multi-line graphs with drag-and-drop functionality.

**Version**: 0.1.0

## Features

- **Interactive editing** - Add, remove, and drag points
- **Multiple lines** - Support for multiple lines with distinct colors
- **Grid snapping** - Optional snap-to-grid for precise positioning
- **Save/Cancel mode** - Edit mode with explicit save or cancel actions
- **Overlapping indicators** - Visual badges when points from different lines overlap
- **Active line selection** - Selected line renders on top for visibility
- **Constraints** - Min/max points per line, disabled (read-only) mode
- **Type-safe API** - Full type hints and validation

## Installation

```bash
# Copy the chart_editor directory to your project
cp -r chart_editor /path/to/your/project/
```

Requirements:
- Python 3.7+
- Streamlit >= 1.0.0

## Quick Start

```python
import streamlit as st
from chart_editor import chart_editor

# Basic usage
lines = chart_editor(
    lines=[[(0, 100), (50, 200), (100, 150)]],
    x_range=(0, 100),
    y_range=(0, 500),
    title="My Chart",
    key="chart1"
)

st.write(lines)
```

## API Reference

### `chart_editor()`

Main component function.

```python
from chart_editor import chart_editor

lines = chart_editor(
    lines=None,              # List of lines, each line is list of (x, y) tuples
    x_range=(0, 100),        # X-axis range (min, max)
    y_range=(0, 1000),       # Y-axis range (min, max)
    colors=None,             # List of hex colors for each line
    grid_snap=None,          # Grid snap as (x_percent, y_percent)
    title="",                # Chart title
    x_label="",              # X-axis label
    y_label="",              # Y-axis label
    width=700,               # Component width in pixels
    height=450,              # Component height in pixels
    key=None,                # Unique key for multiple instances
    disabled=False,          # Read-only mode
    min_points=0,            # Minimum points per line
    max_points=None,         # Maximum points per line
    on_change=None,          # Callback when data changes
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `lines` | `List[List[Tuple[float, float]]]` | `None` | List of lines, where each line is a list of (x, y) coordinate tuples. Points are auto-sorted by X. |
| `x_range` | `Tuple[float, float]` | `(0, 100)` | The (min, max) range for the X axis. |
| `y_range` | `Tuple[float, float]` | `(0, 1000)` | The (min, max) range for the Y axis. |
| `colors` | `List[str]` | `None` | List of hex colors (e.g., `"#FF6B6B"`). Defaults to colorblind-friendly palette. |
| `grid_snap` | `Tuple[float, float]` | `None` | Grid snap as percentages of axis range. `(5, 5)` snaps to 5% increments. |
| `title` | `str` | `""` | Chart title displayed at the top. |
| `x_label` | `str` | `""` | Label for the X axis. |
| `y_label` | `str` | `""` | Label for the Y axis. |
| `width` | `int` | `700` | Width of the component in pixels. |
| `height` | `int` | `450` | Height of the component in pixels. |
| `key` | `str` | `None` | Unique key for the component. **Required when using multiple instances.** |
| `disabled` | `bool` | `False` | If True, chart is displayed but not editable. |
| `min_points` | `int` | `0` | Minimum number of points required per line. |
| `max_points` | `int` | `None` | Maximum number of points allowed per line. |
| `on_change` | `Callable[[Lines], None]` | `None` | Callback function called when data changes. |

#### Returns

`List[List[Tuple[float, float]]]` - Updated list of lines with (x, y) coordinates, sorted by X.

#### Raises

- `ValueError` - If ranges are invalid or constraints are violated
- `TypeError` - If input types are incorrect

---

### Helper Functions

#### `create_horizontal_line()`

Create a horizontal line with two points.

```python
from chart_editor import create_horizontal_line

line = create_horizontal_line(y_value=500, x_range=(0, 100))
# Returns: [(0, 500), (100, 500)]
```

#### `create_vertical_line()`

Create a vertical line with two points.

```python
from chart_editor import create_vertical_line

line = create_vertical_line(x_value=50, y_range=(0, 1000))
# Returns: [(50, 0), (50, 1000)]
```

#### `create_line_from_points()`

Create a line from multiple points (auto-sorted by X).

```python
from chart_editor import create_line_from_points

line = create_line_from_points((50, 200), (0, 100), (100, 300))
# Returns: [(0, 100), (50, 200), (100, 300)]
```

#### `interpolate_line()`

Interpolate Y values for given X values along a line using linear interpolation.

```python
from chart_editor import interpolate_line

line = [(0, 0), (100, 100)]
results = interpolate_line(line, [25, 50, 75])
# Returns: [(25, 25.0), (50, 50.0), (75, 75.0)]
```

---

### Type Aliases

```python
from chart_editor import Point, Line, Lines, ColorList

# Point = Tuple[float, float]        # Single coordinate
# Line = List[Point]                 # List of points forming a line
# Lines = List[Line]                 # Multiple lines
# ColorList = List[str]              # List of hex color strings
```

---

### ChartConfig Dataclass

Reusable configuration container for chart settings.

```python
from chart_editor import ChartConfig, chart_editor

# Create reusable config
config = ChartConfig(
    x_range=(0, 60),
    y_range=(0, 200),
    title="Temperature Profile",
    x_label="Time (min)",
    y_label="Temp (C)",
    grid_snap=(5, 5)
)

# Use with chart_editor
lines = chart_editor(lines=data, **config.to_dict(), key="temp_chart")
```

---

### Constants

```python
from chart_editor import DEFAULT_COLORS, __version__

print(DEFAULT_COLORS)
# ['#FF6B6B', '#4ECDC4', '#A55EEA', '#45B7D1', '#F7DC6F', '#82E0AA', '#F8B500']

print(__version__)
# '0.1.0'
```

---

## Examples

### Basic Single Line

```python
import streamlit as st
from chart_editor import chart_editor, create_horizontal_line

st.title("Simple Chart Editor")

if "data" not in st.session_state:
    st.session_state.data = [create_horizontal_line(500, (0, 100))]

lines = chart_editor(
    lines=st.session_state.data,
    title="Edit the line",
    key="chart1"
)

if lines != st.session_state.data:
    st.session_state.data = lines
```

### Multiple Lines with Custom Colors

```python
lines = chart_editor(
    lines=[
        [(0, 100), (50, 300), (100, 200)],  # Line 1
        [(0, 400), (100, 400)],              # Line 2
        [(0, 600), (25, 700), (75, 500), (100, 650)],  # Line 3
    ],
    colors=["#FF6B6B", "#4ECDC4", "#A55EEA"],
    title="Multi-Line Chart",
    x_label="Time (s)",
    y_label="Value",
    key="multi_chart"
)
```

### With Grid Snapping

```python
lines = chart_editor(
    lines=[[(0, 500), (100, 500)]],
    grid_snap=(10, 10),  # Snap to 10% increments
    title="Grid Snap Enabled",
    key="snap_chart"
)
```

### Read-Only Display

```python
lines = chart_editor(
    lines=existing_data,
    disabled=True,  # View only, no editing
    title="Read-Only Chart",
    key="readonly_chart"
)
```

### With Point Constraints

```python
lines = chart_editor(
    lines=[[(0, 500), (100, 500)]],
    min_points=2,   # Can't have fewer than 2 points
    max_points=10,  # Can't have more than 10 points
    title="Constrained Chart",
    key="constrained_chart"
)
```

### Multiple Chart Instances

```python
col1, col2 = st.columns(2)

with col1:
    lines1 = chart_editor(
        lines=st.session_state.get("chart1_data", []),
        width=350,
        height=300,
        title="Chart 1",
        key="chart_instance_1"  # Unique key required!
    )

with col2:
    lines2 = chart_editor(
        lines=st.session_state.get("chart2_data", []),
        width=350,
        height=300,
        title="Chart 2",
        key="chart_instance_2"  # Different key!
    )
```

### Persistence to File

```python
import json
import os

SAVE_FILE = "chart_data.json"

def save_data(lines):
    with open(SAVE_FILE, 'w') as f:
        json.dump([[[x, y] for x, y in line] for line in lines], f)

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
        return [[(p[0], p[1]) for p in line] for line in data]
    return None

# Load on startup
if "data" not in st.session_state:
    st.session_state.data = load_data() or [[(0, 500), (100, 500)]]

lines = chart_editor(lines=st.session_state.data, key="persist_chart")

if st.button("Save"):
    save_data(lines)
    st.success("Saved!")
```

---

## User Interactions

| Action | Result |
|--------|--------|
| Click empty space | Add new point to active line |
| Click on dot | Remove the point |
| Drag dot | Move point to new position |
| Click line selector | Switch active line (renders on top) |
| Click "Save" | Commit changes to Python |
| Click "Cancel" | Revert to last saved state |

---

## Visual Indicators

| Indicator | Meaning |
|-----------|---------|
| Teal border glow | Unsaved changes (edit mode active) |
| Red flash | Action blocked (constraint violation) |
| Dashed ring around dot | Point overlaps with another line's point |
| Badge with number | Count of lines sharing same position |
| Tooltip on hover | Shows "Line N: (x, y)" coordinates |

---

## Running the Demos

```bash
cd streamlit-components

# Single chart demo with full configuration options
streamlit run demo.py

# Multi-chart demo (3 instances: small, medium, large)
streamlit run demo_multi.py
```

---

## Data Format

The component works with a list of lines, where each line is a list of (x, y) tuples:

```python
# Empty chart
lines = []

# One line with a horizontal segment
lines = [[(0, 500), (100, 500)]]

# Two lines
lines = [
    [(0, 100), (50, 300), (100, 200)],  # Line 1: 3 points
    [(0, 800), (100, 600)],              # Line 2: 2 points
]
```

**Note**: Points are always auto-sorted by X coordinate.

---

## Architecture

```
chart_editor/
├── __init__.py          # Python API with validation and helpers
└── frontend/
    └── index.html       # JavaScript component (HTML5 Canvas)
```

The component uses:
- **Python**: Streamlit's `declare_component` for bidirectional communication
- **Frontend**: Vanilla JavaScript with HTML5 Canvas for rendering

---

## Troubleshooting

### Multiple components show same data
Make sure each `chart_editor()` call has a unique `key` parameter.

### Changes not persisting after refresh
Use `st.session_state` to store data between reruns, or implement file-based persistence.

### Points snapping to wrong positions
Check that `grid_snap` values are reasonable (typically 1-25% of axis range).

### Can't remove points
Check if `min_points` constraint is set. The component won't allow removal below the minimum.

---

## License

MIT License
