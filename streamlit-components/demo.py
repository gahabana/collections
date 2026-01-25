"""
Demo application for the Chart Editor Streamlit component.

Run with: streamlit run demo.py
"""

import streamlit as st
from chart_editor import chart_editor, create_horizontal_line, create_line_from_points

st.set_page_config(
    page_title="Chart Editor Demo",
    page_icon="📈",
    layout="wide"
)

st.title("Chart Editor Component - Full Demo")

# Sidebar configuration
st.sidebar.header("Chart Configuration")

# Axis ranges
st.sidebar.subheader("Axis Ranges")
col_x1, col_x2 = st.sidebar.columns(2)
x_min = col_x1.number_input("X Min", value=0.0, step=10.0)
x_max = col_x2.number_input("X Max", value=100.0, step=10.0)

col_y1, col_y2 = st.sidebar.columns(2)
y_min = col_y1.number_input("Y Min", value=0.0, step=100.0)
y_max = col_y2.number_input("Y Max", value=1000.0, step=100.0)

# Grid snap settings
st.sidebar.subheader("Grid Snap")
enable_grid_snap = st.sidebar.checkbox("Enable Grid Snap", value=False)
if enable_grid_snap:
    col_gx, col_gy = st.sidebar.columns(2)
    grid_snap_x = col_gx.slider("X Snap (%)", min_value=1, max_value=25, value=5)
    grid_snap_y = col_gy.slider("Y Snap (%)", min_value=1, max_value=25, value=5)
    grid_snap = (grid_snap_x, grid_snap_y)
else:
    grid_snap = None

# Labels
st.sidebar.subheader("Labels")
chart_title = st.sidebar.text_input("Chart Title", value="Interactive Chart Editor")
x_label = st.sidebar.text_input("X-Axis Label", value="Time (s)")
y_label = st.sidebar.text_input("Y-Axis Label", value="Value")

# Number of lines
st.sidebar.subheader("Lines")
num_lines = st.sidebar.selectbox("Number of Lines", options=[1, 2, 3], index=1)

# Line colors
default_colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]
colors = []
for i in range(num_lines):
    color = st.sidebar.color_picker(f"Line {i+1} Color", value=default_colors[i])
    colors.append(color)

# Initialize session state with the appropriate number of lines
if "chart_lines" not in st.session_state:
    st.session_state.chart_lines = [
        create_horizontal_line(500, (x_min, x_max)),  # Line 1
        create_horizontal_line(300, (x_min, x_max)),  # Line 2
    ]

# Ensure we have the right number of lines
while len(st.session_state.chart_lines) < num_lines:
    y_val = 500 - len(st.session_state.chart_lines) * 150
    st.session_state.chart_lines.append(create_horizontal_line(y_val, (x_min, x_max)))

while len(st.session_state.chart_lines) > num_lines:
    st.session_state.chart_lines.pop()

# Preset buttons
st.sidebar.markdown("---")
st.sidebar.subheader("Presets")

if st.sidebar.button("Reset to Horizontal Lines"):
    st.session_state.chart_lines = []
    for i in range(num_lines):
        y_val = 500 - i * 150
        st.session_state.chart_lines.append(create_horizontal_line(y_val, (x_min, x_max)))
    st.rerun()

if st.sidebar.button("Sample Zigzag Pattern"):
    st.session_state.chart_lines = []
    for i in range(num_lines):
        base_y = 300 + i * 200
        line = create_line_from_points(
            (x_min, base_y),
            (x_min + (x_max - x_min) * 0.25, base_y + 200),
            (x_min + (x_max - x_min) * 0.5, base_y - 100),
            (x_min + (x_max - x_min) * 0.75, base_y + 150),
            (x_max, base_y)
        )
        st.session_state.chart_lines.append(line)
    st.rerun()

if st.sidebar.button("Clear All Lines"):
    st.session_state.chart_lines = [[] for _ in range(num_lines)]
    st.rerun()

# Instructions
st.markdown("""
**Instructions:**
- **Add point:** Click on empty space on a line's path (or anywhere to add to nearest line)
- **Remove point:** Click on an existing dot
- **Move point:** Drag a dot to a new position
- **Save/Cancel:** Use the buttons that appear when you make changes
""")

if grid_snap:
    st.info(f"Grid snap enabled: {grid_snap[0]}% × {grid_snap[1]}%")

# Main layout
col_chart, col_data = st.columns([2, 1])

with col_chart:
    # The chart editor component
    updated_lines = chart_editor(
        lines=st.session_state.chart_lines,
        x_range=(x_min, x_max),
        y_range=(y_min, y_max),
        colors=colors[:num_lines],
        grid_snap=grid_snap,
        title=chart_title,
        x_label=x_label,
        y_label=y_label,
        width=700,
        height=450,
        key="main_chart"
    )

    # Check if data changed
    if updated_lines != st.session_state.chart_lines:
        st.session_state.chart_lines = updated_lines
        st.toast("Chart data updated!")

with col_data:
    st.subheader("Current Data")

    for i, line in enumerate(updated_lines):
        with st.expander(f"Line {i + 1} ({len(line)} points)", expanded=True):
            if line:
                # Create a small table view
                for j, (x, y) in enumerate(line):
                    st.text(f"[{j}] X: {x:>8.2f}  Y: {y:>8.2f}")
            else:
                st.text("(empty - click on chart to add points)")

    # Raw data for copying
    st.subheader("Raw Data")
    st.code(f"lines = {updated_lines}", language="python")

# Footer with component stats
st.markdown("---")
total_points = sum(len(line) for line in updated_lines)
st.caption(f"Total: {num_lines} line(s), {total_points} point(s) | Grid snap: {'On' if grid_snap else 'Off'}")
