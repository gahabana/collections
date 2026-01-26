"""
Demo: Options Strategy Analyzer (Prototype)

Simulates the user's options trading use case with:
- Main P/L chart (read-only, calculated)
- IV curve input (editable)
- Risk-free rate input (editable)
- Stock price prediction input (editable)

All charts share the same X-axis (days) and support zoom.
"""

import streamlit as st
import math
from chart_editor import get_chart

st.set_page_config(page_title="Options Analyzer", layout="wide")

# ============================================
# CONFIGURATION
# ============================================
DAYS = 180  # 6 months
X_RANGE = (0, DAYS)

# ============================================
# INITIALIZE CHARTS (OOP approach - handles state automatically)
# ============================================

# Main P/L chart (read-only)
pl_chart = get_chart(
    "main_pl",
    x_range=X_RANGE,
    y_range=(-500, 500),
    colors=["#2ecc71"],
    title="Long Call P/L",
    x_label="Days",
    y_label="P/L ($)",
    width=1000,
    height=350,
    zoom_enabled=True,
    read_only=True,
    initial_lines=[[]]  # Will be calculated
)

# IV Curve input
iv_chart = get_chart(
    "iv_curve",
    x_range=X_RANGE,
    y_range=(10, 60),
    colors=["#e74c3c"],
    title="IV Curve",
    x_label="Days",
    y_label="IV %",
    width=400,
    height=280,
    zoom_enabled=True,
    read_only=False,
    initial_lines=[[(0, 30), (30, 32), (60, 28), (90, 27), (120, 26), (150, 25), (180, 25)]]
)

# Rate Curve input
rate_chart = get_chart(
    "rate_curve",
    x_range=X_RANGE,
    y_range=(0, 10),
    colors=["#3498db"],
    title="Rate Curve",
    x_label="Days",
    y_label="Rate %",
    width=400,
    height=280,
    zoom_enabled=True,
    read_only=False,
    initial_lines=[[(0, 5.0), (90, 5.0), (180, 5.0)]]
)

# Price Prediction input
price_chart = get_chart(
    "price_curve",
    x_range=X_RANGE,
    y_range=(80, 140),
    colors=["#9b59b6"],
    title="Price Path",
    x_label="Days",
    y_label="Price $",
    width=400,
    height=280,
    zoom_enabled=True,
    read_only=False,
    initial_lines=[[(0, 100), (30, 102), (60, 105), (90, 108), (120, 110), (150, 112), (180, 115)]]
)


def calculate_pl_curve(iv_lines, rate_lines, price_lines):
    """
    Simplified P/L calculation for demo purposes.
    In real app, this would use Black-Scholes or similar pricing model.
    """
    pl_points = []

    # Get price at each day (interpolate if needed)
    price_map = {int(p[0]): p[1] for p in price_lines[0]} if price_lines and price_lines[0] else {}
    iv_map = {int(p[0]): p[1] for p in iv_lines[0]} if iv_lines and iv_lines[0] else {}

    base_price = price_map.get(0, 100)
    strike = base_price  # ATM option
    initial_value = None

    for day in range(0, DAYS + 1, 5):
        # Simple approximation: P/L based on price movement and IV
        current_price = price_map.get(day, base_price)
        current_iv = iv_map.get(day, 30) / 100

        # Simulated long call P/L
        intrinsic = max(0, current_price - strike)
        time_value = current_iv * math.sqrt((DAYS - day) / 365) * current_price * 0.4
        option_value = intrinsic + time_value

        # P/L relative to initial value
        if initial_value is None:
            initial_value = option_value

        pl = (option_value - initial_value) * 100  # Scale for visibility
        pl_points.append((day, pl))

    return [pl_points]


# ============================================
# HEADER
# ============================================
st.title("📈 Options Strategy Analyzer (v2.0 Prototype)")
st.caption("Edit input curves, see calculated P/L. All charts support zoom and pan.")

# ============================================
# ZOOM SYNC CONTROLS
# ============================================
col_sync1, col_sync2, col_sync3 = st.columns([2, 2, 4])

with col_sync1:
    if st.button("🔗 Sync X-Axis Zoom", help="Apply current X range to all charts"):
        st.toast("Zoom synced across all charts!")

with col_sync2:
    if st.button("↺ Reset All Zoom"):
        st.toast("Zoom reset to default")

with col_sync3:
    st.caption(f"X range: {X_RANGE[0]} - {X_RANGE[1]} days")

st.markdown("---")

# ============================================
# MAIN P/L CHART (Read-only, calculated)
# ============================================
st.subheader("📊 Strategy P/L (Calculated)")

# Calculate P/L from inputs
pl_curve = calculate_pl_curve(
    iv_chart.lines,
    rate_chart.lines,
    price_chart.lines
)

# Update P/L chart with calculated data
pl_chart._state["lines"] = pl_curve
pl_chart.render()

st.caption("🔍 Drag to pan, scroll to zoom. This chart is calculated from inputs below.")

st.markdown("---")

# ============================================
# INPUT CHARTS (Editable)
# ============================================
st.subheader("📝 Input Variables (Editable)")

input_col1, input_col2, input_col3 = st.columns(3)

# IV Curve
with input_col1:
    st.markdown("**Implied Volatility (%)**")
    iv_chart.render()
    st.caption("Ctrl+drag to pan")

# Risk-Free Rate
with input_col2:
    st.markdown("**Risk-Free Rate (%)**")
    rate_chart.render()
    st.caption("Ctrl+drag to pan")

# Stock Price Prediction
with input_col3:
    st.markdown("**Stock Price Prediction ($)**")
    price_chart.render()
    st.caption("Ctrl+drag to pan")

st.markdown("---")

# ============================================
# DATA SUMMARY
# ============================================
st.subheader("📋 Data Summary")

sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)

with sum_col1:
    st.metric("IV Points", iv_chart.total_points)

with sum_col2:
    st.metric("Rate Points", rate_chart.total_points)

with sum_col3:
    st.metric("Price Points", price_chart.total_points)

with sum_col4:
    st.metric("P/L Points", pl_chart.total_points)

# ============================================
# INSTRUCTIONS
# ============================================
with st.expander("ℹ️ Instructions"):
    st.markdown("""
    ### How to Use

    1. **Main P/L Chart (top)**
       - Shows calculated profit/loss based on your inputs
       - Read-only: drag to pan, scroll to zoom

    2. **Input Charts (bottom row)**
       - Click to add points
       - Click existing point to remove
       - Drag points to move
       - Scroll to zoom
       - Ctrl+drag to pan (normal drag edits points)

    3. **Zoom Sync**
       - Use "Sync X-Axis Zoom" to apply same time range to all charts
       - Use "Reset All Zoom" to return to full range

    ### Notes
    - This is a prototype with simplified P/L calculation
    - Real implementation would use Black-Scholes pricing
    - Strategy legs, underlying selection, and scenarios not yet implemented
    """)
