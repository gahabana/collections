# Streamlit Chart Editor Component

An interactive 2D chart editor component for Streamlit that allows users to create and modify lines by adding, removing, and dragging points.

## Features

- **Interactive Editing**: Add points by clicking, remove by clicking on dots, drag to reposition
- **Multiple Lines**: Support for up to 5 lines with distinct colors
- **Auto-sorting**: Points are automatically sorted by X coordinate
- **Configurable Ranges**: Adjustable X and Y axis ranges
- **Grid Snapping**: Optional snap-to-grid for precise positioning
- **Real-time Updates**: Changes are immediately reflected in your Python code
- **Customizable**: Labels, titles, colors, and dimensions

## Installation

1. Ensure you have Streamlit installed:
   ```bash
   pip install streamlit
   ```

2. Clone or copy this component to your project:
   ```
   streamlit-components/
   ├── chart_editor/
   │   ├── __init__.py
   │   └── frontend/
   │       └── index.html
   └── demo.py
   ```

## Quick Start

```python
import streamlit as st
from chart_editor import chart_editor

# Create a simple chart editor
lines = chart_editor(
    lines=[[(0, 500), (100, 500)]],  # Initial horizontal line
    x_range=(0, 100),
    y_range=(0, 1000),
    title="My Chart",
    key="my_chart"
)

# Use the returned data
st.write(f"Lines: {lines}")
```

## API Reference

### `chart_editor()`

Main function to create the chart editor component.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `lines` | `List[List[Tuple[float, float]]]` | `[]` | List of lines, each line is a list of (x, y) tuples |
| `x_range` | `Tuple[float, float]` | `(0, 100)` | Min/max range for X axis |
| `y_range` | `Tuple[float, float]` | `(0, 1000)` | Min/max range for Y axis |
| `colors` | `List[str]` | `["#FF6B6B", ...]` | Colors for each line (hex format) |
| `grid_snap` | `Tuple[float, float]` | `None` | Grid snap as (x%, y%) of axis range |
| `title` | `str` | `""` | Chart title |
| `x_label` | `str` | `""` | X axis label |
| `y_label` | `str` | `""` | Y axis label |
| `width` | `int` | `700` | Component width in pixels |
| `height` | `int` | `450` | Component height in pixels |
| `key` | `str` | `None` | Unique key for component instance |

#### Returns

`List[List[Tuple[float, float]]]` - Updated list of lines with (x, y) coordinates, sorted by X.

### Helper Functions

#### `create_horizontal_line(y_value, x_range=(0, 100))`

Create a horizontal line at a given Y value.

```python
line = create_horizontal_line(500)  # [(0, 500), (100, 500)]
```

#### `create_line_from_points(*points)`

Create a line from multiple points (auto-sorted by X).

```python
line = create_line_from_points((50, 300), (0, 100), (100, 500))
# Returns: [(0, 100), (50, 300), (100, 500)]
```

## Usage Examples

### Basic Usage with Session State

```python
import streamlit as st
from chart_editor import chart_editor

# Initialize state
if "curves" not in st.session_state:
    st.session_state.curves = []

# Create editor
result = chart_editor(
    lines=st.session_state.curves,
    key="editor"
)

# Update state on change
st.session_state.curves = result
```

### With Grid Snapping

```python
# 5% snap on both axes = 20x20 grid
result = chart_editor(
    lines=initial_lines,
    grid_snap=(5, 5),  # 5% of each axis
    key="snapped_editor"
)
```

### Multiple Lines with Custom Colors

```python
result = chart_editor(
    lines=[
        [(0, 200), (100, 800)],  # Line 1
        [(0, 700), (100, 300)],  # Line 2
    ],
    colors=["#FF0000", "#00FF00"],  # Red, Green
    key="multi_line_editor"
)
```

### Custom Axis Ranges

```python
result = chart_editor(
    lines=my_lines,
    x_range=(-50, 50),      # Negative to positive
    y_range=(0, 100),       # Percentage scale
    x_label="Offset",
    y_label="Percentage",
    key="custom_range_editor"
)
```

## User Interactions

| Action | How to Perform |
|--------|----------------|
| Add point | Click on empty chart area |
| Remove point | Click on existing dot |
| Move point | Drag dot to new position |
| Switch active line | Click line button below chart |
| Add new line | Click "+ Add Line" button |
| Adjust ranges | Use input fields on the chart |

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

**Important**: Points are always sorted by X coordinate automatically.

## Running the Demo

```bash
cd streamlit-components
streamlit run demo.py
```

## Requirements

- Python 3.7+
- Streamlit >= 1.0.0

## Architecture

```
chart_editor/
├── __init__.py          # Python interface
└── frontend/
    └── index.html       # JavaScript component (HTML5 Canvas)
```

The component uses:
- **Python side**: Streamlit's `declare_component` for bidirectional communication
- **Frontend**: Vanilla JavaScript with HTML5 Canvas for rendering and interaction

## License

MIT License
