import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime as dt


st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.title("Consensus Economics - Reviews")


st.sidebar.subheader("Report Filters")