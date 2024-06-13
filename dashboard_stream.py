import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# Configurar Streamlit
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# Título
st.title("Financial Dashboard")

# Leer datos desde archivos locales
prop_file = 'prop.csv'
tt_file = 'trades.csv'
metrics_file = 'metrics.csv'

# Leer los datos
try:
    prop_ = pd.read_csv(prop_file, index_col=0, parse_dates=True)
    tt = pd.read_csv(tt_file, index_col=0)
    metrics = pd.read_csv(metrics_file, index_col=0)
except Exception as e:
    st.error(f"Error loading data: {e}")

# Crear gráfica de Plotly
fig = go.Figure()
fig.update_layout(
    width=1500,
    height=800,
    title='How is the Strategy Doing',
    template='plotly_dark',
    xaxis=dict(
        title='Date',
        showgrid=False,
        linecolor='white',
        linewidth=1,
        domain=[0.05, 0.8],
        hoverformat='%Y-%m-%d',
        range=[prop_.index[0], prop_.index[-1] + pd.Timedelta(days=36)]
    ),
    yaxis=dict(
        title='Price',
        side='left',
        position=0.0,
        showgrid=False,
        gridcolor='rgba(255, 255, 255, 0)',
        zeroline=False,
        titlefont=dict(color='rgba(227, 202, 134,1)'),
        tickfont=dict(color='rgba(227, 202, 134,1)'),
        tickformat='$,.0f',
        range=[1000, prop_['gold'].max() * 1.2],
        dtick=100,
        separatethousands=True
    ),
    yaxis2=dict(
        title='Position Sizing - Ounces',
        overlaying='y1',
        side='right',
        position=0.8,
        zeroline=False,
        range=[0, 15000],
        dtick=1000,
        tickformat=',.1f',
        visible=True
    ),
    yaxis3=dict(
        title='Cumulated Position',
        overlaying='y1',
        side='right',
        position=0.9,
        hoverformat=',.0%',
        range=[-0.4, 1],
        dtick=0.1,
        showgrid=False,
        tickangle=-45,
        zeroline=True,
        tickformat=',.0%'
    ),
    hovermode='x',
    legend=dict(x=0.95, y=1, bgcolor='black', traceorder='grouped'),
    margin=dict(l=50, r=50, b=50, t=50, pad=4),
    paper_bgcolor='rgba(0, 0, 0, 1)',
    plot_bgcolor='rgba(0, 0, 0, 1)',
    showlegend=False
)

fig.update_traces(marker_line_color='rgba(0,0,0,0)')
fig.add_trace(go.Scatter(
    x=prop_.index,
    y=prop_['gold'],
    mode='lines+markers',
    line=dict(color='gold', width=1),
    name='gold',
    marker=dict(color='gold', size=4),
    hovertemplate='%{x|%Y-%m-%d}<br>Price: %{y:$,.2f}<br>Asset: gold'
))

fig.add_trace(go.Scatter(
    x=prop_.index,
    y=prop_['gold'] * .99,
    mode='markers',
    marker=dict(color='lightgreen', size=prop_['long_signal_size'] * 10, symbol='triangle-up'),
    name='long',
    text=prop_['long_signal'] * 500,
    hovertemplate='%{x|%Y-%m-%d}<br>Signal: long<br>Value: %{text}',
    hoverinfo='text+name'
))

fig.add_trace(go.Scatter(
    x=prop_.index,
    y=prop_['gold'] * 1.01,
    mode='markers',
    marker=dict(color='red', size=prop_['short_signal_size'] * 10, symbol='triangle-down'),
    name='short',
    text=prop_['short_signal'] * 500,
    hovertemplate='%{x|%Y-%m-%d}<br>Signal: short<br>Value: %{text}',
    hoverinfo='text+name',
    opacity=1
))

fig.add_trace(go.Scatter(
    x=prop_.index,
    y=prop_['str_cum_return'],
    mode='lines',
    line=dict(color='lightblue', width=1),
    name='strategy',
    yaxis='y3',
    hovertemplate='%{x|%Y-%m-%d}<br>Cumulated Return: %{y}'
))

fig.add_trace(go.Scatter(
    x=prop_.index,
    y=prop_['gold_cum_return'],
    mode='lines',
    line=dict(color='gold', width=1),
    name='gold',
    yaxis='y3',
    hovertemplate='%{x|%Y-%m-%d}<br>Cumulated Return: %{y}'
))

fig.add_trace(go.Scatter(
    x=prop_.index,
    y=prop_['oz_exp'],
    mode='lines',
    line=dict(color='lightgreen', width=0.5),
    name='position sizing',
    yaxis='y2',
    fill='tozeroy',
    fillcolor='rgba(0, 255, 0, 0.3)',
    hovertemplate='%{x|%Y-%m-%d}<br>Ounces: %{y}'
))

# Mostrar gráfica en Streamlit
st.plotly_chart(fig, use_container_width=True)

# Mostrar tabla tt
st.subheader("Trade Data")
try:
    st.dataframe(tt.style.format("{:.2f}"))
except Exception as e:
    st.error(f"Error displaying Trade Data: {e}")

# Mostrar tabla metrics
st.subheader("Financial Metrics")
try:
    st.dataframe(metrics)
except Exception as e:
    st.error(f"Error displaying Financial Metrics: {e}")

# Ejecutar Streamlit con `streamlit run app.py`
