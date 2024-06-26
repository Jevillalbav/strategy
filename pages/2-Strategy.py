import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime as dt


st.set_page_config(layout="wide", initial_sidebar_state="expanded")
prop_file =  'data/prop.csv'
tt_file =  'data/trades.csv'
metrics_file = 'data/metrics.csv'
gold_file = 'data/gold_reader.csv'
trade_history = 'data/trade_history.csv'

bear_now_percent = 'data/Bear_Now_percent.csv'
bear_now_price = 'data/Bear_Now_Price.csv'
bull_now_percent = 'data/Bull_Now_percent.csv'
bull_now_price = 'data/Bull_Now_Price.csv'

bear_year_percent = 'data/Bear_Year_percent.csv'
bear_year_price = 'data/Bear_Year_Price.csv'
bull_year_percent = 'data/Bull_Year_percent.csv'
bull_year_price = 'data/Bull_Year_Price.csv'





try:
    prop_ = pd.read_csv(prop_file, index_col=0, parse_dates=True)
    tt = pd.read_csv(tt_file, index_col=0)
    metrics = pd.read_csv(metrics_file, index_col=0)
    gold = pd.read_csv(gold_file, index_col=0, parse_dates=True).loc[ prop_.index[0]:]
    trade_history = pd.read_csv(trade_history)

    bear_now_percent = pd.read_csv(bear_now_percent, index_col=0, parse_dates=True)
    bear_now_price = pd.read_csv(bear_now_price, index_col=0, parse_dates=True)
    bull_now_percent = pd.read_csv(bull_now_percent, index_col=0, parse_dates=True)
    bull_now_price = pd.read_csv(bull_now_price, index_col=0, parse_dates=True)

    bear_year_percent = pd.read_csv(bear_year_percent, index_col=0, parse_dates=True)
    bear_year_price = pd.read_csv(bear_year_price, index_col=0, parse_dates=True)
    bull_year_percent = pd.read_csv(bull_year_percent, index_col=0, parse_dates=True)
    bull_year_price = pd.read_csv(bull_year_price, index_col=0, parse_dates=True)


except Exception as e:
    st.error(f"Error loading data: {e}")



st.title("Strategy Dashboard")

# Valor inicial de la variable de sesión
st.session_state['filter_date'] = ("2021-01-01", "2024-12-31")

# Filtro de fecha
date_range = st.sidebar.slider("Select Strategy Date Range:", 
                min_value=prop_.index.date[0],
                max_value=prop_.index.date[-1], 
                value=(prop_.index.date[0], prop_.index.date[-1]))

st.session_state['filter_date'] = date_range


def crear_chart(start, end):
    # Crear gráfica de Plotly
    fig = go.Figure()
    fig.update_layout(
        width=1500,
        height=800,
        #title='How is the Strategy Doing',
        template='plotly_dark',
        xaxis=dict(
            title='Date',
            showgrid=False,
            linecolor='white',
            linewidth=1,
            domain=[0.05, 0.8],
            hoverformat='%Y-%m-%d',
            range=[start , end + pd.Timedelta(days=36)]),
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
            range=[1200, prop_['gold'].max() * 1.2],
            dtick=100,
            separatethousands=True
        ),
        yaxis2=dict(
            title='Position Sizing - Ounces',
            overlaying='y1',
            side='right',
            position=0.95,
            zeroline=False,
            range=[0, 15000],
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
            range=[-0.4, 1.6],
            dtick=0.2,
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
        #paper_bgcolor= '#06070d',
        #plot_bgcolor= '#06070d',
        showlegend=False
        ## chart layourt rounded corners
        
    )

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
        fillcolor='rgba(0, 255, 0, 0.05)',
        opacity=0.09,
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

fig = crear_chart(date_range[0], date_range[1])
# Mostrar gráfica en Streamlit
st.subheader("Main Chart : Strategy + Return + Current Position")
# Archivo plotly con bordes redondeados
st.plotly_chart(fig, use_container_width=True)


st.subheader(" Montecarlo Simulation")


montecarlo_type = st.sidebar.selectbox("Select Montecarlo Simulation", ["Bull", "Bear" ])
montecarlo_range = st.sidebar.selectbox("For which timeframe ? ", [ "Year", "Now"])
montecarlo_thresholds = st.sidebar.multiselect("Select thresholds", bear_now_price.columns.tolist(), default=['10%', '50%', '90%'])


st.session_state['montecarlo_type'] = montecarlo_type
st.session_state['montecarlo_range'] = montecarlo_range
st.session_state['montecarlo_thresholds'] = montecarlo_thresholds

# st.session_state['montecarlo_type']
# st.session_state['montecarlo_range']
# st.session_state['montecarlo_thresholds']

def crear_montecarlo_chart(montecarlo_type, montecarlo_range, montecarlo_thresholds):
    fig = go.Figure()

    fig.update_layout(
        width=1500,
        height=800,
        #title = 'Montecarlo Simulation',
        template='plotly_dark',
        xaxis=dict(
            title='Date',
            showgrid=False,
            linecolor='white',
            linewidth=1,
            domain=[0.05, 0.9],
            hoverformat='%Y-%m-%d'),
            #range=[bear_year_price.index[0], bear_now_price.index[-1] + pd.Timedelta(days=36)]),
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
            #range=[1500, 3500],
            dtick=100,
            separatethousands=True
        ),
        hovermode='x',showlegend=False  )

    ##3 Current price in White 
    fig.add_trace(go.Scatter( x= prop_.index, y= prop_['gold'], mode='lines', line=dict(color='white', width=2),
        name='Current Price', hoverinfo='y+name'))


    for threshold in montecarlo_thresholds:
        if montecarlo_type == 'Bear' and montecarlo_range == 'Now':
            fig.add_trace(go.Scatter(
                x=bear_now_price.index,
                y=bear_now_price[threshold],
                mode='lines',
                name=threshold,
                text = bear_now_percent[threshold] ,
                hovertemplate='Price: %{y:.2f} <br> Return: %{text:.2%}',
                line=dict(width=1),
            ))

        elif montecarlo_type == 'Bear' and montecarlo_range == 'Year':
            fig.add_trace(go.Scatter
                (x=bear_year_price.index,
                y=bear_year_price[threshold],
                mode='lines',
                name=threshold,
                text = bear_year_percent[threshold] ,
                hovertemplate='Price: %{y:.2f} <br> Return: %{text:.2%}',
                line=dict(width=1),
            ))
        
        elif montecarlo_type == 'Bull' and montecarlo_range == 'Now':
            fig.add_trace(go.Scatter
                (x=bull_now_price.index,
                y=bull_now_price[threshold],
                mode='lines',
                name=threshold,
                text = bull_now_percent[threshold] ,
                hovertemplate='Price: %{y:.2f} <br> Return: %{text:.2%}',
                line=dict(width=1),
            ))

        elif montecarlo_type == 'Bull' and montecarlo_range == 'Year':
            fig.add_trace(go.Scatter
                (x=bull_year_price.index,
                y=bull_year_price[threshold],
                mode='lines',
                name=threshold,
                text = bull_year_percent[threshold] ,
                hovertemplate='Price: %{y:.2f} <br> Return: %{text:.2%}',
                line=dict(width=1),
            ))

    return fig

                
st.plotly_chart(crear_montecarlo_chart(montecarlo_type, montecarlo_range, montecarlo_thresholds), use_container_width=True)

