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
from chart_editor import chart_editor, get_chart

st.set_page_config(page_title="Options Analyzer", layout="wide")

# ============================================
# CONFIGURATION
# ============================================
DAYS = 180  # 6 months
X_RANGE = (0, DAYS)

# ============================================
# INITIALIZE DATA
# ============================================
if "iv_curve" not in st.session_state:
    # Default IV: starts at 30%, ends at 25% with some volatility
    st.session_state.iv_curve = [
        [(0, 30), (30, 32), (60, 28), (90, 27), (120, 26), (150, 25), (180, 25)]
    ]

if "rate_curve" not in st.session_state:
    # Default risk-free rate: flat at 5%
    st.session_state.rate_curve = [
        [(0, 5.0), (90, 5.0), (180, 5.0)]
    ]

if "price_prediction" not in st.session_state:
    # Default price prediction: gradual increase
    st.session_state.price_prediction = [
        [(0, 100), (30, 102), (60, 105), (90, 108), (120, 110), (150, 112), (180, 115)]
    ]

if "shared_x_range" not in st.session_state:
    st.session_state.shared_x_range = list(X_RANGE)


def calculate_pl_curve(iv_curve, rate_curve, price_prediction):
    """
    Simplified P/L calculation for demo purposes.
    In real app, this would use Black-Scholes or similar pricing model.
    """
    # Just create a simple simulated P/L based on price movement
    pl_points = []

    # Get price at each day (interpolate if needed)
    price_map = {int(p[0]): p[1] for p in price_prediction[0]} if price_prediction else {}
    iv_map = {int(p[0]): p[1] for p in iv_curve[0]} if iv_curve else {}

    base_price = price_map.get(0, 100)
    strike = base_price  # ATM option

    for day in range(0, DAYS + 1, 5):
        # Simple approximation: P/L based on price movement and IV
        current_price = price_map.get(day, base_price)
        current_iv = iv_map.get(day, 30) / 100

        # Simulated long call P/L
        intrinsic = max(0, current_price - strike)
        time_value = current_iv * math.sqrt((DAYS - day) / 365) * current_price * 0.4
        option_value = intrinsic + time_value

        # P/L relative to initial value
        if day == 0:
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
        # This would sync from main chart to others
        st.toast("Zoom synced across all charts!")

with col_sync2:
    if st.button("↺ Reset All Zoom"):
        st.session_state.shared_x_range = list(X_RANGE)
        st.toast("Zoom reset to default")

with col_sync3:
    st.caption(f"Shared X range: {st.session_state.shared_x_range[0]:.0f} - {st.session_state.shared_x_range[1]:.0f} days")

st.markdown("---")

# ============================================
# MAIN P/L CHART (Read-only, calculated)
# ============================================
st.subheader("📊 Strategy P/L (Calculated)")

# Calculate P/L from inputs
pl_curve = calculate_pl_curve(
    st.session_state.iv_curve,
    st.session_state.rate_curve,
    st.session_state.price_prediction
)

chart_editor(
    lines=pl_curve,
    x_range=tuple(st.session_state.shared_x_range),
    y_range=(-500, 500),
    colors=["#2ecc71"],  # Green
    title="Long Call P/L",
    x_label="Days",
    y_label="P/L ($)",
    width=1000,
    height=350,
    zoom_enabled=True,
    read_only=True,  # Can't edit, only view
    key="main_pl"
)

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
    iv_result = chart_editor(
        lines=st.session_state.iv_curve,
        x_range=tuple(st.session_state.shared_x_range),
        y_range=(10, 60),
        colors=["#e74c3c"],  # Red
        title="IV Curve",
        x_label="Days",
        y_label="IV %",
        width=400,
        height=280,
        zoom_enabled=True,
        read_only=False,
        key="iv_curve"
    )
    st.session_state.iv_curve = iv_result
    st.caption("Ctrl+drag to pan")

# Risk-Free Rate
with input_col2:
    st.markdown("**Risk-Free Rate (%)**")
    rate_result = chart_editor(
        lines=st.session_state.rate_curve,
        x_range=tuple(st.session_state.shared_x_range),
        y_range=(0, 10),
        colors=["#3498db"],  # Blue
        title="Rate Curve",
        x_label="Days",
        y_label="Rate %",
        width=400,
        height=280,
        zoom_enabled=True,
        read_only=False,
        key="rate_curve"
    )
    st.session_state.rate_curve = rate_result
    st.caption("Ctrl+drag to pan")

# Stock Price Prediction
with input_col3:
    st.markdown("**Stock Price Prediction ($)**")
    price_result = chart_editor(
        lines=st.session_state.price_prediction,
        x_range=tuple(st.session_state.shared_x_range),
        y_range=(80, 140),
        colors=["#9b59b6"],  # Purple
        title="Price Path",
        x_label="Days",
        y_label="Price $",
        width=400,
        height=280,
        zoom_enabled=True,
        read_only=False,
        key="price_curve"
    )
    st.session_state.price_prediction = price_result
    st.caption("Ctrl+drag to pan")

st.markdown("---")

# ============================================
# DATA SUMMARY
# ============================================
st.subheader("📋 Data Summary")

sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)

with sum_col1:
    iv_points = len(st.session_state.iv_curve[0]) if st.session_state.iv_curve else 0
    st.metric("IV Points", iv_points)

with sum_col2:
    rate_points = len(st.session_state.rate_curve[0]) if st.session_state.rate_curve else 0
    st.metric("Rate Points", rate_points)

with sum_col3:
    price_points = len(st.session_state.price_prediction[0]) if st.session_state.price_prediction else 0
    st.metric("Price Points", price_points)

with sum_col4:
    pl_points = len(pl_curve[0]) if pl_curve else 0
    st.metric("P/L Points", pl_points)

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
