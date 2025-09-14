#!/usr/bin/env python3
"""
Fase 3 - Integración y Dashboard (Sprint 3)
Objetivo: Integrar datos con fuentes externas y crear dashboard interactivo
Entregables: 
1. Datos integrados con fuentes externas
2. Dashboard interactivo
3. Sistema de monitorización de calidad
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from pathlib import Path
import json
from datetime import datetime, timedelta
import requests
from sqlalchemy import create_engine
import sqlite3
import warnings
warnings.filterwarnings('ignore')

def configurar_entorno():
    """Configura las rutas y crea directorios necesarios"""
    base_dir = Path.cwd()
    data_dir = base_dir / "data"
    processed_data_dir = data_dir / "processed"
    output_data_dir = data_dir / "output"
    reports_dir = base_dir / "reports"
    dashboards_dir = base_dir / "dashboards"
    database_dir = base_dir / "database"
    
    # Crear directorios si no existen
    dashboards_dir.mkdir(parents=True, exist_ok=True)
    database_dir.mkdir(parents=True, exist_ok=True)
    
    return {
        'base_dir': base_dir,
        'processed_data_dir': processed_data_dir,
        'output_data_dir': output_data_dir,
        'reports_dir': reports_dir,
        'dashboards_dir': dashboards_dir,
        'database_dir': database_dir
    }

def cargar_datos_enriquecidos(ruta_archivo):
    """Carga los datos enriquecidos desde el archivo CSV"""
    try:
        print("Cargando datos enriquecidos...")
        df = pd.read_csv(ruta_archivo)
        print(f"Datos enriquecidos cargados correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
        return df
    except Exception as e:
        print(f"Error al cargar los datos enriquecidos: {e}")
        return None

def integrar_datos_externos(df):
    """Integra datos de fuentes externas"""
    print("\n" + "="*60)
    print("INTEGRACIÓN CON FUENTES EXTERNAS")
    print("="*60)
    
    df_integrado = df.copy()
    
    # 1. Integrar datos económicos por región (datos simulados)
    print("Integrando datos económicos por región...")
    datos_economicos = obtener_datos_economicos()
    df_integrado = df_integrado.merge(datos_economicos, on='Region', how='left')
    
    # 2. Integrar información demográfica (datos simulados)
    print("Integrando información demográfica...")
    datos_demograficos = obtener_datos_demograficos()
    df_integrado = df_integrado.merge(datos_demograficos, on='Ciudad_Act', how='left')
    
    # 3. Agregar información de clima empresarial
    print("Integrando clima empresarial...")
    df_integrado['Clima_Empresarial'] = df_integrado['Region'].apply(calcular_clima_empresarial)
    
    # 4. Agregar puntuación de riesgo
    print("Calculando puntuación de riesgo...")
    df_integrado['Puntuacion_Riesgo'] = calcular_puntuacion_riesgo(df_integrado)
    
    # 5. Categorizar por nivel de riesgo
    df_integrado['Nivel_Riesgo'] = pd.cut(
        df_integrado['Puntuacion_Riesgo'],
        bins=[0, 3, 6, 9, 10],
        labels=['BAJO', 'MEDIO', 'ALTO', 'CRÍTICO']
    )
    
    print("✓ Integración con fuentes externas completada")
    print(f"Columnas añadidas: {set(df_integrado.columns) - set(df.columns)}")
    
    return df_integrado

def obtener_datos_economicos():
    """Obtiene datos económicos por región (simulados)"""
    # Datos simulados de PIB per cápita por región (en millones de COP)
    datos_economicos = {
        'Region': ['BOGOTÁ', 'ANTIOQUIA', 'VALLE', 'ATLÁNTICO', 'BOLÍVAR', 
                  'BOYACÁ', 'CALDAS', 'CAUCA', 'NARIÑO', 'OTRA'],
        'PIB_Per_Capita': [25.6, 18.3, 17.8, 16.2, 14.5, 13.8, 14.2, 11.5, 10.8, 12.0],
        'Tasa_Desempleo': [10.2, 11.5, 12.1, 13.8, 14.5, 12.8, 13.2, 15.5, 16.2, 14.0],
        'Crecimiento_Economico': [3.2, 2.8, 2.9, 2.5, 2.3, 2.6, 2.4, 1.8, 1.5, 2.0]
    }
    return pd.DataFrame(datos_economicos)

def obtener_datos_demograficos():
    """Obtiene datos demográficos por ciudad (simulados)"""
    # Datos simulados de población por ciudad
    datos_demograficos = {
        'Ciudad_Act': ['BOGOTÁ', 'MEDELLÍN', 'CALI', 'BARRANQUILLA', 'CARTAGENA',
                      'BUCARAMANGA', 'PEREIRA', 'SANTA MARTA', 'IBAGUÉ', 'CÚCUTA',
                      'PASTO', 'MANIZALES', 'NEIVA', 'VILLAVICENCIO', 'MONTERÍA',
                      'VALLEDUPAR', 'SINCELEJO', 'POPAYÁN', 'TUNJA', 'RIOHACHA'],
        'Poblacion': [8180, 2560, 2250, 1280, 1040, 580, 480, 520, 560, 680,
                     450, 420, 350, 480, 420, 480, 280, 320, 200, 250],
        'Densidad_Poblacion': [4200, 6800, 3900, 7200, 8500, 5200, 4800, 4500, 
                              3800, 5100, 4200, 4500, 3800, 3200, 3500, 2800, 
                              3100, 2900, 4200, 1800]
    }
    return pd.DataFrame(datos_demograficos)

def calcular_clima_empresarial(region):
    """Calcula clima empresarial basado en la región (simulado)"""
    clima_por_region = {
        'BOGOTÁ': 'MUY FAVORABLE',
        'ANTIOQUIA': 'FAVORABLE',
        'VALLE': 'FAVORABLE',
        'ATLÁNTICO': 'MODERADO',
        'BOLÍVAR': 'MODERADO',
        'BOYACÁ': 'MODERADO',
        'CALDAS': 'MODERADO',
        'CAUCA': 'DESFAVORABLE',
        'NARIÑO': 'DESFAVORABLE',
        'OTRA': 'MODERADO'
    }
    return clima_por_region.get(region, 'MODERADO')

def calcular_puntuacion_riesgo(df):
    """Calcula puntuación de riesgo basada en múltiples factores"""
    puntuaciones = []
    
    for _, row in df.iterrows():
        puntuacion = 5  # Puntuación base
        
        # Ajustar basado en completitud de datos
        completitud = row.get('Porcentaje_Completitud', 50)
        if completitud < 60:
            puntuacion += 2
        elif completitud < 80:
            puntuacion += 1
        
        # Ajustar basado en región
        region = row.get('Region', 'OTRA')
        if region in ['CAUCA', 'NARIÑO']:
            puntuacion += 2
        elif region == 'OTRA':
            puntuacion += 1
        
        # Ajustar basado en tamaño de empresa
        tamaño = row.get('Tamaño_Empresa', 'PEQUEÑA')
        if tamaño == 'PEQUEÑA':
            puntuacion += 1
        
        # Limitar a máximo 10
        puntuacion = min(puntuacion, 10)
        
        puntuaciones.append(puntuacion)
    
    return puntuaciones

def crear_base_datos(df, database_dir):
    """Crea una base de datos SQLite con los datos integrados"""
    print("\n" + "="*60)
    print("CREANDO BASE DE DATOS")
    print("="*60)
    
    try:
        # Crear conexión a la base de datos
        ruta_db = database_dir / "empresas_colombia.db"
        engine = create_engine(f'sqlite:///{ruta_db}')
        
        # Guardar datos en la base de datos
        df.to_sql('empresas', engine, if_exists='replace', index=False)
        
        # Crear tablas adicionales para análisis
        crear_tablas_analiticas(engine, df)
        
        print(f"✓ Base de datos creada exitosamente: {ruta_db}")
        return True
        
    except Exception as e:
        print(f"✗ Error al crear base de datos: {e}")
        return False

def crear_tablas_analiticas(engine, df):
    """Crea tablas analíticas adicionales en la base de datos"""
    
    # Tabla de resumen por región
    resumen_region = df.groupby('Region').agg({
        'ID_Empresa': 'count',
        'Puntuacion_Riesgo': 'mean',
        'Porcentaje_Completitud': 'mean',
        'PIB_Per_Capita': 'mean'
    }).round(2).reset_index()
    resumen_region.rename(columns={'ID_Empresa': 'Total_Empresas'}, inplace=True)
    resumen_region.to_sql('resumen_region', engine, if_exists='replace', index=False)
    
    # Tabla de resumen por ciudad
    resumen_ciudad = df.groupby('Ciudad_Act').agg({
        'ID_Empresa': 'count',
        'Puntuacion_Riesgo': 'mean',
        'Porcentaje_Completitud': 'mean'
    }).round(2).reset_index()
    resumen_ciudad.rename(columns={'ID_Empresa': 'Total_Empresas'}, inplace=True)
    resumen_ciudad.to_sql('resumen_ciudad', engine, if_exists='replace', index=False)
    
    # Tabla de distribución de riesgo
    distribucion_riesgo = df['Nivel_Riesgo'].value_counts().reset_index()
    distribucion_riesgo.columns = ['Nivel_Riesgo', 'Cantidad']
    distribucion_riesgo.to_sql('distribucion_riesgo', engine, if_exists='replace', index=False)

def crear_dashboard_interactivo(df, dashboards_dir):
    """Crea un dashboard interactivo con Plotly"""
    print("\n" + "="*60)
    print("CREANDO DASHBOARD INTERACTIVO")
    print("="*60)
    
    try:
        # Crear dashboard con subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Distribución por Región',
                'Niveles de Riesgo',
                'Completitud vs Puntuación de Riesgo',
                'Top 10 Ciudades'
            ),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # 1. Gráfico de pie - Distribución por región
        region_counts = df['Region'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=region_counts.index,
                values=region_counts.values,
                name="Regiones"
            ),
            row=1, col=1
        )
        
        # 2. Gráfico de barras - Niveles de riesgo
        riesgo_counts = df['Nivel_Riesgo'].value_counts()
        fig.add_trace(
            go.Bar(
                x=riesgo_counts.index,
                y=riesgo_counts.values,
                marker_color=['green', 'yellow', 'orange', 'red'],
                name="Niveles de Riesgo"
            ),
            row=1, col=2
        )
        
        # 3. Gráfico de dispersión - Completitud vs Riesgo
        fig.add_trace(
            go.Scatter(
                x=df['Porcentaje_Completitud'],
                y=df['Puntuacion_Riesgo'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=df['Puntuacion_Riesgo'],
                    colorscale='RdYlGn_r',
                    showscale=True
                ),
                name="Completitud vs Riesgo"
            ),
            row=2, col=1
        )
        
        # 4. Gráfico de barras - Top 10 ciudades
        top_ciudades = df['Ciudad_Act'].value_counts().head(10)
        fig.add_trace(
            go.Bar(
                x=top_ciudades.index,
                y=top_ciudades.values,
                marker_color='lightblue',
                name="Top 10 Ciudades"
            ),
            row=2, col=2
        )
        
        # Actualizar layout
        fig.update_layout(
            height=800,
            width=1000,
            title_text="Dashboard Analítico - Empresas de Colombia",
            showlegend=False
        )
        
        # Guardar dashboard
        ruta_dashboard = dashboards_dir / "dashboard_empresas.html"
        fig.write_html(ruta_dashboard)
        print(f"✓ Dashboard interactivo creado: {ruta_dashboard}")
        
        # Crear dashboard adicional de métricas clave
        crear_dashboard_metricas(df, dashboards_dir)
        
        return True
        
    except Exception as e:
        print(f"✗ Error al crear dashboard: {e}")
        return False

def crear_dashboard_metricas(df, dashboards_dir):
    """Crea un dashboard adicional con métricas clave"""
    
    # Calcular métricas clave
    total_empresas = len(df)
    promedio_completitud = df['Porcentaje_Completitud'].mean()
    promedio_riesgo = df['Puntuacion_Riesgo'].mean()
    empresas_alto_riesgo = len(df[df['Nivel_Riesgo'].isin(['ALTO', 'CRÍTICO'])])
    
    # Crear figura con indicadores
    fig = go.Figure()
    
    # Añadir indicadores
    fig.add_trace(go.Indicator(
        mode="number",
        value=total_empresas,
        title={"text": "Total Empresas"},
        domain={'row': 0, 'column': 0}
    ))
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=promedio_completitud,
        title={"text": "Completitud Promedio (%)"},
        domain={'row': 0, 'column': 1}
    ))
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=promedio_riesgo,
        title={"text": "Riesgo Promedio"},
        domain={'row': 0, 'column': 2}
    ))
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=empresas_alto_riesgo,
        title={"text": "Empresas Alto Riesgo"},
        domain={'row': 0, 'column': 3}
    ))
    
    # Configurar layout
    fig.update_layout(
        grid={'rows': 1, 'columns': 4, 'pattern': "independent"},
        title="Métricas Clave - Calidad de Datos",
        height=300
    )
    
    # Guardar dashboard de métricas
    ruta_metricas = dashboards_dir / "metricas_clave.html"
    fig.write_html(ruta_metricas)
    print(f"✓ Dashboard de métricas creado: {ruta_metricas}")

def crear_sistema_monitorizacion(df, database_dir):
    """Crea un sistema de monitorización de calidad de datos"""
    print("\n" + "="*60)
    print("CREANDO SISTEMA DE MONITORIZACIÓN")
    print("="*60)
    
    try:
        # Crear reporte de monitorización
        reporte_monitorizacion = {
            'fecha_generacion': datetime.now().isoformat(),
            'total_registros': len(df),
            'metricas_calidad': {
                'completitud_promedio': float(df['Porcentaje_Completitud'].mean().round(2)),
                'porcentaje_alto_riesgo': float((len(df[df['Nivel_Riesgo'].isin(['ALTO', 'CRÍTICO'])]) / len(df) * 100).round(2)),
                'empresas_sin_telefono': int(df['Telefono_Act1'].isnull().sum()),
                'empresas_sin_gerente_financiero': int(df['NombresGerenteFinanciero_Act'].isnull().sum())
            },
            'distribucion_riesgo': df['Nivel_Riesgo'].value_counts().to_dict(),
            'alertas': generar_alertas_calidad(df)
        }
        
        # Guardar reporte
        ruta_reporte = database_dir / "monitorizacion_calidad.json"
        with open(ruta_reporte, 'w', encoding='utf-8') as f:
            json.dump(reporte_monitorizacion, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Sistema de monitorización creado: {ruta_reporte}")
        return True
        
    except Exception as e:
        print(f"✗ Error al crear sistema de monitorización: {e}")
        return False

def generar_alertas_calidad(df):
    """Genera alertas de calidad basadas en los datos"""
    alertas = []
    
    # Alerta por completitud baja
    empresas_baja_completitud = len(df[df['Porcentaje_Completitud'] < 50])
    if empresas_baja_completitud > 0:
        alertas.append({
            'tipo': 'COMPLETITUD_BAJA',
            'descripcion': f'{empresas_baja_completitud} empresas con completitud menor al 50%',
            'severidad': 'ALTA'
        })
    
    # Alerta por alto riesgo
    empresas_alto_riesgo = len(df[df['Nivel_Riesgo'].isin(['ALTO', 'CRÍTICO'])])
    if empresas_alto_riesgo > 0:
        alertas.append({
            'tipo': 'ALTO_RIESGO',
            'descripcion': f'{empresas_alto_riesgo} empresas con nivel de riesgo ALTO o CRÍTICO',
            'severidad': 'CRÍTICA'
        })
    
    # Alerta por datos de contacto faltantes
    empresas_sin_telefono = len(df[df['Telefono_Act1'].isnull()])
    if empresas_sin_telefono > 0:
        alertas.append({
            'tipo': 'CONTACTO_FALTANTE',
            'descripcion': f'{empresas_sin_telefono} empresas sin teléfono de contacto',
            'severidad': 'MEDIA'
        })
    
    return alertas

def crear_app_streamlit(df, dashboards_dir):
    """Crea una aplicación Streamlit para visualización"""
    print("\n" + "="*60)
    print("CREANDO APLICACIÓN STREAMLIT")
    print("="*60)
    
    try:
        # Crear script de Streamlit
        script_streamlit = """
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
"""
        
        # Guardar script
        ruta_script = dashboards_dir / "app_empresas.py"
        with open(ruta_script, 'w', encoding='utf-8') as f:
            f.write(script_streamlit)
        
        print(f"✓ Aplicación Streamlit creada: {ruta_script}")
        print("  Para ejecutar: streamlit run dashboards/app_empresas.py")
        return True
        
    except Exception as e:
        print(f"✗ Error al crear aplicación Streamlit: {e}")
        return False

def main():
    """Función principal de la Fase 3"""
    print("=" * 60)
    print("FASE 3 - INTEGRACIÓN Y DASHBOARD (SPRINT 3)")
    print("=" * 60)
    
    # Configurar entorno
    config = configurar_entorno()
    
    # Cargar datos enriquecidos
    ruta_datos_enriquecidos = config['processed_data_dir'] / "datos_enriquecidos.csv"
    df = cargar_datos_enriquecidos(ruta_datos_enriquecidos)
    
    if df is None:
        print("No se pudieron cargar los datos enriquecidos. Ejecute primero la Fase 2.")
        return
    
    # Integrar con fuentes externas
    df_integrado = integrar_datos_externos(df)
    
    # Crear base de datos
    crear_base_datos(df_integrado, config['database_dir'])
    
    # Crear dashboards interactivos
    crear_dashboard_interactivo(df_integrado, config['dashboards_dir'])
    
    # Crear sistema de monitorización
    crear_sistema_monitorizacion(df_integrado, config['database_dir'])
    
    # Crear aplicación Streamlit
    crear_app_streamlit(df_integrado, config['dashboards_dir'])
    
    # Guardar datos integrados
    ruta_integrado_csv = config['processed_data_dir'] / "datos_integrados.csv"
    ruta_integrado_excel = config['processed_data_dir'] / "datos_integrados.xlsx"
    
    df_integrado.to_csv(ruta_integrado_csv, index=False, encoding='utf-8')
    df_integrado.to_excel(ruta_integrado_excel, index=False)
    
    print("\n" + "=" * 60)
    print("RESULTADOS DE LA FASE 3")
    print("=" * 60)
    print("Archivos generados:")
    print(f"- Datos integrados (CSV): {ruta_integrado_csv}")
    print(f"- Datos integrados (Excel): {ruta_integrado_excel}")
    print(f"- Base de datos: {config['database_dir'] / 'empresas_colombia.db'}")
    print(f"- Dashboards interactivos: {config['dashboards_dir']}/*.html")
    print(f"- Aplicación Streamlit: {config['dashboards_dir'] / 'app_empresas.py'}")
    print(f"- Sistema de monitorización: {config['database_dir'] / 'monitorizacion_calidad.json'}")
    
    print("\n" + "=" * 60)
    print("INSTRUCCIONES DE USO")
    print("=" * 60)
    print("1. Para ver dashboards: Abrir archivos HTML en navegador web")
    print("2. Para ejecutar aplicación: streamlit run dashboards/app_empresas.py")
    print("3. Para consultar base de datos: Usar SQLite con empresas_colombia.db")
    print("4. Revisar sistema de monitorización para alertas de calidad")
    
    print("\n¡Fase 3 completada exitosamente!")
    print("¡Proyecto de Business Intelligence finalizado! 🎉")

if __name__ == "__main__":
    main()