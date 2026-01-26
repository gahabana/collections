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

## Object-Oriented API

The OOP approach provides encapsulated state management, which is especially useful when working with **tabs** or multiple charts that need independent state.

### `ChartEditor` Class

```python
from chart_editor import ChartEditor, get_chart

# Create directly
chart = ChartEditor(
    key="my_chart",
    x_range=(0, 100),
    y_range=(0, 1000),
    colors=None,
    grid_snap=None,
    title="",
    x_label="",
    y_label="",
    width=700,
    height=450,
    disabled=False,
    min_points=0,
    max_points=None,
    initial_lines=None,
    on_change=None,
)

# Or use helper (recommended)
chart = get_chart("my_chart", title="Temperature", x_range=(0, 60))
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `lines` | `Lines` | Current saved line data (read/write) |
| `version` | `int` | State version, increments on each save |
| `line_count` | `int` | Number of lines in the chart |
| `total_points` | `int` | Total points across all lines |
| `has_pending_changes` | `bool` | Whether there are unapplied UI changes |

#### Methods

| Method | Description |
|--------|-------------|
| `render()` | Display the chart editor, returns current lines |
| `add_line(points)` | Add a new line, returns index |
| `remove_line(index)` | Remove line by index |
| `add_horizontal_line(y)` | Add horizontal line at Y value |
| `add_vertical_line(x)` | Add vertical line at X value |
| `get_line(index)` | Get specific line by index |
| `set_line(index, points)` | Replace points for a line |
| `clear()` | Remove all lines |
| `reset(initial_lines)` | Reset to initial state |
| `save_to_file(path)` | Save chart data to JSON file |
| `load_from_file(path)` | Load chart data from JSON file |
| `to_dict()` | Export state as dictionary |

### `get_chart()` Helper

Returns an existing ChartEditor instance or creates a new one. Recommended for most use cases.

```python
from chart_editor import get_chart

# Always returns the same instance for the same key
chart = get_chart("my_chart", title="Temperature", x_range=(0, 60))
chart.render()
```

---

## Functional vs OOP: When to Use Which

| Scenario | Recommended | Why |
|----------|-------------|-----|
| Single chart, simple page | Functional | Less boilerplate |
| Multiple charts in **tabs** | **OOP** | Prevents state loss on tab switch |
| Programmatic manipulation | **OOP** | Methods like `add_line()`, `clear()` |
| File persistence needed | **OOP** | Built-in `save_to_file()` / `load_from_file()` |
| Change callbacks | Either | Both support `on_change` |

### Why OOP Works Better with Tabs

When using tabs with the functional approach, switching tabs causes Streamlit to rerun. The inactive tab's `chart_editor()` returns stale/default data, which overwrites your saved state.

The OOP `ChartEditor.render()` method includes a check: `if result != self.lines` — it only updates state when data actually changed, preventing the overwrite.

---

## Comparison Examples

### Example 1: Basic Single Chart

**Functional approach:**
```python
import streamlit as st
from chart_editor import chart_editor

if "data" not in st.session_state:
    st.session_state.data = [[(0, 500), (100, 500)]]

lines = chart_editor(
    lines=st.session_state.data,
    title="My Chart",
    key="chart1"
)

st.session_state.data = lines
st.write(f"Points: {sum(len(line) for line in lines)}")
```

**OOP approach:**
```python
import streamlit as st
from chart_editor import get_chart

chart = get_chart(
    "chart1",
    title="My Chart",
    initial_lines=[[(0, 500), (100, 500)]]
)

chart.render()
st.write(f"Points: {chart.total_points}")
```

Both work identically for a single chart. OOP is slightly more concise.

---

### Example 2: Multiple Charts in Tabs (OOP Required)

**Functional approach (BROKEN - loses state on tab switch):**
```python
import streamlit as st
from chart_editor import chart_editor

# Initialize state
if "temp_data" not in st.session_state:
    st.session_state.temp_data = [[(0, 100), (60, 100)]]
if "pressure_data" not in st.session_state:
    st.session_state.pressure_data = [[(0, 5), (60, 5)]]

tab1, tab2 = st.tabs(["Temperature", "Pressure"])

with tab1:
    lines = chart_editor(
        lines=st.session_state.temp_data,
        title="Temperature",
        key="temp_chart"
    )
    st.session_state.temp_data = lines  # BUG: Overwrites with stale data!

with tab2:
    lines = chart_editor(
        lines=st.session_state.pressure_data,
        title="Pressure",
        key="pressure_chart"
    )
    st.session_state.pressure_data = lines  # BUG: Overwrites with stale data!
```

**OOP approach (WORKS correctly):**
```python
import streamlit as st
from chart_editor import get_chart

# Create chart objects - state is managed internally
temp_chart = get_chart(
    "temp_chart",
    title="Temperature",
    initial_lines=[[(0, 100), (60, 100)]]
)
pressure_chart = get_chart(
    "pressure_chart",
    title="Pressure",
    initial_lines=[[(0, 5), (60, 5)]]
)

tab1, tab2 = st.tabs(["Temperature", "Pressure"])

with tab1:
    temp_chart.render()  # Only updates when data actually changes
    st.caption(f"Lines: {temp_chart.line_count}")

with tab2:
    pressure_chart.render()  # Safe - won't overwrite temp_chart
    st.caption(f"Lines: {pressure_chart.line_count}")
```

---

### Example 3: Programmatic Manipulation with Buttons

**Functional approach:**
```python
import streamlit as st
from chart_editor import chart_editor, create_horizontal_line

if "data" not in st.session_state:
    st.session_state.data = [[(0, 500), (100, 500)]]

lines = chart_editor(lines=st.session_state.data, key="chart1")
st.session_state.data = lines

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Add Line"):
        st.session_state.data.append(create_horizontal_line(300, (0, 100)))
        st.rerun()

with col2:
    if st.button("Clear All"):
        st.session_state.data = []
        st.rerun()

with col3:
    if st.button("Reset"):
        st.session_state.data = [[(0, 500), (100, 500)]]
        st.rerun()
```

**OOP approach:**
```python
import streamlit as st
from chart_editor import get_chart

chart = get_chart("chart1", initial_lines=[[(0, 500), (100, 500)]])
chart.render()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Add Line"):
        chart.add_horizontal_line(300)
        st.rerun()

with col2:
    if st.button("Clear All"):
        chart.clear()
        st.rerun()

with col3:
    if st.button("Reset"):
        chart.reset([[(0, 500), (100, 500)]])
        st.rerun()
```

OOP provides cleaner methods for manipulation instead of manual list operations.

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

# OOP demo with tabs (demonstrates state persistence)
streamlit run demo_oop.py
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
