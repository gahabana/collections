"""
Object-Oriented Chart Editor Demo - Using ChartEditor class with tabs.

This demo shows how the object-oriented approach handles tabs correctly,
with state encapsulated in the ChartEditor object.

Run with: streamlit run demo_oop.py
"""

import streamlit as st
from chart_editor import ChartEditor, get_chart

st.set_page_config(
    page_title="OOP Chart Editor",
    page_icon="📊",
    layout="wide"
)

st.title("Object-Oriented Chart Editor")
st.markdown("Each chart is a `ChartEditor` object with encapsulated state.")

# Create chart objects (or get existing ones)
# These persist across tab switches because state is in session_state
chart_a = get_chart(
    "chart_a",
    title="Temperature Profile",
    x_range=(0, 60),
    y_range=(0, 200),
    x_label="Time (min)",
    y_label="Temp (°C)",
    colors=["#FF6B6B", "#4ECDC4"],
    initial_lines=[[(0, 100), (60, 100)]],  # Only used on first creation
)

chart_b = get_chart(
    "chart_b",
    title="Pressure Curve",
    x_range=(0, 60),
    y_range=(0, 10),
    x_label="Time (min)",
    y_label="Pressure (bar)",
    colors=["#45B7D1", "#A55EEA"],
    initial_lines=[[(0, 5), (60, 5)]],
)

chart_c = get_chart(
    "chart_c",
    title="Flow Rate",
    x_range=(0, 60),
    y_range=(0, 100),
    x_label="Time (min)",
    y_label="Flow (L/min)",
    colors=["#96CEB4", "#F7DC6F"],
    initial_lines=[[(0, 50), (60, 50)]],
)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Temperature", "Pressure", "Flow Rate"])

with tab1:
    st.subheader("Temperature Profile")
    chart_a.render()  # Just render - state is managed by the object

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Add Line", key="add_a"):
            chart_a.add_horizontal_line(50)
            st.rerun()
    with col2:
        if st.button("Clear", key="clear_a"):
            chart_a.clear()
            st.rerun()
    with col3:
        if st.button("Reset", key="reset_a"):
            chart_a.reset([[(0, 100), (60, 100)]])
            st.rerun()

    st.caption(f"Lines: {chart_a.line_count} | Points: {chart_a.total_points} | Version: {chart_a.version}")

with tab2:
    st.subheader("Pressure Curve")
    chart_b.render()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Add Line", key="add_b"):
            chart_b.add_horizontal_line(3)
            st.rerun()
    with col2:
        if st.button("Clear", key="clear_b"):
            chart_b.clear()
            st.rerun()
    with col3:
        if st.button("Reset", key="reset_b"):
            chart_b.reset([[(0, 5), (60, 5)]])
            st.rerun()

    st.caption(f"Lines: {chart_b.line_count} | Points: {chart_b.total_points} | Version: {chart_b.version}")

with tab3:
    st.subheader("Flow Rate Control")
    chart_c.render()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Add Line", key="add_c"):
            chart_c.add_horizontal_line(25)
            st.rerun()
    with col2:
        if st.button("Clear", key="clear_c"):
            chart_c.clear()
            st.rerun()
    with col3:
        if st.button("Reset", key="reset_c"):
            chart_c.reset([[(0, 50), (60, 50)]])
            st.rerun()

    st.caption(f"Lines: {chart_c.line_count} | Points: {chart_c.total_points} | Version: {chart_c.version}")

# Sidebar - Show all chart states
st.sidebar.header("All Charts State")

for name, chart in [("A: Temp", chart_a), ("B: Pressure", chart_b), ("C: Flow", chart_c)]:
    with st.sidebar.expander(f"{name} ({chart.line_count} lines)", expanded=False):
        for i, line in enumerate(chart.lines):
            st.text(f"Line {i+1}: {len(line)} pts")
            if line:
                st.code(str(line[:3]) + ("..." if len(line) > 3 else ""))

st.sidebar.markdown("---")

# Global actions
st.sidebar.subheader("Global Actions")

if st.sidebar.button("Save All to Files"):
    chart_a.save_to_file("chart_a.json")
    chart_b.save_to_file("chart_b.json")
    chart_c.save_to_file("chart_c.json")
    st.sidebar.success("Saved all charts!")

if st.sidebar.button("Load All from Files"):
    chart_a.load_from_file("chart_a.json")
    chart_b.load_from_file("chart_b.json")
    chart_c.load_from_file("chart_c.json")
    st.sidebar.success("Loaded all charts!")
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
**Object-Oriented Advantages:**
- State encapsulated in `ChartEditor` object
- Works correctly with tabs (no state loss on tab switch)
- Methods for data manipulation: `add_line()`, `clear()`, `reset()`
- Built-in persistence: `save_to_file()`, `load_from_file()`
- Version tracking for change detection
""")
