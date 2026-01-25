"""
Multi-Chart Demo - Mimics real application usage with multiple chart instances.

Run with: streamlit run demo_multi.py
"""

import streamlit as st
from chart_editor import chart_editor, create_horizontal_line, create_line_from_points

st.set_page_config(
    page_title="Multi-Chart Editor",
    page_icon="📊",
    layout="wide"
)

# Chart configurations
CHART_CONFIGS = {
    "Chart A": {
        "title": "Temperature Profile",
        "x_label": "Time (min)",
        "y_label": "Temp (°C)",
        "x_range": (0, 60),
        "y_range": (0, 200),
        "colors": ["#FF6B6B", "#4ECDC4"],
        "size": "small"
    },
    "Chart B": {
        "title": "Pressure Curve",
        "x_label": "Time (min)",
        "y_label": "Pressure (bar)",
        "x_range": (0, 60),
        "y_range": (0, 10),
        "colors": ["#45B7D1", "#A55EEA"],
        "size": "medium"
    },
    "Chart C": {
        "title": "Flow Rate Control",
        "x_label": "Time (min)",
        "y_label": "Flow (L/min)",
        "x_range": (0, 60),
        "y_range": (0, 100),
        "colors": ["#96CEB4", "#FFEAA7", "#FF6B6B"],
        "size": "large"
    }
}

# Size configurations
SIZES = {
    "small": {"width": 350, "height": 250},
    "medium": {"width": 500, "height": 350},
    "large": {"width": 900, "height": 500}
}

# Initialize session state for each chart
for chart_name in CHART_CONFIGS:
    key = f"data_{chart_name}"
    if key not in st.session_state:
        config = CHART_CONFIGS[chart_name]
        x_range = config["x_range"]
        y_mid = (config["y_range"][0] + config["y_range"][1]) / 2
        st.session_state[key] = [
            create_horizontal_line(y_mid, x_range)
        ]

# Active chart selector
if "active_chart" not in st.session_state:
    st.session_state.active_chart = "Chart C"  # Default to large chart

# Header with chart selector
col_title, col_selector = st.columns([3, 1])
with col_title:
    st.title("Multi-Chart Editor Demo")
with col_selector:
    active_chart = st.selectbox(
        "Active Chart",
        options=list(CHART_CONFIGS.keys()),
        index=list(CHART_CONFIGS.keys()).index(st.session_state.active_chart),
        key="chart_selector"
    )
    st.session_state.active_chart = active_chart

st.markdown("---")

# Layout: Small and Medium on top row, Large below
col1, col2 = st.columns([1, 1.5])

# Chart A (Small)
with col1:
    config = CHART_CONFIGS["Chart A"]
    size = SIZES[config["size"]]
    is_active = st.session_state.active_chart == "Chart A"

    if is_active:
        st.markdown("##### 🔵 Chart A (Active)")
    else:
        st.markdown("##### Chart A")

    data_key = "data_Chart A"
    updated = chart_editor(
        lines=st.session_state[data_key],
        x_range=config["x_range"],
        y_range=config["y_range"],
        colors=config["colors"],
        title=config["title"],
        x_label=config["x_label"],
        y_label=config["y_label"],
        width=size["width"],
        height=size["height"],
        key="chart_a"
    )
    if updated != st.session_state[data_key]:
        st.session_state[data_key] = updated

# Chart B (Medium)
with col2:
    config = CHART_CONFIGS["Chart B"]
    size = SIZES[config["size"]]
    is_active = st.session_state.active_chart == "Chart B"

    if is_active:
        st.markdown("##### 🔵 Chart B (Active)")
    else:
        st.markdown("##### Chart B")

    data_key = "data_Chart B"
    updated = chart_editor(
        lines=st.session_state[data_key],
        x_range=config["x_range"],
        y_range=config["y_range"],
        colors=config["colors"],
        title=config["title"],
        x_label=config["x_label"],
        y_label=config["y_label"],
        width=size["width"],
        height=size["height"],
        key="chart_b"
    )
    if updated != st.session_state[data_key]:
        st.session_state[data_key] = updated

st.markdown("---")

# Chart C (Large) - Full width
config = CHART_CONFIGS["Chart C"]
size = SIZES[config["size"]]
is_active = st.session_state.active_chart == "Chart C"

if is_active:
    st.markdown("##### 🔵 Chart C (Active)")
else:
    st.markdown("##### Chart C")

data_key = "data_Chart C"
updated = chart_editor(
    lines=st.session_state[data_key],
    x_range=config["x_range"],
    y_range=config["y_range"],
    colors=config["colors"],
    title=config["title"],
    x_label=config["x_label"],
    y_label=config["y_label"],
    width=size["width"],
    height=size["height"],
    key="chart_c"
)
if updated != st.session_state[data_key]:
    st.session_state[data_key] = updated

# Sidebar: Show data for active chart
st.sidebar.header(f"Data: {st.session_state.active_chart}")

active_config = CHART_CONFIGS[st.session_state.active_chart]
active_data_key = f"data_{st.session_state.active_chart}"
active_data = st.session_state[active_data_key]

for i, line in enumerate(active_data):
    with st.sidebar.expander(f"Line {i+1} ({len(line)} points)", expanded=True):
        if line:
            for j, (x, y) in enumerate(line):
                st.text(f"[{j}] X: {x:>6.1f}  Y: {y:>6.1f}")
        else:
            st.text("(empty)")

# Sidebar: Quick actions
st.sidebar.markdown("---")
st.sidebar.subheader("Quick Actions")

if st.sidebar.button("Add Line to Active Chart"):
    config = CHART_CONFIGS[st.session_state.active_chart]
    y_range = config["y_range"]
    x_range = config["x_range"]
    y_val = y_range[0] + (y_range[1] - y_range[0]) * 0.3
    st.session_state[active_data_key].append(create_horizontal_line(y_val, x_range))
    st.rerun()

if st.sidebar.button("Reset Active Chart"):
    config = CHART_CONFIGS[st.session_state.active_chart]
    x_range = config["x_range"]
    y_mid = (config["y_range"][0] + config["y_range"][1]) / 2
    st.session_state[active_data_key] = [create_horizontal_line(y_mid, x_range)]
    st.rerun()

if st.sidebar.button("Reset All Charts"):
    for chart_name in CHART_CONFIGS:
        config = CHART_CONFIGS[chart_name]
        x_range = config["x_range"]
        y_mid = (config["y_range"][0] + config["y_range"][1]) / 2
        st.session_state[f"data_{chart_name}"] = [create_horizontal_line(y_mid, x_range)]
    st.rerun()

# Footer
st.markdown("---")
st.caption("Each chart operates independently. Select the active chart from the dropdown to view/manage its data in the sidebar.")
