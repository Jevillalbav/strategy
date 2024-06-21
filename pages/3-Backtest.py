import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime as dt



# Leer datos desde archivos locales
prop_file =  'data/prop.csv'
tt_file =  'data/trades.csv'
metrics_file = 'data/metrics.csv'
gold_file = 'data/gold_reader.csv'
china_file = 'data/china_reader.csv'
india_file = 'data/india_reader.csv'
turkey_file = 'data/turkey_reader.csv'
trade_history = 'data/trade_history.csv'

# ##############################################################################################################################################
# Leer los datos
try:
    prop_ = pd.read_csv(prop_file, index_col=0, parse_dates=True)
    tt = pd.read_csv(tt_file, index_col=0)
    metrics = pd.read_csv(metrics_file, index_col=0)
    gold = pd.read_csv(gold_file, index_col=0, parse_dates=True).loc[ prop_.index[0]:]
    china = pd.read_csv(china_file, index_col=0, parse_dates=True).loc[ prop_.index[0]:]
    india = pd.read_csv(india_file, index_col=0, parse_dates=True).loc[ prop_.index[0]:]
    turkey = pd.read_csv(turkey_file, index_col=0, parse_dates=True).loc[ prop_.index[0]:]
    trade_history = pd.read_csv(trade_history)

except Exception as e:
    st.error(f"Error loading data: {e}")




# Mostrar tabla tt
st.subheader("Trades Overview since: " + str(prop_.index[0].date()))
try:
    st.dataframe(tt.iloc[:4])
except Exception as e:
    st.error(f"Error displaying Trade Data: {e}")

# Mostrar tabla metrics
st.subheader("Financial Metrics")
try:
    st.dataframe(metrics)
except Exception as e:
    st.error(f"Error displaying Financial Metrics: {e}")