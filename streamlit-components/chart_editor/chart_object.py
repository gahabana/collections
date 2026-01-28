"""
Object-oriented wrapper for chart_editor component.

Provides encapsulated state management and cleaner API for complex applications.
"""

import streamlit as st
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass, field
import json
import os

from . import (
    chart_editor as _chart_editor,
    create_horizontal_line,
    create_vertical_line,
    create_line_from_points,
    Point, Line, Lines, ColorList,
    ChartConfig,
)


class ChartEditor:
    """
    Object-oriented chart editor with encapsulated state.

    Unlike the functional `chart_editor()`, this class:
    - Manages its own state in session_state
    - Only updates when you call `save()` or `apply_changes()`
    - Works correctly with tabs (state persists across tab switches)
    - Provides methods for common operations

    Example:
        >>> chart = ChartEditor("my_chart", title="Temperature")
        >>> chart.render()  # Display the chart
        >>>
        >>> # Access data
        >>> print(chart.lines)
        >>>
        >>> # Modify programmatically
        >>> chart.add_line([(0, 100), (100, 200)])
        >>> chart.save_to_file("data.json")
    """

    def __init__(
        self,
        key: str,
        x_range: Tuple[float, float] = (0, 100),
        y_range: Tuple[float, float] = (0, 1000),
        colors: Optional[ColorList] = None,
        grid_snap: Optional[Tuple[float, float]] = None,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        width: int = 700,
        height: int = 450,
        disabled: bool = False,
        min_points: int = 0,
        max_points: Optional[int] = None,
        initial_lines: Optional[Lines] = None,
        on_change: Optional[Callable[[Lines], None]] = None,
        zoom_enabled: bool = False,
        read_only: bool = False,
    ):
        """
        Initialize a ChartEditor instance.

        Parameters
        ----------
        key : str
            Unique identifier for this chart. Used for session_state storage.
        initial_lines : Lines, optional
            Initial line data. Only used on first creation.
        on_change : Callable[[Lines], None], optional
            Callback function called when chart data changes.
            Receives the new lines data as argument.
            Called on UI edits and programmatic changes.

        Other parameters match chart_editor() function.
        """
        self.key = key
        self._state_key = f"_chart_obj_{key}"

        # Configuration (can be changed)
        self.x_range = x_range
        self.y_range = y_range
        self.colors = colors
        self.grid_snap = grid_snap
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.width = width
        self.height = height
        self.disabled = disabled
        self.min_points = min_points
        self.max_points = max_points
        self.on_change = on_change
        self.zoom_enabled = zoom_enabled
        self.read_only = read_only

        # Initialize state if needed
        if self._state_key not in st.session_state:
            st.session_state[self._state_key] = {
                "lines": initial_lines or [],
                "pending_changes": None,  # Holds changes before apply
                "version": 0,  # Increment on each save
            }

    @property
    def _state(self) -> dict:
        """Access internal state dict."""
        return st.session_state[self._state_key]

    @property
    def lines(self) -> Lines:
        """Get current saved line data."""
        return self._state["lines"]

    @lines.setter
    def lines(self, value: Lines):
        """Set line data directly."""
        old_lines = self._state["lines"]
        self._state["lines"] = value
        self._state["version"] += 1
        if value != old_lines:
            self._trigger_on_change()

    @property
    def version(self) -> int:
        """Get state version (increments on each save)."""
        return self._state["version"]

    @property
    def has_pending_changes(self) -> bool:
        """Check if there are unapplied changes from the UI."""
        return self._state["pending_changes"] is not None

    def _trigger_on_change(self):
        """Call the on_change callback if set."""
        if self.on_change is not None:
            self.on_change(self.lines)

    def render(self) -> Lines:
        """
        Render the chart editor component.

        Returns the current line data. Changes made in the UI are stored
        as pending until you call `apply_changes()`.

        Returns
        -------
        Lines
            Current line data (not including pending changes)
        """
        # Call the underlying component
        result = _chart_editor(
            lines=self.lines,
            x_range=self.x_range,
            y_range=self.y_range,
            colors=self.colors,
            grid_snap=self.grid_snap,
            title=self.title,
            x_label=self.x_label,
            y_label=self.y_label,
            width=self.width,
            height=self.height,
            key=self.key,
            disabled=self.disabled,
            min_points=self.min_points,
            max_points=self.max_points,
            zoom_enabled=self.zoom_enabled,
            read_only=self.read_only,
        )

        # Check if data changed
        if result != self.lines:
            # Store as pending changes (auto-apply for simplicity)
            self._state["lines"] = result
            self._state["version"] += 1
            self._trigger_on_change()

        return self.lines

    def apply_changes(self):
        """Apply pending changes from UI interactions."""
        if self._state["pending_changes"] is not None:
            self._state["lines"] = self._state["pending_changes"]
            self._state["pending_changes"] = None
            self._state["version"] += 1

    def discard_changes(self):
        """Discard pending changes."""
        self._state["pending_changes"] = None

    # ==================== Data Manipulation ====================

    def add_line(self, points: Optional[Line] = None) -> int:
        """
        Add a new line to the chart.

        Parameters
        ----------
        points : Line, optional
            Initial points for the line. If None, creates empty line.

        Returns
        -------
        int
            Index of the new line.
        """
        new_line = list(points) if points else []
        self._state["lines"].append(new_line)
        self._state["version"] += 1
        self._trigger_on_change()
        return len(self._state["lines"]) - 1

    def remove_line(self, index: int):
        """Remove a line by index."""
        if 0 <= index < len(self._state["lines"]):
            self._state["lines"].pop(index)
            self._state["version"] += 1
            self._trigger_on_change()

    def add_horizontal_line(self, y_value: float) -> int:
        """Add a horizontal line at the given Y value."""
        line = create_horizontal_line(y_value, self.x_range)
        return self.add_line(line)  # on_change triggered in add_line

    def add_vertical_line(self, x_value: float) -> int:
        """Add a vertical line at the given X value."""
        line = create_vertical_line(x_value, self.y_range)
        return self.add_line(line)  # on_change triggered in add_line

    def clear(self):
        """Remove all lines."""
        if self._state["lines"]:  # Only trigger if there was data
            self._state["lines"] = []
            self._state["version"] += 1
            self._trigger_on_change()

    def reset(self, initial_lines: Optional[Lines] = None):
        """Reset to initial state."""
        old_lines = self._state["lines"]
        self._state["lines"] = initial_lines or []
        self._state["pending_changes"] = None
        self._state["version"] += 1
        if self._state["lines"] != old_lines:
            self._trigger_on_change()

    # ==================== Persistence ====================

    def save_to_file(self, filepath: str):
        """
        Save chart data to a JSON file.

        Parameters
        ----------
        filepath : str
            Path to save the JSON file.
        """
        data = {
            "lines": [
                [[float(x), float(y)] for x, y in line]
                for line in self.lines
            ],
            "version": self.version,
            "config": {
                "x_range": self.x_range,
                "y_range": self.y_range,
                "title": self.title,
            }
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filepath: str) -> bool:
        """
        Load chart data from a JSON file.

        Parameters
        ----------
        filepath : str
            Path to the JSON file.

        Returns
        -------
        bool
            True if loaded successfully, False otherwise.
        """
        if not os.path.exists(filepath):
            return False

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            old_lines = self._state["lines"]
            self._state["lines"] = [
                [(float(p[0]), float(p[1])) for p in line]
                for line in data.get("lines", [])
            ]
            self._state["version"] += 1
            if self._state["lines"] != old_lines:
                self._trigger_on_change()
            return True
        except (json.JSONDecodeError, KeyError, TypeError):
            return False

    def to_dict(self) -> dict:
        """Export state as dictionary."""
        return {
            "key": self.key,
            "lines": self.lines,
            "version": self.version,
        }

    # ==================== Utility ====================

    def get_line(self, index: int) -> Optional[Line]:
        """Get a specific line by index."""
        if 0 <= index < len(self.lines):
            return self.lines[index]
        return None

    def set_line(self, index: int, points: Line):
        """Set points for a specific line."""
        if 0 <= index < len(self._state["lines"]):
            old_points = self._state["lines"][index]
            self._state["lines"][index] = list(points)
            self._state["version"] += 1
            if list(points) != old_points:
                self._trigger_on_change()

    @property
    def line_count(self) -> int:
        """Number of lines in the chart."""
        return len(self.lines)

    @property
    def total_points(self) -> int:
        """Total number of points across all lines."""
        return sum(len(line) for line in self.lines)

    def __repr__(self) -> str:
        return f"ChartEditor(key='{self.key}', lines={self.line_count}, points={self.total_points})"


# Convenience function to get or create a ChartEditor
def get_chart(key: str, **kwargs) -> ChartEditor:
    """
    Get or create a ChartEditor instance.

    This is useful for ensuring you always get the same instance
    for a given key, even across reruns.

    Example:
        >>> chart = get_chart("my_chart", title="Temperature", x_range=(0, 60))
        >>> chart.render()
    """
    # Store instance reference in session_state
    instance_key = f"_chart_instance_{key}"

    if instance_key not in st.session_state:
        st.session_state[instance_key] = ChartEditor(key, **kwargs)

    return st.session_state[instance_key]
