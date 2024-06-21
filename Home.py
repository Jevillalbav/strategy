import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime as dt
import numpy as np


# Configurar Streamlit
st.set_page_config(page_title="Gold Strategy", page_icon=":moneybag:", layout="wide")


# Tittle
st.title("Gold Strategy - Sunvalley Investments")

st.markdown("Based on market states theory,  SV's trading desk looks to identify attractive trades to purchase gold")

st.subheader("- Summary of the strategy:")

st.markdown("1. **Market - How is it doing currently ? :** Here you'll find current price (up to yesterday), financial metrics, market phases and premium discounts from China, India, and Turkey.")
st.markdown("2. **Strategy - What are we looking for ? :** Here you'll find the strategy's signals, the current position, current performance and a montecarlo model to calculate downside risk and upside potential.")  
st.markdown("3. **Backtest - How did we do in the past ? :** Here you'll find backtest results, performance metrics and trades history.")

st.subheader("- Instructions:")
st.markdown("In the sidebar, you'll be able to navigate between pages")









