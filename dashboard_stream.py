import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def chart_colors(left, right, cases):
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
    width = 1200, height = 700, template='plotly_dark',  hovermode='x', showlegend=False)
    return fig

##############################################################################################################################################

# Configurar Streamlit
st.set_page_config(page_title="Gold Strategy", page_icon=":moneybag:", layout="wide", initial_sidebar_state="expanded")


with open("styles/corners.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



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
    gold = pd.read_csv(gold_file, index_col=0)
    china = pd.read_csv(china_file, index_col=0)
    india = pd.read_csv(india_file, index_col=0)
    turkey = pd.read_csv(turkey_file, index_col=0)
    trade_history = pd.read_csv(trade_history)


except Exception as e:
    st.error(f"Error loading data: {e}")


# Crear pestañas
tab_home , tab_china , tab_india , tab_turkey   = st.tabs(["Home - Strategy", "China's Market", "India's Market", "Turkey's Market"])

# Tab Home
with tab_home:
    # Título
    st.title("Gold Strategy Dashboard")


    # last_world = gold.index[-1]
    # market_state_last = gold['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
    # market_state_current = gold['market_cases'].map({0: ' No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
    # st.write(f" Up to {last_world} world gold has been on a {market_state_current} state. The last update per market satate was {market_state_last}.")
    # # Crear gráfica de Plotly
    # fig = chart_colors( gold['ma_price'], gold['ma_volume'], gold['market_cases_'])
    # fig.add_trace(go.Scatter(x=gold.index, y=gold['price'], mode='lines', name='London FIX', line=dict(color='white', width=1), opacity=0.2))
    # st.plotly_chart(fig, use_container_width=True)


    def crear_chart():
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
            #paper_bgcolor= '#06070d',
            #plot_bgcolor= '#06070d',
            showlegend=False
            ## chart layourt rounded corners
            
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
    # Archivo plotly con bordes redondeados
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("----")

    # Mostrar tabla tt
    st.subheader("Trades Overview since: " + str(prop_.index[0].date()))
    try:
        st.dataframe(tt.iloc[:4] )
    except Exception as e:
        st.error(f"Error displaying Trade Data: {e}")
    
    st.markdown("----")

    # Mostrar tabla metrics
    st.subheader("Financial Metrics")
    try:
        st.dataframe(metrics)
    except Exception as e:
        st.error(f"Error displaying Financial Metrics: {e}")
    
    st.markdown("----")


with tab_china:
    st.title("China's Market")
    
    last_china = china.index[-1]
    market_state_china = china['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]

    
    st.write(f" China's Market State: {market_state_china} - Last Update: {last_china}")
    # Crear gráfica de Plotly
    #china = china.rename(columns={'ma_price': 'Mov Avg.'})
    fig = chart_colors( china['ma_price'], china['ma_volume'], china['market_cases_'])
    fig.add_trace(go.Scatter(x=china.index, y=china['price'], mode='lines', name='P/D', line=dict(color='white', width=1), opacity=0.2))

    # Mostrar gráfica en Streamlit
    st.plotly_chart(fig, use_container_width=True)


with tab_india:
    st.title("India's Market")
    
    last_india = india.index[-1]
    market_state_india = india['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
    st.write(f" India's Market State: {market_state_india} - Last Update: {last_india}")
    # Crear gráfica de Plotly
    fig = chart_colors( india['ma_price'], india['ma_volume'], india['market_cases_'])
    fig.add_trace(go.Scatter(x=india.index, y=india['price'], mode='lines', name='P/D', line=dict(color='white', width=1), opacity=0.2))

    # Mostrar gráfica en Streamlit
    st.plotly_chart(fig, use_container_width=True)


# with tab_turkey:
#     st.title("Turkey's Market")
    
#     last_turkey = turkey.index[-1]
#     market_state_turkey = turkey['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
#     st.write(f" Turkey's Market State: {market_state_turkey} - Last Update: {last_turkey}")
#     # Crear gráfica de Plotly
#     fig = chart_colors( turkey['ma_price'], turkey['ma_volume'], turkey['market_cases_'])
#     fig.add_trace(go.Scatter(x=turkey.index, y=turkey['price'], mode='lines', name='P/D', line=dict(color='white', width=1), opacity=0.2))

#     # Mostrar gráfica en Streamlit
#     st.plotly_chart(fig, use_container_width=True)





