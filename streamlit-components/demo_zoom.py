"""
Demo: Zoom and Pan functionality

Tests the v2.0 zoom features:
- Mouse wheel zoom (centered on cursor)
- Ctrl+drag pan (or just drag in read_only mode)
- Zoom buttons (+, -, fit, reset)
- Read-only mode for output charts
"""

import streamlit as st
from chart_editor import chart_editor, get_chart

st.set_page_config(page_title="Zoom Demo", layout="wide")
st.title("Chart Editor - Zoom Demo (v2.0)")

# Initialize demo data
if "demo_lines" not in st.session_state:
    # Create some sample data with many points
    import math
    points = []
    for i in range(0, 365, 5):  # One year of data, every 5 days
        # Simulated price with some randomness
        base = 100 + 20 * math.sin(i / 30) + 0.05 * i
        points.append((i, base))
    st.session_state.demo_lines = [points]

st.markdown("---")

# Two columns: Editable chart and Read-only chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("Editable Chart + Zoom")
    st.caption("Edit points AND zoom. Use Ctrl+drag to pan.")

    lines = chart_editor(
        lines=st.session_state.demo_lines,
        x_range=(0, 365),
        y_range=(50, 200),
        title="Stock Price Prediction",
        x_label="Days",
        y_label="Price ($)",
        width=600,
        height=400,
        zoom_enabled=True,
        read_only=False,
        key="editable_zoom"
    )
    st.session_state.demo_lines = lines

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

    chart_editor(
        lines=st.session_state.demo_lines,
        x_range=(0, 365),
        y_range=(50, 200),
        title="Stock Price (Read Only)",
        x_label="Days",
        y_label="Price ($)",
        width=600,
        height=400,
        zoom_enabled=True,
        read_only=True,
        key="readonly_zoom"
    )

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

chart_editor(
    lines=[
        [(0, 100), (100, 150), (200, 120), (300, 180)],
        [(0, 80), (100, 90), (200, 110), (300, 100)],
    ],
    x_range=(0, 400),
    y_range=(0, 250),
    title="Multi-Line with Zoom",
    x_label="X Axis",
    y_label="Y Axis",
    width=800,
    height=450,
    zoom_enabled=True,
    read_only=False,
    key="buttons_test"
)

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
