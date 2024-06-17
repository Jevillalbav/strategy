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
                            line=dict(color='gray', width=1), opacity=1, hoverinfo='skip', name= left.name))
    fig.add_trace(go.Scatter(x=right.index, y= right, mode='lines', name=right.name,
                                line = dict(color='pink', width=0.4) , yaxis='y2', opacity=0.7))
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