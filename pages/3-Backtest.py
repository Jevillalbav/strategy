import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime as dt

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Leer datos desde archivos locales
prop_file =  'data/prop.csv'
tt_file =  'data/trades.csv'
metrics_file = 'data/metrics.csv'
gold_file = 'data/gold_reader.csv'
china_file = 'data/china_reader.csv'
india_file = 'data/india_reader.csv'
turkey_file = 'data/turkey_reader.csv'
trade_history = 'data/trade_history.csv'
b_b = 'data/b_b.csv'

# ##############################################################################################################################################
# Leer los datos
try:
    prop_ = pd.read_csv(prop_file, index_col=0, parse_dates=True)
    tt = pd.read_csv(tt_file, index_col=0)
    metrics = pd.read_csv(metrics_file, index_col=0)
    trade_history = pd.read_csv(trade_history)
    b_b = pd.read_csv(b_b, index_col=0)
    b_b.index.name = "Year"
    b_c = b_b.copy()
    b_c.columns = [(i.split('_')[0] , i.split('_')[1]) for i in b_c.columns]
    b_c.columns = pd.MultiIndex.from_tuples(b_c.columns)
    b_c = b_c.swaplevel(axis=1)
    b_c = b_c.sort_index(axis=1)[['Trades', 'Alpha', 'Beta', 'InfoRatio', 'Return','Volatility' ,'Sharpe', 'Sortino', 'Drawdown', 'Var', 'CVar']]
    b_c['Trades'] = (b_c['Trades'].astype(int))
    b_c['Alpha' , 'Strategy'] = b_c['Alpha' , 'Strategy'].apply(lambda x: f"{x:.0%}")
    b_c['Beta' , 'Strategy'] = b_c['Beta' , 'Strategy'].apply(lambda x: f"{x:.0%}")
    b_c['InfoRatio' , 'Strategy'] = b_c['InfoRatio' , 'Strategy'].apply(lambda x: f"{x:.0%}")
    b_c['Return' , 'Strategy'] = b_c['Return' , 'Strategy'].apply(lambda x: f"{x:.0%}")
    b_c['Return' , 'Gold'] = b_c['Return' , 'Gold'].apply(lambda x: f"{x:.0%}")
    b_c['Sharpe' , 'Strategy'] = b_c['Sharpe' , 'Strategy'].apply(lambda x: f"{x:.2f}")
    b_c['Sharpe' , 'Gold'] = b_c['Sharpe' , 'Gold'].apply(lambda x: f"{x:.2f}")
    b_c['Sortino' , 'Strategy'] = b_c['Sortino' , 'Strategy'].apply(lambda x: f"{x:.2f}")
    b_c['Sortino' , 'Gold'] = b_c['Sortino' , 'Gold'].apply(lambda x: f"{x:.2f}")
    b_c['Drawdown' , 'Strategy'] = b_c['Drawdown' , 'Strategy'].apply(lambda x: f"{x:.0%}")
    b_c['Drawdown', 'Gold'] = b_c['Drawdown', 'Gold'].apply(lambda x: f"{x:.0%}")
    b_c['Volatility' , 'Strategy'] = b_c['Volatility' , 'Strategy'].apply(lambda x: f"{x:.0%}")
    b_c['Volatility' , 'Gold'] = b_c['Volatility' , 'Gold'].apply(lambda x: f"{x:.0%}")
    b_c['Var' , 'Strategy'] = b_c['Var' , 'Strategy'].apply(lambda x: f"{x:.1%}")
    b_c['Var' , 'Gold'] = b_c['Var' , 'Gold'].apply(lambda x: f"{x:.1%}")
    b_c['CVar' , 'Strategy'] = b_c['CVar' , 'Strategy'].apply(lambda x: f"{x:.1%}")
    b_c['CVar' , 'Gold'] = b_c['CVar' , 'Gold'].apply(lambda x: f"{x:.1%}")

except Exception as e:
    st.error(f"Error loading data: {e}")

# ##############################################################################################################################################
# Mostrar tabla tt
st.subheader("Trades Overview since: " + str(prop_.index[0].date()))
st.dataframe(tt.iloc[:4])

# Mostrar tabla metrics
st.subheader("Financial Metrics")
st.dataframe(metrics)

# ##############################################################################################################################################

# Mostrar tabla b_b
st.subheader("Yearly Backtest")
st.table(b_c)