"""
Demo: Zoom and Pan functionality

Tests the v2.0 zoom features:
- Mouse wheel zoom (centered on cursor)
- Ctrl+drag pan (or just drag in read_only mode)
- Zoom buttons (+, -, fit, reset)
- Read-only mode for output charts
"""

import streamlit as st
import math
from chart_editor import get_chart, chart_editor

st.set_page_config(page_title="Zoom Demo", layout="wide")
st.title("Chart Editor - Zoom Demo (v2.0)")

# Initialize demo data using OOP approach
demo_chart = get_chart(
    "demo_main",
    x_range=(0, 365),
    y_range=(50, 200),
    title="Stock Price Prediction",
    x_label="Days",
    y_label="Price ($)",
    width=600,
    height=400,
    zoom_enabled=True,
    read_only=False,
    initial_lines=[[
        (i, 100 + 20 * math.sin(i / 30) + 0.05 * i)
        for i in range(0, 365, 5)
    ]]
)

st.markdown("---")

# Two columns: Editable chart and Read-only chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("Editable Chart + Zoom")
    st.caption("Edit points AND zoom. Use Ctrl+drag to pan.")
    demo_chart.render()

    st.info("""
    **Controls:**
    - 🖱️ **Click** to add point
    - 🖱️ **Click point** to remove
    - 🖱️ **Drag point** to move
    - 🔄 **Mouse wheel** to zoom
    - ⌨️ **Ctrl+drag** to pan
    """)

with col2:
    st.subheader("Read-Only Chart + Zoom")
    st.caption("View only. Drag to pan, wheel to zoom.")

    # Read-only view of the same data
    readonly_chart = get_chart(
        "demo_readonly",
        x_range=(0, 365),
        y_range=(50, 200),
        title="Stock Price (Read Only)",
        x_label="Days",
        y_label="Price ($)",
        width=600,
        height=400,
        zoom_enabled=True,
        read_only=True,
        initial_lines=demo_chart.lines  # Mirror the editable chart's data
    )
    # Update with latest data from editable chart
    readonly_chart._state["lines"] = demo_chart.lines
    readonly_chart.render()

    st.info("""
    **Controls:**
    - 🖱️ **Drag** to pan (no Ctrl needed)
    - 🔄 **Mouse wheel** to zoom
    - ❌ Editing disabled
    """)

st.markdown("---")
st.subheader("Zoom Buttons Test")

# Single chart with zoom controls visible
st.caption("Use the +, -, ⊡ (fit), ↺ (reset) buttons below the chart")

buttons_chart = get_chart(
    "buttons_test",
    x_range=(0, 400),
    y_range=(0, 250),
    title="Multi-Line with Zoom",
    x_label="X Axis",
    y_label="Y Axis",
    width=800,
    height=450,
    zoom_enabled=True,
    read_only=False,
    initial_lines=[
        [(0, 100), (100, 150), (200, 120), (300, 180)],
        [(0, 80), (100, 90), (200, 110), (300, 100)],
    ]
)
buttons_chart.render()

st.markdown("---")
st.markdown("""
### Zoom Features Checklist

| Feature | Status |
|---------|--------|
| Mouse wheel zoom | ✅ |
| Zoom centered on cursor | ✅ |
| Pan with Ctrl+drag | ✅ |
| Pan with drag (read-only) | ✅ |
| Zoom buttons (+/-) | ✅ |
| Fit to data button | ✅ |
| Reset zoom button | ✅ |
| Zoom limits (min/max) | ✅ |
| Read-only mode | ✅ |
""")
