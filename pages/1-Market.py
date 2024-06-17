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
    yaxis_showgrid=False,
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
    yaxis_showgrid=False,
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
    yaxis_showgrid=False,
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
    yaxis_showgrid=False,
    yaxis_title= left.name,
    yaxis_tickformat = ',.0f',
    width = 1200, height = 800, template='plotly_dark',  hovermode='x', showlegend=False)
    return fig

st.title('Market Data')
st.markdown('---')

st.subheader(' Demand and Supply signals ')

gold_file = 'data/gold_reader.csv'
china_file = 'data/china_reader.csv'
india_file = 'data/india_reader.csv'
turkey_file = 'data/turkey_reader.csv'

gold = pd.read_csv(gold_file, index_col=0 , parse_dates=True)
gold['corr'] = gold['corr'].ewm(span=15).mean()
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
st.markdown(f'Cross correlation is currently at: {gold["corr"].iloc[-1]:.0%}, compared to yesterday\'s {gold["corr"].iloc[-2]:.0%}')

fig = chart_colors_two_axis_no_markers( gold['ma_price'], gold['corr'])
fig.add_trace(go.Scatter(x=gold.index, y=gold['price'], mode='lines', name='London FIX', line=dict(color='white', width=1), opacity=0.2))
fig.add_hline(y=0, line_color='red', yref='y2', line_width=0.5)
st.plotly_chart(fig, use_container_width=True)
st.markdown('---')
##########################
st.subheader(' China Gold Demand and Supply Signals ')
last_china = china.index.date[-1]
market_state_last_china = china['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
market_state_current_china = china['market_cases'].map({0: ' No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
last_pd = china['price'].iloc[-1]
bef_last_pd = china['price'].iloc[-2]
st.write(f" Up to {last_china} China gold has been on a {market_state_current_china} state. The last update per market state was {market_state_last_china}. Current Premium Discount is {last_pd:.2f} USD/oz. compared to yesterday's {bef_last_pd:.2f} USD/oz. ")

fig = chart_colors_two_axis( china['ma_price'], china['ma_volume'], china['market_cases'])
fig.add_trace(go.Scatter(x=china.index, y=china['price'], mode='lines', name='China P/D', line=dict(color='white', width=1), opacity=0.2))
st.plotly_chart(fig, use_container_width=True)
st.markdown('---')
##########################
st.subheader(' India Gold Demand and Supply Signals ')
last_india = india.index.date[-1]
market_state_last_india = india['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
market_state_current_india = india['market_cases'].map({0: ' No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
last_pd_india = india['price'].iloc[-1]
bef_last_pd_india = india['price'].iloc[-2]
st.write(f" Up to {last_india} India gold has been on a {market_state_current_india} state. The last update per market state was {market_state_last_india}. Current Premium Discount is {last_pd_india:.2f} USD/oz. compared to yesterday's {bef_last_pd_india:.2f} USD/oz. ")

fig = chart_colors_two_axis( india['ma_price'], india['ma_volume'], india['market_cases'])
fig.add_trace(go.Scatter(x=india.index, y=india['price'], mode='lines', name='India P/D', line=dict(color='white', width=1), opacity=0.2))
st.plotly_chart(fig, use_container_width=True)
st.markdown('---')
##########################
st.subheader(' Turkey Gold Demand and Supply Signals ')
last_turkey = turkey.index.date[-1]
market_state_last_turkey = turkey['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
market_state_current_turkey = turkey['market_cases'].map({0: ' No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
last_pd_turkey = turkey['price'].iloc[-1]
bef_last_pd_turkey = turkey['price'].iloc[-2]
st.write(f" Up to {last_turkey} Turkey gold has been on a {market_state_current_turkey} state. The last update per market state was {market_state_last_turkey}. Current Premium Discount is {last_pd_turkey:.2f} USD/oz. compared to yesterday's {bef_last_pd_turkey:.2f} USD/oz. ")

fig = chart_colors_two_axis( turkey['ma_price'], turkey['ma_volume'], turkey['market_cases'])
fig.add_trace(go.Scatter(x=turkey.index, y=turkey['price'], mode='lines', name='Turkey P/D', line=dict(color='white', width=1), opacity=0.2))
st.plotly_chart(fig, use_container_width=True)
st.markdown('---')
##########################

