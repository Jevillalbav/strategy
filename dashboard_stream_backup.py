import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# Configurar Streamlit
st.set_page_config(page_title="Gold Strategy", page_icon=":moneybag:", layout="wide", initial_sidebar_state="expanded")

# Título
st.title("Gold Strategy Dashboard")

# Leer datos desde archivos locales
prop_file =  'prop.csv'
tt_file =  'trades.csv'
metrics_file = 'metrics.csv'


# Leer los datos
try:
    prop_ = pd.read_csv(prop_file, index_col=0, parse_dates=True)
    tt = pd.read_csv(tt_file, index_col=0)
    metrics = pd.read_csv(metrics_file, index_col=0)


except Exception as e:
    st.error(f"Error loading data: {e}")

def crear_chart():
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
            range=[500, prop_['gold'].max() * 1.2],
            dtick=100,
            separatethousands=True
        ),
        yaxis2=dict(
            title='Position Sizing - Ounces',
            overlaying='y1',
            side='right',
            position=0.95,
            zeroline=False,
            range=[0, 20000],
            dtick=1000,
            tickformat=',.1f',
            visible=True,
            showgrid=False,
            titlefont=dict(color='lightgreen'),
            tickfont=dict(color='lightgreen')
        ),
        yaxis3=dict(
            title='Cumulated Position',
            overlaying='y1',
            side='right',
            position=0.85,
            hoverformat=',.0%',
            range=[-0.4, 1],
            dtick=0.1,
            showgrid=False,
            tickangle=-45,
            zeroline=False,
            tickformat=',.0%',
            titlefont=dict(color='lightblue'),
            tickfont=dict(color='lightblue')
        ),
        hovermode='x',
        legend=dict(x=0.95, y=1, bgcolor='black', traceorder='grouped'),
        margin=dict(l=50, r=50, b=50, t=50, pad=4),
        paper_bgcolor='rgba(0, 0, 0, 1)',
        plot_bgcolor='rgba(0, 0, 0, 1)',
        showlegend=False
    )

    #fig.update_traces(marker_line_color='rgba(0,0,0,0)')

    fig.add_trace(go.Scatter(
        x=prop_.index,
        y=prop_['gold'],
        mode='lines+markers',
        line=dict(color='gold', width=1),
        name='Gold',
        marker=dict(color='gold', size=4),
        text= 'Gold Price',
        hoverinfo='y+name'
    ))
    fig.add_trace(go.Scatter(
        x=prop_.index,
        y=prop_['gold'] * .99,
        mode='markers',
        marker=dict(color='lightgreen', size=prop_['long_signal_size'] * 10, symbol='triangle-up'),
        name='Long ↗',
        text=prop_['long_signal'] * 500,
        hoverinfo='text+name'
    ))
    fig.add_trace(go.Scatter(
        x=prop_.index,
        y=prop_['gold'] * 1.01,
        mode='markers',
        marker=dict(color='red', size=prop_['short_signal_size'] * 10, symbol='triangle-down'),
        name='Short ↘',
        text=prop_['short_signal'] * 500,
        hoverinfo='text+name',
        opacity=1
    ))
    fig.add_trace(go.Scatter(
        x=prop_.index,
        y=prop_['str_cum_return'],
        mode='lines',
        line=dict(color='lightblue', width=1, dash='dot'), 
        name='Strategy %',
        yaxis='y3',
        hoverinfo='y+name'
    ))
    fig.add_trace(go.Scatter(
        x=prop_.index,
        y=prop_['gold_cum_return'],
        mode='lines',
        line=dict(color='gold', width=1, dash='dot'),
        name='Gold Ret%',
        yaxis='y3',
        hoverinfo='y+name'
    ))
    fig.add_trace(go.Scatter(
        x=prop_.index,
        y=prop_['oz_exp'],
        mode='lines',
        line=dict(color='lightgreen', width=0.5),
        name='Open Size',
        yaxis='y2',
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.3)',
        opacity=0.5,
        hoverinfo='y+name'
    ))
    fig.add_trace(go.Scatter(
        x = prop_.index,
        y = (prop_['oz_exp'] * 0) - 100 , 
        mode='lines',
        line=dict(color='white', width=0),
        name='',
        yaxis='y2',
        hoverinfo='name+x'))
    return fig

fig = crear_chart()
# Mostrar gráfica en Streamlit
st.subheader("Main Chart : Strategy + Return + Current Position")
st.plotly_chart(fig, use_container_width=True)

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

