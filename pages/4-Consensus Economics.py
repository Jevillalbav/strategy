import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime as dt

# Load Data
cn = pd.read_csv("data/consensus.csv", index_col=0, parse_dates=True)
gold = pd.read_csv("data/gold_reader.csv", index_col=0, parse_dates=True).loc['2016-01-01':]


st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title("Consensus Economics - Reviews")

st.sidebar.subheader("Report Filters")

st.session_state.year_report, st.session_state.month_report, st.session_state.bank = None, None, None

year_report = st.sidebar.selectbox("Select Report - Year", [2017, 2018, 2019, 2020, 2021 , 2022, 2023, 2024], index= 7
                     ) 
st.session_state.year_report = year_report


month_report = st.sidebar.selectbox("Select Report - Month", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], index= 5
                     )
st.session_state.month_report = month_report

bank = st.sidebar.multiselect("Select Bank", cn['bank'].unique(), default= ['consensus mean', 'high', 'low'])
st.session_state.bank = bank


# st.write("Report Date: ", st.session_state.year_report, st.session_state.month_report, st.session_state.bank)

st.subheader("Report Chart")

# gold


# cn


def chart_consensus(year, report, banks_group):
    fig = go.Figure()
    fig.update_layout(
        width=1600,
        height=900,
        #title='How is the Strategy Doing',
        template='plotly_dark',
        xaxis=dict(
            title='Date',
            showgrid=False,
            linecolor='white',
            linewidth=1,
            domain=[0.05, 0.95],
            hoverformat='%Y-%m-%d'),
        yaxis=dict(
            title='Price',
            showgrid=False,
            linecolor='white',
            linewidth=1,
            ),    
    showlegend=False,hovermode='x',hoverdistance=100, spikedistance=1000)

    fig.add_trace(go.Scatter(x=gold.index, y=gold['price'], mode='lines', name='Gold Price', line=dict(color='gold', width=2)))

    date_gold = gold.loc[ : dt.datetime(year, report, 1) + pd.DateOffset(months=1)].index[-1]
    value_gold = gold.loc[date_gold, 'price']

    try: 
        df = cn.loc[(cn['year_report'] == year) & (cn['month_report'] == report) & (cn['bank'].isin(banks_group))].copy().pivot_table(index='date_forecast', columns='bank', values='value')
        df.index = pd.to_datetime(df.index)
        df.loc[date_gold] = value_gold
        df = df.sort_index()
        df = df.resample('D').last().interpolate(method='pchip')
        for i in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[i], mode='lines', name=i, line=dict(width=1)))
    except:
        pass
    return fig



fig = chart_consensus(year_report, month_report,bank)     
st.plotly_chart(fig)
    
