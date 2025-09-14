
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configurar página
st.set_page_config(page_title="Dashboard Empresas Colombia", layout="wide")

# Título
st.title("📊 Dashboard de Empresas Colombianas")
st.markdown("Análisis integral de datos empresariales con indicadores de calidad y riesgo")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv('data/processed/datos_integrados.csv')

df = load_data()

# Métricas principales
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Empresas", len(df))
with col2:
    st.metric("Completitud Promedio", f"{df['Porcentaje_Completitud'].mean():.1f}%")
with col3:
    st.metric("Riesgo Promedio", f"{df['Puntuacion_Riesgo'].mean():.1f}/10")
with col4:
    alto_riesgo = len(df[df['Nivel_Riesgo'].isin(['ALTO', 'CRÍTICO'])])
    st.metric("Empresas Alto Riesgo", alto_riesgo)

# Filtros
st.sidebar.header("Filtros")
region = st.sidebar.multiselect("Región", options=df['Region'].unique())
nivel_riesgo = st.sidebar.multiselect("Nivel de Riesgo", options=df['Nivel_Riesgo'].unique())

# Aplicar filtros
if region:
    df = df[df['Region'].isin(region)]
if nivel_riesgo:
    df = df[df['Nivel_Riesgo'].isin(nivel_riesgo)]

# Gráficos
col1, col2 = st.columns(2)

with col1:
    fig = px.pie(df, names='Region', title='Distribución por Región')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(df['Nivel_Riesgo'].value_counts(), 
                 title='Distribución por Nivel de Riesgo',
                 color=df['Nivel_Riesgo'].value_counts().index,
                 color_discrete_map={'BAJO': 'green', 'MEDIO': 'yellow', 'ALTO': 'orange', 'CRÍTICO': 'red'})
    st.plotly_chart(fig, use_container_width=True)

# Mapa de calor de correlación
st.subheader("Mapa de Calor de Correlación")
corr_matrix = df[['Porcentaje_Completitud', 'Puntuacion_Riesgo', 'PIB_Per_Capita']].corr()
fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
st.plotly_chart(fig, use_container_width=True)

# Datos crudos
if st.checkbox("Mostrar datos crudos"):
    st.subheader("Datos Crudos")
    st.dataframe(df)

# Footer
st.markdown("---")
st.markdown(f"*Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
