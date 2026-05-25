import streamlit as st
import pandas as pd
import numpy as np

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="PitWall Quant",
    page_icon="🏎️",
    layout="wide"
)

# ---- KELLY FUNCTION ----
def kelly_criterion(odds, model_prob):
    b = odds - 1
    p = model_prob
    q = 1 - p
    f = (b * p - q) / b
    return max(f, 0)

# ---- HEADER ----
st.title("🏎️ PitWall Quant")
st.markdown("**Quantitative F1 Analytics — Where Telemetry Meets Hedge Fund Logic swagg projecttt !!!!!!**")
st.divider()

# ---- DATA ----
signals = {
    'Red Bull Racing':  {'odds': 1.25,   'model_prob': 0.407, 'signal': 'SELL'},
    'Ferrari':          {'odds': 5.00,   'model_prob': 0.227, 'signal': 'BUY'},
    'Mercedes':         {'odds': 8.00,   'model_prob': 0.115, 'signal': 'HOLD'},
    'Aston Martin':     {'odds': 15.00,  'model_prob': 0.116, 'signal': 'BUY'},
    'McLaren':          {'odds': 20.00,  'model_prob': 0.014, 'signal': 'SELL'},
    'Alpine':           {'odds': 50.00,  'model_prob': 0.037, 'signal': 'HOLD'},
    'Haas F1 Team':     {'odds': 100.00, 'model_prob': 0.045, 'signal': 'BUY'},
    'AlphaTauri':       {'odds': 100.00, 'model_prob': 0.014, 'signal': 'HOLD'},
    'Alfa Romeo':       {'odds': 100.00, 'model_prob': 0.013, 'signal': 'HOLD'},
    'Williams':         {'odds': 200.00, 'model_prob': 0.012, 'signal': 'HOLD'},
}

bankroll = 1000

# ---- BUILD TABLE ----
rows = []
for team, data in signals.items():
    kelly = kelly_criterion(data['odds'], data['model_prob'])
    bet = round(bankroll * kelly, 2)
    rows.append({
        'Team': team,
        'Market Odds': data['odds'],
        'Market Prob': f"{1/data['odds']:.1%}",
        'Model Prob': f"{data['model_prob']:.1%}",
        'Kelly %': f"{kelly:.1%}",
        'Bet ($1000)': f"${bet}",
        'Signal': data['signal']
    })

df = pd.DataFrame(rows)

# ---- SIGNAL COLORS ----
def color_signal(val):
    if val == 'BUY':
        return 'background-color: #1a472a; color: #2ecc71'
    elif val == 'SELL':
        return 'background-color: #4a0000; color: #e74c3c'
    else:
        return 'background-color: #2d2d2d; color: #f39c12'

# ---- METRICS ROW ----
col1, col2, col3 = st.columns(3)
col1.metric("Race Weekend", "Bahrain GP 2023")
col2.metric("Simulated Bankroll", "$1,000")
col3.metric("BUY Signals", sum(1 for v in signals.values() if v['signal'] == 'BUY'))

st.divider()

# ---- TABLE ----
st.subheader("Trading Signals")
st.dataframe(
    df.style.applymap(color_signal, subset=['Signal']),
    use_container_width=True,
    hide_index=True
)

# ---- PACE CHART ----
st.divider()
st.subheader("Model Probability vs Market Probability")

chart_data = pd.DataFrame({
    'Team': list(signals.keys()),
    'Market': [1/v['odds'] for v in signals.values()],
    'Model': [v['model_prob'] for v in signals.values()]
}).set_index('Team')

st.bar_chart(chart_data)