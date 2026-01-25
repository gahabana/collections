"""
Multi-Chart Demo - Mimics real application usage with multiple chart instances.

Run with: streamlit run demo_multi.py
"""

import json
import os
import streamlit as st
from chart_editor import chart_editor, create_horizontal_line, create_line_from_points

st.set_page_config(
    page_title="Multi-Chart Editor",
    page_icon="📊",
    layout="wide"
)

# Persistence file path
SAVE_FILE = os.path.join(os.path.dirname(__file__), "chart_data.json")

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


def get_default_data(chart_name: str):
    """Get default data for a chart."""
    config = CHART_CONFIGS[chart_name]
    x_range = config["x_range"]
    y_mid = (config["y_range"][0] + config["y_range"][1]) / 2
    return [create_horizontal_line(y_mid, x_range)]


def save_all_charts():
    """Save all chart data to JSON file."""
    data = {}
    for chart_name in CHART_CONFIGS:
        key = f"data_{chart_name}"
        if key in st.session_state:
            # Convert tuples to lists for JSON serialization
            data[chart_name] = [
                [[float(x), float(y)] for x, y in line]
                for line in st.session_state[key]
            ]
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    return True


def load_all_charts():
    """Load all chart data from JSON file."""
    if not os.path.exists(SAVE_FILE):
        return False
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
        for chart_name, lines in data.items():
            if chart_name in CHART_CONFIGS:
                key = f"data_{chart_name}"
                # Convert lists back to tuples
                st.session_state[key] = [
                    [(float(p[0]), float(p[1])) for p in line]
                    for line in lines
                ]
        return True
    except (json.JSONDecodeError, KeyError, TypeError):
        return False


def has_saved_data():
    """Check if saved data exists."""
    return os.path.exists(SAVE_FILE)

# Initialize session state for each chart
# On first load, try to restore from saved file
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    if has_saved_data():
        load_all_charts()
        st.session_state.loaded_from_file = True
    else:
        st.session_state.loaded_from_file = False

# Ensure all charts have data (use defaults if not loaded)
for chart_name in CHART_CONFIGS:
    key = f"data_{chart_name}"
    if key not in st.session_state:
        st.session_state[key] = get_default_data(chart_name)

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

# Sidebar: Persistence
st.sidebar.markdown("---")
st.sidebar.subheader("Persistence")

col_save, col_load = st.sidebar.columns(2)
with col_save:
    if st.button("Save All", use_container_width=True):
        if save_all_charts():
            st.toast("All charts saved!")
        else:
            st.error("Failed to save")

with col_load:
    if st.button("Load All", use_container_width=True, disabled=not has_saved_data()):
        if load_all_charts():
            st.toast("Charts loaded from file!")
            st.rerun()
        else:
            st.error("Failed to load")

if has_saved_data():
    st.sidebar.caption(f"Saved data exists: {os.path.basename(SAVE_FILE)}")
else:
    st.sidebar.caption("No saved data yet")

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
    st.session_state[active_data_key] = get_default_data(st.session_state.active_chart)
    st.rerun()

if st.sidebar.button("Reset All Charts"):
    for chart_name in CHART_CONFIGS:
        st.session_state[f"data_{chart_name}"] = get_default_data(chart_name)
    st.rerun()

# Footer
st.markdown("---")
load_status = " (loaded from saved file)" if st.session_state.get("loaded_from_file") else ""
st.caption(f"Each chart operates independently. Use Save All to persist data across refreshes.{load_status}")
