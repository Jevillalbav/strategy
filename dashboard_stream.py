import streamlit as st
import pandas as pd

# Configurar Streamlit
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# Título
st.title("Financial Dashboard")

# Leer datos desde archivos locales
prop_file = 'prop.csv'
tt_file = 'trades.csv'
metrics_file = 'metrics.csv'
plotly_graph_file = 'fig.html'

# Leer los datos
try:
    prop_ = pd.read_csv(prop_file, index_col=0, parse_dates=True)
    tt = pd.read_csv(tt_file, index_col=0)
    metrics = pd.read_csv(metrics_file, index_col=0)
except Exception as e:
    st.error(f"Error loading data: {e}")

# Cargar y mostrar gráfica de Plotly guardada localmente
st.subheader("Plotly Graph")

try:
    with open(plotly_graph_file, 'r') as f:
        plotly_graph_html = f.read()
    st.components.v1.html(plotly_graph_html, height=800)
except Exception as e:
    st.error(f"Error loading the Plotly graph: {e}")

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
