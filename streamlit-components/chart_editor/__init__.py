"""
Streamlit Chart Editor Component

A reusable, interactive 2D chart editor that allows users to:
- View multiple lines on a graph
- Add points by clicking on empty space
- Remove points by clicking on existing dots
- Drag dots to modify coordinates
- All within configurable X/Y ranges with optional grid snapping
"""

import os
import streamlit.components.v1 as components
from typing import List, Tuple, Optional, Dict, Any

# Path to the frontend build
_FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

# Declare the component
_component_func = components.declare_component(
    "chart_editor",
    path=_FRONTEND_DIR
)


def chart_editor(
    lines: Optional[List[List[Tuple[float, float]]]] = None,
    x_range: Tuple[float, float] = (0, 100),
    y_range: Tuple[float, float] = (0, 1000),
    colors: Optional[List[str]] = None,
    grid_snap: Optional[Tuple[float, float]] = None,
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    width: int = 700,
    height: int = 450,
    key: Optional[str] = None,
) -> List[List[Tuple[float, float]]]:
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
        Defaults to a preset palette if not specified.

    grid_snap : Tuple[float, float], optional
        Grid snap as (x_percent, y_percent) of the respective axis range.
        For example, (1, 1) creates a 100x100 virtual grid.
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
        Unique key for the component instance.

    Returns
    -------
    List[List[Tuple[float, float]]]
        Updated list of lines with their (x, y) coordinates, sorted by X.
        Returns empty list [] if no lines/points exist.
    """

    # Default colors if not provided
    if colors is None:
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]

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
        key=key,
        default=prepared_lines,
    )

    # Convert back to list of tuples
    if component_value is None:
        return [list(map(tuple, line)) for line in prepared_lines]

    result = []
    for line in component_value:
        if line:
            # Sort by X and convert to tuples
            sorted_line = sorted(line, key=lambda p: p[0])
            result.append([(float(p[0]), float(p[1])) for p in sorted_line])
        else:
            result.append([])

    return result


def create_horizontal_line(y_value: float, x_range: Tuple[float, float] = (0, 100)) -> List[Tuple[float, float]]:
    """
    Helper function to create a horizontal line.

    Parameters
    ----------
    y_value : float
        The Y coordinate for the horizontal line.
    x_range : Tuple[float, float]
        The X range (min, max) for the line endpoints.

    Returns
    -------
    List[Tuple[float, float]]
        A line with two points forming a horizontal line.
    """
    return [(x_range[0], y_value), (x_range[1], y_value)]


def create_line_from_points(*points: Tuple[float, float]) -> List[Tuple[float, float]]:
    """
    Helper function to create a line from multiple points.
    Points will be auto-sorted by X coordinate.

    Parameters
    ----------
    *points : Tuple[float, float]
        Variable number of (x, y) coordinate tuples.

    Returns
    -------
    List[Tuple[float, float]]
        A sorted list of points forming a line.
    """
    return sorted(points, key=lambda p: p[0])
