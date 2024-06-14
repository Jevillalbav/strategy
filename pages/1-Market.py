import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime as dt

def chart_colors_two_axis(left, right, cases):
    siz = 5
    siz = cases.map({0: 0, 1: siz, 2: siz, 3: siz, 4: siz})
    colors = cases.map({0: 'rgba(0,0,0,0)', 1: 'yellow', 2: 'green', 3: 'blue', 4: 'red'})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=left.index, y=left           , mode='lines', 
                            line=dict(color='gray', width=1), opacity=1, hoverinfo='skip', name= left.name))
    fig.add_trace(go.Scatter(x=left.index, y= left, mode='markers',
                            marker=dict(color= colors, size=siz, line = dict(width=0)), name=left.name))
    fig.add_trace(go.Scatter(x=right.index, y= right, mode='lines', name=right.name,
                                line = dict(color='pink', width=0.4) , yaxis='y2', opacity=0.7))
    fig.update_layout(
    xaxis_title='Date',
    yaxis_title= left.name,
    yaxis_tickformat = ',.0f',
    yaxis2 = dict(overlaying='y', side='right', showgrid=False, tickformat = ',.2f', title=right.name, zeroline=False),
    width = 1200, height = 800, template='plotly_dark',  hovermode='x', showlegend=False)
    return fig
def chart_colors_one_axis(left, cases):
    siz = 5
    siz = cases.map({0: 0, 1: siz, 2: siz, 3: siz, 4: siz})
    colors = cases.map({0: 'rgba(0,0,0,0)', 1: 'yellow', 2: 'green', 3: 'blue', 4: 'red'})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=left.index, y=left           , mode='lines', 
                            line=dict(color='gray', width=1), opacity=1, hoverinfo='skip', name= left.name))
    fig.add_trace(go.Scatter(x=left.index, y= left, mode='markers',
                            marker=dict(color= colors, size=siz, line = dict(width=0)), name=left.name))
    fig.update_layout(
    xaxis_title='Date',
    yaxis_title= left.name,
    yaxis_tickformat = ',.0f',
    width = 1200, height = 800, template='plotly_dark',  hovermode='x', showlegend=False)
    return fig
def chart_colors_two_axis_no_markers(left, right):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=left.index, y=left           , mode='lines', 
                            line=dict(color='white', width=1), opacity=1, hoverinfo='skip', name= left.name))
    fig.add_trace(go.Scatter(x=right.index, y= right, mode='lines', name=right.name,
                                line = dict(color='pink', width=0.4) , yaxis='y2', opacity=0.9))
    fig.update_layout(
    xaxis_title='Date',
    yaxis_title= left.name,
    yaxis_tickformat = ',.0f',
    yaxis2 = dict(overlaying='y', side='right', showgrid=False, tickformat = ',.2f', title=right.name, zeroline=False),
    width = 1200, height = 800, template='plotly_dark',  hovermode='x', showlegend=False)
    return fig
def chart_colors_one_axis_no_markers(left):

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=left.index, y=left           , mode='lines', 
                            line=dict(color='gray', width=1), opacity=1, hoverinfo='skip', name= left.name))
    fig.update_layout(
    xaxis_title='Date',
    yaxis_title= left.name,
    yaxis_tickformat = ',.0f',
    width = 1200, height = 800, template='plotly_dark',  hovermode='x', showlegend=False)
    return fig

st.title('Market Data')
st.markdown('---')

st.subheader(' Demand and Supply signals ')

gold_file = 'data/gold_reader.csv'
china_file = 'data/gold_reader.csv'
india_file = 'data/gold_reader.csv'
turkey_file = 'data/gold_reader.csv'

gold = pd.read_csv(gold_file, index_col=0 , parse_dates=True)
china = pd.read_csv(china_file, index_col=0 , parse_dates=True)
india = pd.read_csv(india_file, index_col=0 , parse_dates=True)
turkey = pd.read_csv(turkey_file, index_col=0 , parse_dates=True)


last_world = gold.index.date[-1]
market_state_last = gold['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
market_state_current = gold['market_cases'].map({0: ' No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
last_price = gold['price'].iloc[-1]

st.write(f" Up to {last_world} world gold has been on a {market_state_current} state. The last update per market state was {market_state_last}. Current price is {last_price} USD/oz. ")
# Crear gráfica de Plotly
fig = chart_colors_two_axis( gold['ma_price'], gold['ma_volume'], gold['market_cases'])
fig.add_trace(go.Scatter(x=gold.index, y=gold['price'], mode='lines', name='London FIX', line=dict(color='white', width=1), opacity=0.2))
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')
st.subheader(' Gold Price vs Volume Cross Correlation')
st.markdown('Cross correlation is currently at: {gold["corr"].iloc[-1]:.2f}')

fig = chart_colors_two_axis_no_markers( gold['ma_price'], gold['corr'])
fig.add_trace(go.Scatter(x=gold.index, y=gold['price'], mode='lines', name='London FIX', line=dict(color='white', width=1), opacity=0.2))

st.plotly_chart(fig, use_container_width=True)
