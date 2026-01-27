"""
Demo: Options Strategy Analyzer (Prototype)

Simulates the user's options trading use case with:
- Main P/L chart (read-only, calculated)
- IV curve input (editable)
- Risk-free rate input (editable)
- Stock price prediction input (editable)

All charts have X-axis range selectors for synchronized zoom.
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
# INITIALIZE CHARTS (OOP approach)
# ============================================

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
    zoom_enabled=True,  # Enable range selector
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
    initial_lines=[[]]
)


def calculate_pl_curve(iv_lines, rate_lines, price_lines):
    """
    Simplified P/L calculation for demo purposes.
    In real app, this would use Black-Scholes or similar pricing model.
    """
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
st.caption("Edit input curves to see calculated P/L. Use the range selector below each chart to zoom.")

st.markdown("---")

# ============================================
# MAIN P/L CHART (Read-only, calculated)
# ============================================
st.subheader("Strategy P/L (Calculated)")

# Calculate P/L from inputs
pl_curve = calculate_pl_curve(
    iv_chart.lines,
    rate_chart.lines,
    price_chart.lines
)

# Update P/L chart with calculated data
pl_chart._state["lines"] = pl_curve
pl_chart.render()

st.caption("Drag the range selector handles below to zoom. Double-click to reset.")

st.markdown("---")

# ============================================
# INPUT CHARTS (Editable)
# ============================================
st.subheader("Input Variables (Editable)")

input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    st.markdown("**Implied Volatility (%)**")
    iv_chart.render()

with input_col2:
    st.markdown("**Risk-Free Rate (%)**")
    rate_chart.render()

with input_col3:
    st.markdown("**Stock Price Prediction ($)**")
    price_chart.render()

st.markdown("---")

# ============================================
# DATA SUMMARY
# ============================================
st.subheader("Data Summary")

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
with st.expander("Instructions"):
    st.markdown("""
    ### Range Selector (Zoom)

    Each chart has a range selector bar below it:
    - **Drag the shaded area** to pan left/right
    - **Drag the left/right handles** to zoom in/out
    - **Double-click** the range selector to reset zoom

    ### Editing Points

    - **Click** on chart to add a point
    - **Click** on existing point to remove it
    - **Drag** a point to move it
    - **Ctrl+drag** on chart to pan (when zoomed)
    - Click **Save** to apply changes

    ### Notes
    - This is a prototype with simplified P/L calculation
    - Real implementation would use Black-Scholes pricing
    """)
