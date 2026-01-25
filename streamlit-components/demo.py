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

st.title("📈 Interactive Chart Editor Demo")
st.markdown("""
This demo showcases the **Chart Editor** component - an interactive 2D graph editor
that allows you to create and modify lines by adding, removing, and dragging points.
""")

# Sidebar configuration
st.sidebar.header("Configuration")

# X/Y Range configuration
st.sidebar.subheader("Axis Ranges")
col1, col2 = st.sidebar.columns(2)
x_min = col1.number_input("X Min", value=0.0, step=10.0)
x_max = col2.number_input("X Max", value=100.0, step=10.0)
y_min = col1.number_input("Y Min", value=0.0, step=100.0)
y_max = col2.number_input("Y Max", value=1000.0, step=100.0)

# Grid snap configuration
st.sidebar.subheader("Grid Snapping")
enable_snap = st.sidebar.checkbox("Enable Grid Snap", value=False)
if enable_snap:
    snap_x = st.sidebar.slider("X Snap (%)", 1, 20, 5)
    snap_y = st.sidebar.slider("Y Snap (%)", 1, 20, 5)
    grid_snap = (snap_x, snap_y)
else:
    grid_snap = None

# Labels
st.sidebar.subheader("Labels")
chart_title = st.sidebar.text_input("Chart Title", "My Interactive Chart")
x_label = st.sidebar.text_input("X Label", "Time")
y_label = st.sidebar.text_input("Y Label", "Value")

# Demo presets
st.sidebar.subheader("Demo Presets")
preset = st.sidebar.selectbox("Load Preset", [
    "Empty",
    "Single Horizontal Line",
    "Two Lines",
    "Complex Example"
])

# Initialize session state for lines
if "chart_lines" not in st.session_state:
    st.session_state.chart_lines = []

# Apply presets
if st.sidebar.button("Apply Preset"):
    if preset == "Empty":
        st.session_state.chart_lines = [[]]
    elif preset == "Single Horizontal Line":
        st.session_state.chart_lines = [
            create_horizontal_line(500, (x_min, x_max))
        ]
    elif preset == "Two Lines":
        st.session_state.chart_lines = [
            [(x_min, 200), (x_max, 800)],  # Ascending line
            [(x_min, 700), (x_max, 300)],  # Descending line
        ]
    elif preset == "Complex Example":
        st.session_state.chart_lines = [
            create_line_from_points(
                (0, 100), (25, 400), (50, 300), (75, 800), (100, 600)
            ),
            create_line_from_points(
                (0, 500), (50, 500), (100, 500)
            ),
            create_line_from_points(
                (10, 900), (30, 200), (70, 700), (90, 100)
            ),
        ]
    st.rerun()

# Main content
st.markdown("---")

# Instructions
with st.expander("📖 How to Use", expanded=False):
    st.markdown("""
    ### Interactions:
    - **Add a point**: Click anywhere on the empty chart area
    - **Remove a point**: Click on an existing dot
    - **Move a point**: Drag a dot to a new position
    - **Switch lines**: Click the line buttons below the chart
    - **Add new line**: Click the "+ Add Line" button

    ### Features:
    - Points are automatically sorted by X coordinate
    - Multiple lines supported (up to 5)
    - Adjustable X/Y ranges via the input fields on the chart
    - Optional grid snapping for precise positioning
    - Hover over points to see their coordinates
    """)

# Create two columns - chart and data view
col_chart, col_data = st.columns([3, 1])

with col_chart:
    # The chart editor component
    updated_lines = chart_editor(
        lines=st.session_state.chart_lines,
        x_range=(x_min, x_max),
        y_range=(y_min, y_max),
        colors=["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"],
        grid_snap=grid_snap,
        title=chart_title,
        x_label=x_label,
        y_label=y_label,
        width=700,
        height=450,
        key="demo_chart"
    )

    # Update session state if lines changed
    if updated_lines != st.session_state.chart_lines:
        st.session_state.chart_lines = updated_lines

with col_data:
    st.subheader("📊 Current Data")

    if not updated_lines or all(len(line) == 0 for line in updated_lines):
        st.info("No points on chart. Click on the chart to add points!")
    else:
        for i, line in enumerate(updated_lines):
            if line:
                color_map = {
                    0: "🔴", 1: "🔵", 2: "🟢", 3: "🟡", 4: "🟠"
                }
                st.markdown(f"**{color_map.get(i, '⚪')} Line {i + 1}** ({len(line)} points)")

                # Create a compact display
                points_str = ", ".join([f"({p[0]:.1f}, {p[1]:.1f})" for p in line[:5]])
                if len(line) > 5:
                    points_str += f" ... +{len(line) - 5} more"
                st.caption(points_str)

# Raw data section
st.markdown("---")
with st.expander("🔧 Raw Data (Python)", expanded=False):
    st.code(f"lines = {updated_lines}", language="python")

    st.markdown("**Copy-paste ready code:**")
    code = f'''from chart_editor import chart_editor

lines = chart_editor(
    lines={updated_lines},
    x_range=({x_min}, {x_max}),
    y_range=({y_min}, {y_max}),
    grid_snap={grid_snap},
    title="{chart_title}",
    x_label="{x_label}",
    y_label="{y_label}",
)
'''
    st.code(code, language="python")

# Usage example section
st.markdown("---")
st.subheader("💡 Integration Example")

st.markdown("""
Here's how you would use this component in your own Streamlit application:
""")

st.code('''
import streamlit as st
from chart_editor import chart_editor, create_horizontal_line

# Initialize state
if "my_curves" not in st.session_state:
    st.session_state.my_curves = [
        create_horizontal_line(500)  # Start with horizontal line at y=500
    ]

# Create the editor
result = chart_editor(
    lines=st.session_state.my_curves,
    x_range=(0, 100),
    y_range=(0, 1000),
    title="My Editor",
    key="my_editor"
)

# Update state on changes
st.session_state.my_curves = result

# Use the data
st.write(f"Number of lines: {len(result)}")
for i, line in enumerate(result):
    st.write(f"Line {i+1} has {len(line)} points")
''', language="python")

# Footer
st.markdown("---")
st.caption("Chart Editor Component Demo | Built with Streamlit")
