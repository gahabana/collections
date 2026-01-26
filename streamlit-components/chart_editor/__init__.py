"""
Streamlit Chart Editor Component

A reusable, interactive 2D chart editor that allows users to:
- View multiple lines on a graph
- Add points by clicking on empty space
- Remove points by clicking on existing dots
- Drag dots to modify coordinates
- All within configurable X/Y ranges with optional grid snapping

Example usage:
    >>> from chart_editor import chart_editor
    >>> lines = chart_editor(
    ...     lines=[[(0, 100), (50, 200), (100, 150)]],
    ...     x_range=(0, 100),
    ...     y_range=(0, 500),
    ...     title="My Chart"
    ... )
"""

__version__ = "1.0.0"

import os
import streamlit.components.v1 as components
from typing import List, Tuple, Optional, Callable, Union, Literal
from dataclasses import dataclass, field

# Type aliases for better readability
Point = Tuple[float, float]
Line = List[Point]
Lines = List[Line]
ColorList = List[str]

# Path to the frontend build
_FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

# Declare the component
_component_func = components.declare_component(
    "chart_editor",
    path=_FRONTEND_DIR
)

# Default color palette (colorblind-friendly)
DEFAULT_COLORS: ColorList = [
    "#FF6B6B",  # Coral Red
    "#4ECDC4",  # Teal
    "#A55EEA",  # Purple
    "#45B7D1",  # Sky Blue
    "#F7DC6F",  # Yellow
    "#82E0AA",  # Green
    "#F8B500",  # Orange
]


@dataclass
class ChartConfig:
    """Configuration dataclass for chart_editor.

    Useful for storing and reusing chart configurations.

    Example:
        >>> config = ChartConfig(
        ...     x_range=(0, 60),
        ...     y_range=(0, 200),
        ...     title="Temperature Profile",
        ...     x_label="Time (min)",
        ...     y_label="Temp (°C)"
        ... )
        >>> lines = chart_editor(lines=data, **config.to_dict())
    """
    x_range: Tuple[float, float] = (0, 100)
    y_range: Tuple[float, float] = (0, 1000)
    colors: Optional[ColorList] = None
    grid_snap: Optional[Tuple[float, float]] = None
    title: str = ""
    x_label: str = ""
    y_label: str = ""
    width: int = 700
    height: int = 450

    def to_dict(self) -> dict:
        """Convert to dictionary for passing to chart_editor."""
        return {
            "x_range": self.x_range,
            "y_range": self.y_range,
            "colors": self.colors,
            "grid_snap": self.grid_snap,
            "title": self.title,
            "x_label": self.x_label,
            "y_label": self.y_label,
            "width": self.width,
            "height": self.height,
        }


def validate_lines(lines: Optional[Lines], x_range: Tuple[float, float], y_range: Tuple[float, float]) -> None:
    """Validate lines data and raise clear errors if invalid.

    Raises:
        ValueError: If lines contain invalid data
        TypeError: If lines are not the expected type
    """
    if lines is None:
        return

    if not isinstance(lines, list):
        raise TypeError(f"lines must be a list, got {type(lines).__name__}")

    for i, line in enumerate(lines):
        if not isinstance(line, list):
            raise TypeError(f"lines[{i}] must be a list, got {type(line).__name__}")

        for j, point in enumerate(line):
            if not isinstance(point, (list, tuple)) or len(point) != 2:
                raise TypeError(
                    f"lines[{i}][{j}] must be a tuple/list of (x, y), got {point}"
                )

            x, y = point
            try:
                x, y = float(x), float(y)
            except (TypeError, ValueError):
                raise TypeError(
                    f"lines[{i}][{j}] coordinates must be numeric, got ({x}, {y})"
                )


def validate_range(range_tuple: Tuple[float, float], name: str) -> None:
    """Validate that a range tuple is valid.

    Raises:
        ValueError: If range is invalid
    """
    if not isinstance(range_tuple, (list, tuple)) or len(range_tuple) != 2:
        raise ValueError(f"{name} must be a tuple of (min, max)")

    min_val, max_val = range_tuple
    if min_val >= max_val:
        raise ValueError(f"{name} min ({min_val}) must be less than max ({max_val})")


def chart_editor(
    lines: Optional[Lines] = None,
    x_range: Tuple[float, float] = (0, 100),
    y_range: Tuple[float, float] = (0, 1000),
    colors: Optional[ColorList] = None,
    grid_snap: Optional[Tuple[float, float]] = None,
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    width: int = 700,
    height: int = 450,
    key: Optional[str] = None,
    disabled: bool = False,
    min_points: int = 0,
    max_points: Optional[int] = None,
    on_change: Optional[Callable[[Lines], None]] = None,
) -> Lines:
    """
    Create an interactive chart editor component.

    Parameters
    ----------
    lines : List[List[Tuple[float, float]]], optional
        List of lines, where each line is a list of (x, y) coordinate tuples.
        Points will be auto-sorted by X. Default is empty list (no lines).

    x_range : Tuple[float, float], default (0, 100)
        The (min, max) range for the X axis.

    y_range : Tuple[float, float], default (0, 1000)
        The (min, max) range for the Y axis.

    colors : List[str], optional
        List of colors for each line (hex format like "#FF6B6B").
        Defaults to a colorblind-friendly palette if not specified.

    grid_snap : Tuple[float, float], optional
        Grid snap as (x_percent, y_percent) of the respective axis range.
        For example, (5, 5) snaps to 5% increments of each axis.
        None means no snapping (free positioning).

    title : str, default ""
        Chart title displayed at the top.

    x_label : str, default ""
        Label for the X axis.

    y_label : str, default ""
        Label for the Y axis.

    width : int, default 700
        Width of the component in pixels.

    height : int, default 450
        Height of the component in pixels.

    key : str, optional
        Unique key for the component instance. Required when using multiple
        chart_editor instances on the same page.

    disabled : bool, default False
        If True, the chart is displayed but not editable.

    min_points : int, default 0
        Minimum number of points required per line.
        Setting to 2 ensures lines always have at least 2 points.

    max_points : int, optional
        Maximum number of points allowed per line. None means unlimited.

    on_change : Callable[[Lines], None], optional
        Callback function called when the chart data changes.
        Receives the new lines data as argument.

    Returns
    -------
    List[List[Tuple[float, float]]]
        Updated list of lines with their (x, y) coordinates, sorted by X.
        Returns empty list [] if no lines/points exist.

    Raises
    ------
    ValueError
        If ranges are invalid or constraints are violated.
    TypeError
        If input types are incorrect.

    Examples
    --------
    Basic usage with a single line:

    >>> lines = chart_editor(
    ...     lines=[[(0, 100), (50, 200), (100, 150)]],
    ...     x_range=(0, 100),
    ...     y_range=(0, 500)
    ... )

    Multiple lines with custom colors:

    >>> lines = chart_editor(
    ...     lines=[
    ...         [(0, 100), (100, 100)],  # Line 1
    ...         [(0, 200), (100, 200)],  # Line 2
    ...     ],
    ...     colors=["#FF0000", "#00FF00"],
    ...     title="Two Lines"
    ... )

    With grid snapping (5% increments):

    >>> lines = chart_editor(
    ...     lines=[[(0, 500), (100, 500)]],
    ...     grid_snap=(5, 5)
    ... )
    """
    # Validate inputs
    validate_range(x_range, "x_range")
    validate_range(y_range, "y_range")
    validate_lines(lines, x_range, y_range)

    if grid_snap is not None:
        if not isinstance(grid_snap, (list, tuple)) or len(grid_snap) != 2:
            raise ValueError("grid_snap must be a tuple of (x_percent, y_percent)")
        if grid_snap[0] <= 0 or grid_snap[1] <= 0:
            raise ValueError("grid_snap percentages must be positive")

    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive integers")

    # Default colors if not provided
    if colors is None:
        colors = DEFAULT_COLORS.copy()

    # Initialize lines if None
    if lines is None:
        lines = []

    # Prepare lines data - ensure sorted by X and convert to list format
    prepared_lines = []
    for line in lines:
        if line:
            # Sort by X coordinate
            sorted_line = sorted(line, key=lambda p: p[0])
            # Convert to list of [x, y] for JSON serialization
            prepared_lines.append([[float(p[0]), float(p[1])] for p in sorted_line])
        else:
            prepared_lines.append([])

    # Call the component
    component_value = _component_func(
        lines=prepared_lines,
        xRange=list(x_range),
        yRange=list(y_range),
        colors=colors,
        gridSnap=list(grid_snap) if grid_snap else None,
        title=title,
        xLabel=x_label,
        yLabel=y_label,
        width=width,
        height=height,
        disabled=disabled,
        minPoints=min_points,
        maxPoints=max_points,
        key=key,
        default=prepared_lines,
    )

    # Convert back to list of tuples
    if component_value is None:
        result = [list(map(tuple, line)) for line in prepared_lines]
    else:
        result = []
        for line in component_value:
            if line:
                # Sort by X and convert to tuples
                sorted_line = sorted(line, key=lambda p: p[0])
                result.append([(float(p[0]), float(p[1])) for p in sorted_line])
            else:
                result.append([])

    # Call on_change callback if data changed
    if on_change is not None and component_value is not None:
        # Check if data actually changed
        old_data = [list(map(tuple, line)) for line in prepared_lines]
        if result != old_data:
            on_change(result)

    return result


def create_horizontal_line(
    y_value: float,
    x_range: Tuple[float, float] = (0, 100)
) -> Line:
    """
    Create a horizontal line with two points.

    Parameters
    ----------
    y_value : float
        The Y coordinate for the horizontal line.
    x_range : Tuple[float, float], default (0, 100)
        The X range (min, max) for the line endpoints.

    Returns
    -------
    Line
        A line with two points forming a horizontal line.

    Examples
    --------
    >>> line = create_horizontal_line(500, (0, 100))
    >>> line
    [(0, 500), (100, 500)]
    """
    return [(x_range[0], y_value), (x_range[1], y_value)]


def create_vertical_line(
    x_value: float,
    y_range: Tuple[float, float] = (0, 1000)
) -> Line:
    """
    Create a vertical line with two points.

    Parameters
    ----------
    x_value : float
        The X coordinate for the vertical line.
    y_range : Tuple[float, float], default (0, 1000)
        The Y range (min, max) for the line endpoints.

    Returns
    -------
    Line
        A line with two points forming a vertical line.

    Examples
    --------
    >>> line = create_vertical_line(50, (0, 1000))
    >>> line
    [(50, 0), (50, 1000)]
    """
    return [(x_value, y_range[0]), (x_value, y_range[1])]


def create_line_from_points(*points: Point) -> Line:
    """
    Create a line from multiple points (auto-sorted by X).

    Parameters
    ----------
    *points : Tuple[float, float]
        Variable number of (x, y) coordinate tuples.

    Returns
    -------
    Line
        A sorted list of points forming a line.

    Examples
    --------
    >>> line = create_line_from_points((50, 200), (0, 100), (100, 300))
    >>> line
    [(0, 100), (50, 200), (100, 300)]
    """
    return sorted(points, key=lambda p: p[0])


def interpolate_line(
    line: Line,
    x_values: List[float]
) -> List[Tuple[float, Optional[float]]]:
    """
    Interpolate Y values for given X values along a line.

    Uses linear interpolation between points. Returns None for X values
    outside the line's X range.

    Parameters
    ----------
    line : Line
        The line to interpolate along.
    x_values : List[float]
        X values to get Y values for.

    Returns
    -------
    List[Tuple[float, Optional[float]]]
        List of (x, y) tuples. Y is None if x is outside the line's range.

    Examples
    --------
    >>> line = [(0, 0), (100, 100)]
    >>> interpolate_line(line, [25, 50, 75])
    [(25, 25.0), (50, 50.0), (75, 75.0)]
    """
    if not line or len(line) < 2:
        return [(x, None) for x in x_values]

    sorted_line = sorted(line, key=lambda p: p[0])
    results = []

    for x in x_values:
        # Check bounds
        if x < sorted_line[0][0] or x > sorted_line[-1][0]:
            results.append((x, None))
            continue

        # Find surrounding points
        for i in range(len(sorted_line) - 1):
            x1, y1 = sorted_line[i]
            x2, y2 = sorted_line[i + 1]

            if x1 <= x <= x2:
                # Linear interpolation
                if x2 == x1:
                    y = y1
                else:
                    t = (x - x1) / (x2 - x1)
                    y = y1 + t * (y2 - y1)
                results.append((x, y))
                break

    return results


# Import object-oriented API
from .chart_object import ChartEditor, get_chart


# Export public API
__all__ = [
    # Main component (functional)
    "chart_editor",

    # Object-oriented API
    "ChartEditor",
    "get_chart",

    # Type aliases
    "Point",
    "Line",
    "Lines",
    "ColorList",

    # Configuration
    "ChartConfig",
    "DEFAULT_COLORS",

    # Helper functions
    "create_horizontal_line",
    "create_vertical_line",
    "create_line_from_points",
    "interpolate_line",

    # Version
    "__version__",
]
