"""
Demo: Options Strategy Analyzer (Prototype)

Simulates the user's options trading use case with:
- Main P/L chart (read-only, calculated) - HAS the range selector
- IV curve input (editable) - follows main chart zoom
- Risk-free rate input (editable) - follows main chart zoom
- Stock price prediction input (editable) - follows main chart zoom

Single master range selector under main chart controls all 4 charts.
"""

import streamlit as st
import math
from chart_editor import chart_editor, get_chart

st.set_page_config(page_title="Options Analyzer", layout="wide")

# ============================================
# CONFIGURATION
# ============================================
DAYS = 180  # 6 months

# ============================================
# SHARED X-AXIS RANGE (controlled by main chart)
# ============================================
if "shared_x_min" not in st.session_state:
    st.session_state.shared_x_min = 0.0
if "shared_x_max" not in st.session_state:
    st.session_state.shared_x_max = float(DAYS)

def get_shared_x_range():
    return (st.session_state.shared_x_min, st.session_state.shared_x_max)

def on_main_chart_zoom(x_range, y_range):
    """Called when main P/L chart is zoomed - updates shared range for all charts."""
    st.session_state.shared_x_min = x_range[0]
    st.session_state.shared_x_max = x_range[1]

# ============================================
# INITIALIZE INPUT CHARTS (OOP approach, no zoom selector)
# ============================================

iv_chart = get_chart(
    "iv_curve",
    x_range=(0, DAYS),  # Full range, will be overridden
    y_range=(10, 60),
    colors=["#e74c3c"],
    title="IV Curve",
    x_label="Days",
    y_label="IV %",
    width=400,
    height=250,
    zoom_enabled=False,  # No range selector - controlled by main
    read_only=False,
    initial_lines=[[(0, 30), (30, 32), (60, 28), (90, 27), (120, 26), (150, 25), (180, 25)]]
)

rate_chart = get_chart(
    "rate_curve",
    x_range=(0, DAYS),
    y_range=(0, 10),
    colors=["#3498db"],
    title="Rate Curve",
    x_label="Days",
    y_label="Rate %",
    width=400,
    height=250,
    zoom_enabled=False,
    read_only=False,
    initial_lines=[[(0, 5.0), (90, 5.0), (180, 5.0)]]
)

price_chart = get_chart(
    "price_curve",
    x_range=(0, DAYS),
    y_range=(80, 140),
    colors=["#9b59b6"],
    title="Price Path",
    x_label="Days",
    y_label="Price $",
    width=400,
    height=250,
    zoom_enabled=False,
    read_only=False,
    initial_lines=[[(0, 100), (30, 102), (60, 105), (90, 108), (120, 110), (150, 112), (180, 115)]]
)


def calculate_pl_curve(iv_lines, rate_lines, price_lines):
    """Simplified P/L calculation for demo purposes."""
    pl_points = []
    price_map = {int(p[0]): p[1] for p in price_lines[0]} if price_lines and price_lines[0] else {}
    iv_map = {int(p[0]): p[1] for p in iv_lines[0]} if iv_lines and iv_lines[0] else {}

    base_price = price_map.get(0, 100)
    strike = base_price
    initial_value = None

    for day in range(0, DAYS + 1, 5):
        current_price = price_map.get(day, base_price)
        current_iv = iv_map.get(day, 30) / 100
        intrinsic = max(0, current_price - strike)
        time_value = current_iv * math.sqrt((DAYS - day) / 365) * current_price * 0.4
        option_value = intrinsic + time_value
        if initial_value is None:
            initial_value = option_value
        pl = (option_value - initial_value) * 100
        pl_points.append((day, pl))

    return [pl_points]


# ============================================
# HEADER
# ============================================
st.title("Options Strategy Analyzer (v2.0)")
st.caption("Use the range selector under the P/L chart to zoom all charts together.")

st.markdown("---")

# ============================================
# MAIN P/L CHART (with range selector)
# ============================================
st.subheader("Strategy P/L (Calculated)")

# Calculate P/L from inputs
pl_curve = calculate_pl_curve(
    iv_chart.lines,
    rate_chart.lines,
    price_chart.lines
)

# Main chart with zoom enabled (has the range selector)
# Use functional API to capture zoom state via on_zoom callback
main_result = chart_editor(
    lines=pl_curve,
    x_range=(0, DAYS),  # Original full range for zoom reference
    y_range=(-500, 500),
    colors=["#2ecc71"],
    title="Long Call P/L",
    x_label="Days",
    y_label="P/L ($)",
    width=1000,
    height=350,
    zoom_enabled=True,  # HAS the range selector
    read_only=True,
    key="main_pl",
    on_zoom=on_main_chart_zoom,  # Sync zoom to other charts
)

st.caption("Drag the range selector handles to zoom. All charts below will follow.")

st.markdown("---")

# ============================================
# INPUT CHARTS (follow main chart's zoom)
# ============================================
st.subheader("Input Variables (Editable)")

# Apply shared zoom range to input charts
shared_range = get_shared_x_range()

input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    st.markdown("**Implied Volatility (%)**")
    iv_chart.x_range = shared_range
    iv_chart.render()

with input_col2:
    st.markdown("**Risk-Free Rate (%)**")
    rate_chart.x_range = shared_range
    rate_chart.render()

with input_col3:
    st.markdown("**Stock Price Prediction ($)**")
    price_chart.x_range = shared_range
    price_chart.render()

st.markdown("---")

# ============================================
# DATA SUMMARY
# ============================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("IV Points", iv_chart.total_points)
with col2:
    st.metric("Rate Points", rate_chart.total_points)
with col3:
    st.metric("Price Points", price_chart.total_points)
with col4:
    st.metric("Zoom", f"{shared_range[0]:.0f}-{shared_range[1]:.0f}d")

with st.expander("Instructions"):
    st.markdown("""
    **Range Selector (under P/L chart):**
    - Drag handles to zoom in/out
    - Drag middle to pan
    - Double-click to reset

    **Input Charts:**
    - Click to add point, click point to remove
    - Drag to move points
    - All follow the main chart's zoom
    """)
