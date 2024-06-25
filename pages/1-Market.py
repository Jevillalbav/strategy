import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime as dt

st.set_page_config(layout="wide")
#3 Titulo
st.title('Market Data')


def chart_colors_two_axis(left, right, cases):
    siz = 8
    siz = cases.map({0: 0, 1: siz, 2: siz, 3: siz, 4: siz})
    colors = cases.map({0: 'rgba(0,0,0,0)', 1: 'yellow', 2: 'green', 3: 'blue', 4: 'red'})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=left.index, y=left           , mode='lines', 
                            line=dict(color='white', width=1), opacity=1, hoverinfo='skip', name= left.name))
    fig.add_trace(go.Scatter(x=left.index, y= left, mode='markers',
                            marker=dict(color= colors, size=siz, line = dict(width=0)), name=left.name))
    fig.add_trace(go.Scatter(x=right.index, y= right, mode='lines', name=right.name,
                                line = dict(color='pink', width=1) , yaxis='y2', opacity=0.8))
    fig.update_layout(
    xaxis_title='Date',
    yaxis_title= left.name,
    yaxis_tickformat = ',.0f',
    yaxis_showgrid=False,
    xaxis_domain=[0.05, 0.9],
    yaxis2 = dict(overlaying='y', side='right', showgrid=False, tickformat = ',.2f', title=right.name, zeroline=False),
    width = 1200, height = 800, template='plotly_dark',  hovermode='x', showlegend=False)
    return fig
def chart_colors_one_axis(left, cases):
    siz = 8
    siz = cases.map({0: 0, 1: siz, 2: siz, 3: siz, 4: siz})
    colors = cases.map({0: 'rgba(0,0,0,0)', 1: 'yellow', 2: 'green', 3: 'blue', 4: 'red'})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=left.index, y=left           , mode='lines', 
                            line=dict(color='gray', width=1), opacity=1, hoverinfo='skip', name= left.name))
    fig.add_trace(go.Scatter(x=left.index, y= left, mode='markers',
                            marker=dict(color= colors, size=siz, line = dict(width=0)), name=left.name))
    fig.update_layout(
    xaxis_title='Date',
    xaxis_domain=[0.05, 0.9],
    yaxis_title= left.name,
    yaxis_showgrid=False,
    yaxis_tickformat = ',.0f',
    width = 1200, height = 800, template='plotly_dark',  hovermode='x', showlegend=False)
    return fig
def chart_colors_two_axis_no_markers(left, right):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=left.index, y=left           , mode='lines', 
                            line=dict(color='white', width=1), opacity=1, name= left.name))
    fig.add_trace(go.Scatter(x=right.index, y= right, mode='lines', name=right.name,
                                line = dict(color='pink', width=1) , yaxis='y2', opacity=0.9))
    fig.update_layout(
    xaxis_title='Date',
    xaxis_domain=[0.05, 0.9],
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
    xaxis_domain=[0.05, 0.9],
    yaxis_showgrid=False,
    yaxis_title= left.name,
    yaxis_tickformat = ',.0f',
    width = 1200, height = 800, template='plotly_dark',  hovermode='x', showlegend=False)
    return fig



#3 Leo datos de mercado
gold_file = 'data/gold_reader.csv'
china_file = 'data/china_reader.csv'
india_file = 'data/india_reader.csv'
turkey_file = 'data/turkey_reader.csv'
cftc_file = 'data/cftc.csv'


gold = pd.read_csv(gold_file, index_col=0 , parse_dates=True).loc['2024':]
gold['corr'] = gold['corr'].ewm(span=5).mean()
china = pd.read_csv(china_file, index_col=0 , parse_dates=True).loc['2024':]
india = pd.read_csv(india_file, index_col=0 , parse_dates=True).loc['2024':]
turkey = pd.read_csv(turkey_file, index_col=0 , parse_dates=True).loc['2024':]
cftc = pd.read_csv(cftc_file, index_col=0 , parse_dates=True).loc['2024':]






st.subheader(' CFTC Dashboard ')


fig = go.Figure()
fig.update_layout(template='plotly_dark', title= dict(text='Gold CFTC updated: '  + cftc.index[-1].strftime('%Y-%m-%d'),
                  x=0.5, font=dict(size=30, color='white')), title_x=0.5,
                  xaxis = dict(title='Date', showgrid=False, dtick='M1', tickangle=45), # , tickformat='%b %Y',
                  xaxis_range = [cftc.index[0], cftc.index[-1] + dt.timedelta(days=40)],
                    yaxis = dict(title='Net Position', showgrid=False, range = [-500000 , 500000], dtick=50000, tickformat=',.0f'),
                    yaxis2 = dict(title='USD', showgrid=False, overlaying='y1', side='right', tickformat='$,.0f', dtick=50),
                    width = 1700, height = 900, ##3 add a xaxis range slider
                    #margin=dict(l=50, r=50, t=50, b=50), 
                    hovermode='x',
                    #hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(18, 30, 48,0.5)' , namelength=-1, align='right'),

                    #xaxis_rangeslider_visible=True, 
                    )

## change the line of hover to white
fig.update_traces( selector=dict(mode='lines'))


#stacked area chart
## managed
fig.add_scatter(x=cftc.index, y=cftc['managed_pos'], name='Managed',                 
                hoverinfo= np.where(cftc['managed_pos'] == 0, 'skip', 'y+name'),
                line=dict( width=0), mode='lines', showlegend=True, yaxis='y1', stackgroup= 'one' ,  fillcolor='rgba(109, 171, 191,0.8)',  legendgroup='one', legendgrouptitle=dict(text='Long'), legendrank=1)#, hovertemplate='<b>%{x}</b><br><br>Managed: %{y:,.0f}<extra></extra>', hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(109, 171, 191,1)', namelength=-1, align='right'))
fig.add_scatter(x=cftc.index, y=cftc['managed_neg'], name='Managed',
                hoverinfo= np.where(cftc['managed_neg'] == 0, 'skip', 'y+name'),
                 line=dict( width=0), mode='lines', showlegend=True, yaxis='y1', stackgroup= 'two' ,  fillcolor='rgba(109, 171, 191,0.8)', legendgroup='two', legendgrouptitle=dict(text='Short'), legendrank=1)#, hovertemplate='<b>%{x}</b><br><br>Managed: %{y:,.0f}<extra></extra>', hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(109, 171, 191,1)', namelength=-1, align='right'))
## non_reportable
fig.add_scatter(x=cftc.index, y=cftc['non_reportable_pos'], name='Non Reportable',
                hoverinfo= np.where(cftc['non_reportable_pos'] == 0, 'skip', 'y+name'),
                 line=dict( width=0), mode='lines', showlegend=True, yaxis='y1', stackgroup= 'one' ,  fillcolor='rgba(191, 191, 109,0.8)', legendgroup='one', legendgrouptitle=dict(text='Long'), legendrank=2)#, hovertemplate='<b>%{x}</b><br><br>Non Reportable: %{y:,.0f}<extra></extra>', hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(191, 191, 109,1)', namelength=-1, align='right'))
fig.add_scatter(x=cftc.index, y=cftc['non_reportable_neg'], name='Non Reportable',
                hoverinfo= np.where(cftc['non_reportable_neg'] == 0, 'skip', 'y+name'),
                 line=dict( width=0), mode='lines', showlegend=True, yaxis='y1', stackgroup= 'two' ,  fillcolor='rgba(191, 191, 109,0.8)', legendgroup='two', legendgrouptitle=dict(text='Short'), legendrank=2)#), hovertemplate='<b>%{x}</b><br><br>Non Reportable: %{y:,.0f}<extra></extra>', hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(191, 191, 109,1)', namelength=-1, align='right'))

## others
fig.add_scatter(x=cftc.index, y=cftc['others_pos'], name='Others',
                hoverinfo= np.where(cftc['others_pos'] == 0, 'skip', 'y+name'),
                 line=dict( width=0), mode='lines', showlegend=True, yaxis='y1', stackgroup= 'one' ,  fillcolor='rgba(191, 109, 109,0.8)', legendgroup='one', legendgrouptitle=dict(text='Long'), legendrank=3)#, hovertemplate='<b>%{x}</b><br><br>Others: %{y:,.0f}<extra></extra>', hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(191, 109, 109,1)', namelength=-1, align='right'))
fig.add_scatter(x=cftc.index, y=cftc['others_neg'], name='Others', 
                hoverinfo= np.where(cftc['others_neg'] == 0, 'skip', 'y+name'),
                line=dict(width=0), mode='lines', showlegend=True, yaxis='y1', stackgroup= 'two' ,  fillcolor='rgba(191, 109, 109,0.8)', legendgroup='two', legendgrouptitle=dict(text='Short'), legendrank=3)#, hovertemplate='<b>%{x}</b><br><br>Others: %{y:,.0f}<extra></extra>', hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(191, 109, 109,1)', namelength=-1, align='right'))

## producer
fig.add_scatter(x=cftc.index, y=cftc['producer_pos'], name='Producer',
                hoverinfo= np.where(cftc['producer_pos'] == 0, 'skip', 'y+name'),
                 line=dict(width=0), mode='lines', showlegend=True, yaxis='y1', stackgroup= 'one' ,  fillcolor='rgba(68, 194, 101,0.8)', legendgroup='one', legendgrouptitle=dict(text='Long'), legendrank=4)#, hovertemplate='<b>%{x}</b><br><br>Producer: %{y:,.0f}<extra></extra>', hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(68, 194, 101,1)', namelength=-1, align='right'))
fig.add_scatter(x=cftc.index, y=cftc['producer_neg'], name='Producer',
                hoverinfo= np.where(cftc['producer_neg'] == 0, 'skip', 'y+name'),
                 line=dict(width=0), mode='lines', showlegend=True, yaxis='y1', stackgroup= 'two' ,  fillcolor='rgba(68, 194, 101,0.8)', legendgroup='two', legendgrouptitle=dict(text='Short'), legendrank=4)#, hovertemplate='<b>%{x}</b><br><br>Producer: %{y:,.0f}<extra></extra>', hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(68, 194, 101,1)', namelength=-1, align='right'))

## swap
fig.add_scatter(x=cftc.index, y=cftc['swap_pos'], name='Swap Dealers', 
                hoverinfo= np.where(cftc['swap_pos'] == 0, 'skip', 'y+name'),
                line=dict(width=0), mode='lines', showlegend=True, yaxis='y1', stackgroup= 'one' ,  fillcolor='rgba(194, 68, 101,0.8)', legendgroup='one', legendgrouptitle=dict(text='Long'), legendrank=5)#, hovertemplate='<b>%{x}</b><br><br>Swap: %{y:,.0f}<extra></extra>', hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(194, 68, 101,1)', namelength=-1, align='right'))
fig.add_scatter(x=cftc.index, y=cftc['swap_neg'], name='Swap Dealers', 
                hoverinfo= np.where(cftc['swap_neg'] == 0, 'skip', 'y+name'),
                line=dict(width=0), mode='lines', showlegend=True, yaxis='y1', stackgroup= 'two' ,  fillcolor='rgba(194, 68, 101,0.8)', legendgroup='two', legendgrouptitle=dict(text='Short'), legendrank=5)#, hovertemplate='<b>%{x}</b><br><br>Swap: %{y:,.0f}<extra></extra>', hoverlabel=dict(font=dict(size=15), bordercolor='white', bgcolor = 'rgba(194, 68, 101,1)', namelength=-1, align='right'))


# ## gold 
fig.add_scatter(x=gold.index, y=gold['price'], name='Gold',
                hoverinfo='y+name', 
                 line=dict(color='gold', width=1), mode='lines', showlegend=True, yaxis='y2', legendgroup='three', legendgrouptitle=dict(text='Gold'), legendrank=1)#, hovertemplate='<b>%{x}</b><br><br>Gold: %{y:,.0f}<extra></extra>')


fig.add_scatter(x = gold.index , y= (gold['ma_price'] * 0) - 100000000 , opacity=0 , 
                hoverinfo='x' , showlegend=False
                )



# ### legend should be horaizontal and on the top left corner
fig.update_layout(legend=dict(x=0.01, y=1, bgcolor='rgba(18, 30, 48,0.7)', 
                               orientation='h', font=dict(size=12, color='white'), bordercolor='white', borderwidth=1),
                               )




# ## add a vertical line for the current date
fig.add_shape(type='line', x0=cftc.index[-1]  , y0=-700000, x1=cftc.index[-1], y1=700000, line=dict(color='rgba(245, 245, 245, 0.2)', width=1, dash='dash'), xref='x', yref='y1', layer='below')

# ## add a horizontal line for the current net position
fig.add_shape(type='line', x0= cftc.index[0] , y0=cftc['long'].iloc[-1], x1=cftc.index[-1], y1=cftc['long'].iloc[-1], line=dict(color='rgba(245, 245, 245, 0.2)', width=1, dash = 'dash'), xref='x', yref='y1', layer='below')

# ## add a horizontal line for the current net position
fig.add_shape(type='line', x0= cftc.index[0] , y0=cftc['short'].iloc[-1], x1=cftc.index[-1], y1=cftc['short'].iloc[-1], line=dict(color='rgba(245, 245, 245, 0.2)', width=1, dash = 'dash'), xref='x', yref='y1', layer='below')


fig.update_xaxes(hoverformat='%Y-%m-%d')
# ## hide legend 
fig.update_layout(showlegend=False)

fig.update_layout(legend= {'itemsizing': 'constant'})
# fig.show()

st.plotly_chart(fig, use_container_width=True)
#st.markdown('---')







st.subheader("London's market")

# Guardo los datos
last_world = gold.index.date[-1]
market_state_last = gold['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
market_state_current = gold['market_cases'].map({0: ' No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
last_price = gold['price'].iloc[-1]

st.write(f" Up to {last_world} world gold has been on a {market_state_current} state. The last update per market state was {market_state_last}. Current price is {last_price} USD/oz. ")
# Crear gráfica de Plotly
fig = chart_colors_two_axis( gold['ma_price'], gold['ma_volume'], gold['market_cases'])
fig.add_trace(go.Scatter(x=gold.index, y=gold['price'], mode='lines', name='London FIX', line=dict(color='gold', width=1.5), opacity=0.9))
st.plotly_chart(fig, use_container_width=True)

# st.markdown('---')
# st.subheader(' Gold Price vs Volume Cross Correlation')
# st.markdown(f'Cross correlation is currently at: {gold["corr"].iloc[-1]:.0%}, compared to yesterday\'s {gold["corr"].iloc[-2]:.0%}')

# fig = chart_colors_two_axis_no_markers( gold['price'], gold['corr'])
# fig.add_hline(y=0, line_color='red', yref='y2', line_width=0.5)
# fig.update_layout(xaxis_range = [gold.index[0], gold.index[-1] + dt.timedelta(days=20)])

# st.plotly_chart(fig, use_container_width=True)
# st.markdown('---')
##########################

##########################
st.subheader(' China Market')
last_china = china.index.date[-1]
market_state_last_china = china['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
market_state_current_china = china['market_cases'].map({0: ' No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
last_pd = china['price'].iloc[-1]
bef_last_pd = china['price'].iloc[-2]
st.write(f" Up to {last_china} China gold has been on a {market_state_current_china} state. The last update per market state was {market_state_last_china}. Current Premium Discount is {last_pd:.2f} USD/oz. compared to yesterday's {bef_last_pd:.2f} USD/oz. ")

fig = chart_colors_two_axis( china['ma_price'], china['ma_volume']/1000000, china['market_cases'])
fig.add_trace(go.Scatter(x=china.index, y=china['price'], mode='lines', name='China P/D', line=dict(color='gold', width=1), opacity=0.2))
st.plotly_chart(fig, use_container_width=True)
# st.markdown('---')


##########################
st.subheader(' India Market')
last_india = india.index.date[-1]
market_state_last_india = india['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
market_state_current_india = india['market_cases'].map({0: ' No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
last_pd_india = india['price'].iloc[-1]
bef_last_pd_india = india['price'].iloc[-2]
st.write(f" Up to {last_india} India gold has been on a {market_state_current_india} state. The last update per market state was {market_state_last_india}. Current Premium Discount is {last_pd_india:.2f} USD/oz. compared to yesterday's {bef_last_pd_india:.2f} USD/oz. ")

fig = chart_colors_two_axis( india['ma_price'], india['ma_volume'], india['market_cases'])
fig.add_trace(go.Scatter(x=india.index, y=india['price'], mode='lines', name='India P/D', line=dict(color='gold', width=1), opacity=0.2))
st.plotly_chart(fig, use_container_width=True)
# st.markdown('---')


##########################
st.subheader(' Turkey market')
last_turkey = turkey.index.date[-1]
market_state_last_turkey = turkey['market_cases_'].map({0: 'No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
market_state_current_turkey = turkey['market_cases'].map({0: ' No Signal', 1: ' Supply Scarcity', 2: 'Demand Abundance', 3: 'Demand Scarcity', 4: 'Supply Abundance'}).iloc[-1]
last_pd_turkey = turkey['price'].iloc[-1]
bef_last_pd_turkey = turkey['price'].iloc[-2]
st.write(f" Up to {last_turkey} Turkey gold has been on a {market_state_current_turkey} state. The last update per market state was {market_state_last_turkey}. Current Premium Discount is {last_pd_turkey:.2f} USD/oz. compared to yesterday's {bef_last_pd_turkey:.2f} USD/oz. ")

fig = chart_colors_two_axis( turkey['ma_price'], turkey['ma_volume'], turkey['market_cases'])
fig.add_trace(go.Scatter(x=turkey.index, y=turkey['price'], mode='lines', name='Turkey P/D', line=dict(color='gold', width=1), opacity=0.2))
st.plotly_chart(fig, use_container_width=True)
# st.markdown('---')


##########################


