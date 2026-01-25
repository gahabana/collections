"""
Demo application for the Chart Editor Streamlit component.

Run with: streamlit run demo.py
"""

import streamlit as st
from chart_editor import chart_editor, create_horizontal_line

st.set_page_config(
    page_title="Chart Editor Demo",
    page_icon="📈",
    layout="wide"
)

st.title("Chart Editor - Debug Demo")

# Initialize with a simple horizontal line (2 dots)
if "chart_lines" not in st.session_state:
    # Single horizontal line at y=500 with 2 points
    st.session_state.chart_lines = [
        [(0.0, 500.0), (100.0, 500.0)]
    ]

st.markdown("**Instructions:** Click to add | Click dot to remove | Drag to move")

# Sidebar for debug controls
st.sidebar.header("Debug Controls")

if st.sidebar.button("Reset to Horizontal Line"):
    st.session_state.chart_lines = [[(0.0, 500.0), (100.0, 500.0)]]
    st.rerun()

if st.sidebar.button("Clear All"):
    st.session_state.chart_lines = [[]]
    st.rerun()

if st.sidebar.button("Add 3 Points"):
    st.session_state.chart_lines = [[(0.0, 200.0), (50.0, 800.0), (100.0, 300.0)]]
    st.rerun()

# Main layout
col_chart, col_data = st.columns([2, 1])

with col_chart:
    # The chart editor component
    updated_lines = chart_editor(
        lines=st.session_state.chart_lines,
        x_range=(0, 100),
        y_range=(0, 1000),
        colors=["#FF6B6B", "#4ECDC4", "#45B7D1"],
        grid_snap=None,
        title="Debug Chart",
        x_label="X Axis",
        y_label="Y Axis",
        width=600,
        height=400,
        key="debug_chart"
    )

    # Check if data changed
    if updated_lines != st.session_state.chart_lines:
        st.session_state.chart_lines = updated_lines
        st.sidebar.success("Data updated from component!")

with col_data:
    st.subheader("Current Data (Full)")

    # Show ALL points - no truncation
    for i, line in enumerate(updated_lines):
        st.markdown(f"**Line {i + 1}** ({len(line)} points)")

        if line:
            # Display each point on its own line
            for j, (x, y) in enumerate(line):
                st.text(f"  [{j}] x={x:.4f}, y={y:.4f}")
        else:
            st.text("  (empty)")

        st.markdown("---")

    # Raw Python representation
    st.subheader("Raw Data")
    st.code(f"lines = {updated_lines}", language="python")

# Session state debug
st.sidebar.markdown("---")
st.sidebar.subheader("Session State")
st.sidebar.json({
    "chart_lines": st.session_state.chart_lines
})
