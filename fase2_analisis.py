#!/usr/bin/env python3
"""
Fase 2 - Análisis y Enriquecimiento de Datos (Sprint 2)
Objetivo: Analizar los datos limpios y enriquecerlos con información adicional
Entregables: 
1. Reporte de análisis exploratorio
2. Datos enriquecidos
3. Dashboard de visualización
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from datetime import datetime

def configurar_entorno():
    """Configura las rutas y crea directorios necesarios"""
    base_dir = Path.cwd()
    data_dir = base_dir / "data"
    processed_data_dir = data_dir / "processed"
    output_data_dir = data_dir / "output"
    reports_dir = base_dir / "reports"
    
    # Crear directorios si no existen
    processed_data_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    return {
        'base_dir': base_dir,
        'processed_data_dir': processed_data_dir,
        'output_data_dir': output_data_dir,
        'reports_dir': reports_dir
    }

def cargar_datos_limpios(ruta_archivo):
    """Carga los datos limpios desde el archivo CSV"""
    try:
        print("Cargando datos limpios...")
        df = pd.read_csv(ruta_archivo)
        print(f"Datos limpios cargados correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
        return df
    except Exception as e:
        print(f"Error al cargar los datos limpios: {e}")
        return None

def convertir_a_serializable(obj):
    """Convierte objetos no serializables a formatos compatibles con JSON"""
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif pd.isna(obj):
        return None
    elif hasattr(obj, 'dtype') and pd.api.types.is_object_dtype(obj):
        return str(obj)
    else:
        return obj

def analisis_exploratorio(df):
    """Realiza análisis exploratorio de los datos"""
    print("\n" + "="*60)
    print("ANÁLISIS EXPLORATORIO DE DATOS")
    print("="*60)
    
    resultados = {}
    
    # 1. Estadísticas básicas
    resultados['estadisticas_basicas'] = {
        'total_registros': len(df),
        'total_columnas': len(df.columns),
        'registros_por_tipo_dato': {str(k): v for k, v in df.dtypes.value_counts().to_dict().items()}
    }
    
    print(f"Total de registros: {len(df)}")
    print(f"Total de columnas: {len(df.columns)}")
    
    # 2. Análisis de valores nulos
    nulos_por_columna = df.isnull().sum()
    porcentaje_nulos = (nulos_por_columna / len(df) * 100).round(2)
    
    resultados['valores_nulos'] = {
        'por_columna': nulos_por_columna.to_dict(),
        'porcentaje_por_columna': porcentaje_nulos.to_dict(),
        'total_nulos': int(nulos_por_columna.sum()),
        'porcentaje_total_nulos': float((nulos_por_columna.sum() / (len(df) * len(df.columns)) * 100).round(2))
    }
    
    print("\nValores nulos por columna:")
    for columna, nulos in nulos_por_columna.items():
        if nulos > 0:
            print(f"  - {columna}: {nulos} ({porcentaje_nulos[columna]}%)")
    
    # 3. Análisis de ciudades
    resultados['analisis_ciudades'] = {
        'total_ciudades_unicas': int(df['Ciudad_Act'].nunique()),
        'top_10_ciudades': df['Ciudad_Act'].value_counts().head(10).to_dict(),
        'distribucion_ciudades': df['Ciudad_Act'].value_counts(normalize=True).head(10).to_dict()
    }
    
    print(f"\nTotal de ciudades únicas: {df['Ciudad_Act'].nunique()}")
    print("\nTop 10 ciudades por cantidad de empresas:")
    for ciudad, count in resultados['analisis_ciudades']['top_10_ciudades'].items():
        print(f"  - {ciudad}: {count} empresas")
    
    # 4. Análisis de gerentes
    gerentes_unicos = df[['NombresGerenteGeneral_Act', 'ApellidosGerenteGeneral_Act']].drop_duplicates()
    resultados['analisis_gerentes'] = {
        'total_gerentes_unicos': len(gerentes_unicos),
        'gerentes_multiple_empresas': analizar_gerentes_multiple_empresas(df)
    }
    
    print(f"\nTotal de gerentes únicos: {len(gerentes_unicos)}")
    
    # 5. Análisis de códigos DANE
    resultados['analisis_dane'] = {
        'codigos_dane_unicos': int(df['CodDANE'].nunique()),
        'codigos_dane_invalidos': int(df['CodDANE'].isnull().sum())
    }
    
    # 6. Análisis de teléfonos
    resultados['analisis_telefonos'] = {
        'telefonos_1_validos': int(df['Telefono_Act1'].notnull().sum()),
        'telefonos_2_validos': int(df['Telefono_Act2'].notnull().sum()),
        'porcentaje_telefonos_1': float((df['Telefono_Act1'].notnull().sum() / len(df) * 100).round(2)),
        'porcentaje_telefonos_2': float((df['Telefono_Act2'].notnull().sum() / len(df) * 100).round(2))
    }
    
    # Convertir todos los valores a serializables
    resultados = convertir_resultados_serializables(resultados)
    
    return resultados

def convertir_resultados_serializables(resultados):
    """Convierte todos los valores en el diccionario de resultados a serializables"""
    def _convertir_valores(obj):
        if isinstance(obj, dict):
            return {k: _convertir_valores(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [_convertir_valores(v) for v in obj]
        else:
            return convertir_a_serializable(obj)
    
    return _convertir_valores(resultados)

def analizar_gerentes_multiple_empresas(df):
    """Identifica gerentes que están en múltiples empresas"""
    gerentes_empresas = df.groupby(['NombresGerenteGeneral_Act', 'ApellidosGerenteGeneral_Act']).size()
    gerentes_multiple = gerentes_empresas[gerentes_empresas > 1]
    
    return {
        'total_gerentes_multiple_empresas': int(len(gerentes_multiple)),
        'gerentes_con_mas_empresas': gerentes_multiple.sort_values(ascending=False).head(10).to_dict()
    }

def enriquecer_datos(df):
    """Enriquece los datos con información adicional"""
    print("\n" + "="*60)
    print("ENRIQUECIMIENTO DE DATOS")
    print("="*60)
    
    df_enriquecido = df.copy()
    
    # 1. Agregar región basada en código DANE
    df_enriquecido['Region'] = df_enriquecido['CodDANE'].apply(obtener_region_dane)
    
    # 2. Agregar categoría de tamaño de empresa (basado en ciudad)
    df_enriquecido['Tamaño_Empresa'] = df_enriquecido['Ciudad_Act'].apply(categorizar_tamaño_empresa)
    
    # 3. Crear identificador único para cada empresa
    df_enriquecido['ID_Empresa'] = crear_ids_empresas(df_enriquecido)
    
    # 4. Agregar fecha de procesamiento
    df_enriquecido['Fecha_Procesamiento'] = datetime.now().strftime('%Y-%m-%d')
    
    # 5. Calcular completitud de datos por registro
    df_enriquecido['Porcentaje_Completitud'] = calcular_completitud(df_enriquecido)
    
    print("Datos enriquecidos con:")
    print("  - Región basada en código DANE")
    print("  - Categoría de tamaño de empresa")
    print("  - ID único para cada empresa")
    print("  - Fecha de procesamiento")
    print("  - Porcentaje de completitud de datos")
    
    return df_enriquecido

def obtener_region_dane(codigo_dane):
    """Obtiene la región basada en el código DANE"""
    if pd.isna(codigo_dane):
        return 'DESCONOCIDA'
    
    codigo_str = str(codigo_dane)
    primer_digito = codigo_str[0] if len(codigo_str) >= 1 else '0'
    
    regiones = {
        '1': 'BOGOTÁ',
        '2': 'ANTIOQUIA',
        '3': 'VALLE',
        '4': 'ATLÁNTICO',
        '5': 'BOLÍVAR',
        '6': 'BOYACÁ',
        '7': 'CALDAS',
        '8': 'CAUCA',
        '9': 'NARIÑO'
    }
    
    return regiones.get(primer_digito, 'OTRA')

def categorizar_tamaño_empresa(ciudad):
    """Categoriza el tamaño de empresa basado en la ciudad"""
    ciudades_principales = ['BOGOTÁ', 'MEDELLÍN', 'CALI', 'BARRANQUILLA', 'CARTAGENA']
    
    if ciudad in ciudades_principales:
        return 'GRANDE'
    elif ciudad in ['BUCARAMANGA', 'PEREIRA', 'SANTA MARTA', 'IBAGUÉ', 'CÚCUTA']:
        return 'MEDIANA'
    else:
        return 'PEQUEÑA'

def crear_ids_empresas(df):
    """Crea IDs únicos para cada empresa"""
    from datetime import datetime
    import hashlib
    
    base_time = datetime.now().strftime('%Y%m%d%H%M%S')
    base_hash = int(hashlib.sha256(base_time.encode()).hexdigest(), 16) % (10 ** 8)
    ids = []
    
    for i in range(len(df)):
        ids.append(f"EMP{base_hash + i:08d}")
    
    return ids

def calcular_completitud(df):
    """Calcula el porcentaje de completitud de datos por registro"""
    columnas_relevantes = [
        'NombresGerenteGeneral_Act', 'ApellidosGerenteGeneral_Act',
        'NombresGerenteFinanciero_Act', 'ApellidosGerenteFinanciero_Act',
        'Ciudad_Act', 'CodDANE', 'Telefono_Act1'
    ]
    
    completitud = []
    for _, row in df.iterrows():
        campos_llenos = sum(1 for col in columnas_relevantes if not pd.isna(row[col]) and str(row[col]).strip() != '')
        porcentaje = (campos_llenos / len(columnas_relevantes) * 100)
        completitud.append(round(porcentaje, 2))
    
    return completitud

def generar_visualizaciones(df, resultados, reports_dir):
    """Genera visualizaciones para el dashboard"""
    print("\n" + "="*60)
    print("GENERANDO VISUALIZACIONES")
    print("="*60)
    
    # Configurar estilo de las gráficas
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 1. Distribución de empresas por ciudad (Top 10)
    plt.figure(figsize=(12, 8))
    top_ciudades = df['Ciudad_Act'].value_counts().head(10)
    ax = top_ciudades.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Ciudades por Cantidad de Empresas', fontsize=16, fontweight='bold')
    plt.xlabel('Ciudad', fontsize=12)
    plt.ylabel('Cantidad de Empresas', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Añadir valores en las barras
    for i, v in enumerate(top_ciudades):
        ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(reports_dir / 'distribucion_ciudades.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Distribución por región (si existe la columna)
    if 'Region' in df.columns:
        plt.figure(figsize=(10, 8))
        region_counts = df['Region'].value_counts()
        plt.pie(region_counts.values, labels=region_counts.index, autopct='%1.1f%%')
        plt.title('Distribución de Empresas por Región', fontsize=16, fontweight='bold')
        plt.savefig(reports_dir / 'distribucion_regiones.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # 3. Completitud de datos
    plt.figure(figsize=(10, 6))
    if 'Porcentaje_Completitud' in df.columns:
        plt.hist(df['Porcentaje_Completitud'], bins=20, color='lightgreen', edgecolor='black')
        plt.title('Distribución de Completitud de Datos', fontsize=16, fontweight='bold')
        plt.xlabel('Porcentaje de Completitud', fontsize=12)
        plt.ylabel('Cantidad de Empresas', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(reports_dir / 'completitud_datos.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # 4. Teléfonos válidos
    telefonos_data = {
        'Teléfono Principal': resultados['analisis_telefonos']['porcentaje_telefonos_1'],
        'Teléfono Secundario': resultados['analisis_telefonos']['porcentaje_telefonos_2']
    }
    
    plt.figure(figsize=(8, 6))
    plt.bar(telefonos_data.keys(), telefonos_data.values(), color=['blue', 'orange'])
    plt.title('Porcentaje de Teléfonos Válidos', fontsize=16, fontweight='bold')
    plt.ylabel('Porcentaje (%)', fontsize=12)
    plt.ylim(0, 100)
    
    for i, v in enumerate(telefonos_data.values()):
        plt.text(i, v + 1, f'{v}%', ha='center', va='bottom')
    
    plt.savefig(reports_dir / 'telefonos_validos.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Visualizaciones generadas y guardadas en la carpeta reports/")

def generar_reporte(resultados, reports_dir):
    """Genera un reporte completo en formato JSON y TXT"""
    print("\n" + "="*60)
    print("GENERANDO REPORTE")
    print("="*60)
    
    # Reporte en JSON
    try:
        with open(reports_dir / 'reporte_analisis.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        print("✓ Reporte JSON generado exitosamente")
    except Exception as e:
        print(f"✗ Error al generar reporte JSON: {e}")
    
    # Reporte en texto plano
    try:
        with open(reports_dir / 'reporte_analisis.txt', 'w', encoding='utf-8') as f:
            f.write("REPORTE DE ANÁLISIS - DATOS DE EMPRESAS\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("ESTADÍSTICAS BÁSICAS:\n")
            f.write(f"- Total de registros: {resultados['estadisticas_basicas']['total_registros']}\n")
            f.write(f"- Total de columnas: {resultados['estadisticas_basicas']['total_columnas']}\n\n")
            
            f.write("ANÁLISIS DE CIUDADES:\n")
            f.write(f"- Ciudades únicas: {resultados['analisis_ciudades']['total_ciudades_unicas']}\n")
            f.write("- Top 10 ciudades:\n")
            for ciudad, count in resultados['analisis_ciudades']['top_10_ciudades'].items():
                f.write(f"  - {ciudad}: {count} empresas\n")
            
            f.write("\nANÁLISIS DE GERENTES:\n")
            f.write(f"- Gerentes únicos: {resultados['analisis_gerentes']['total_gerentes_unicos']}\n")
            f.write(f"- Gerentes en múltiples empresas: {resultados['analisis_gerentes']['gerentes_multiple_empresas']['total_gerentes_multiple_empresas']}\n")
            
            f.write("\nANÁLISIS DE TELÉFONOS:\n")
            f.write(f"- Teléfonos principales válidos: {resultados['analisis_telefonos']['porcentaje_telefonos_1']}%\n")
            f.write(f"- Teléfonos secundarios válidos: {resultados['analisis_telefonos']['porcentaje_telefonos_2']}%\n")
            
            f.write("\nCALIDAD DE DATOS:\n")
            f.write(f"- Porcentaje total de valores nulos: {resultados['valores_nulos']['porcentaje_total_nulos']}%\n")
        
        print("✓ Reporte TXT generado exitosamente")
    except Exception as e:
        print(f"✗ Error al generar reporte TXT: {e}")

def main():
    """Función principal de la Fase 2"""
    print("=" * 60)
    print("FASE 2 - ANÁLISIS Y ENRIQUECIMIENTO DE DATOS (SPRINT 2)")
    print("=" * 60)
    
    # Configurar entorno
    config = configurar_entorno()
    
    # Cargar datos limpios
    ruta_datos_limpios = config['output_data_dir'] / "datos_limpios.csv"
    df = cargar_datos_limpios(ruta_datos_limpios)
    
    if df is None:
        print("No se pudieron cargar los datos limpios. Ejecute primero la Fase 1.")
        return
    
    # Realizar análisis exploratorio
    resultados_analisis = analisis_exploratorio(df)
    
    # Enriquecer datos
    df_enriquecido = enriquecer_datos(df)
    
    # Generar visualizaciones
    generar_visualizaciones(df_enriquecido, resultados_analisis, config['reports_dir'])
    
    # Generar reportes
    generar_reporte(resultados_analisis, config['reports_dir'])
    
    # Guardar datos enriquecidos
    ruta_enriquecido_csv = config['processed_data_dir'] / "datos_enriquecidos.csv"
    ruta_enriquecido_excel = config['processed_data_dir'] / "datos_enriquecidos.xlsx"
    
    df_enriquecido.to_csv(ruta_enriquecido_csv, index=False, encoding='utf-8')
    df_enriquecido.to_excel(ruta_enriquecido_excel, index=False)
    
    print("\n" + "=" * 60)
    print("RESULTADOS DE LA FASE 2")
    print("=" * 60)
    print("Archivos generados:")
    print(f"- Datos enriquecidos (CSV): {ruta_enriquecido_csv}")
    print(f"- Datos enriquecidos (Excel): {ruta_enriquecido_excel}")
    print(f"- Reporte de análisis (JSON): {config['reports_dir'] / 'reporte_analisis.json'}")
    print(f"- Reporte de análisis (TXT): {config['reports_dir'] / 'reporte_analisis.txt'}")
    print(f"- Visualizaciones: {config['reports_dir']}/*.png")
    
    print("\n" + "=" * 60)
    print("PRÓXIMOS PASOS RECOMENDADOS")
    print("=" * 60)
    print("1. Revisar el reporte de análisis para identificar oportunidades de mejora")
    print("2. Utilizar las visualizaciones para presentaciones ejecutivas")
    print("3. Integrar con fuentes externas para mayor enriquecimiento")
    print("4. Implementar monitoreo continuo de calidad de datos")
    
    print("\n¡Fase 2 completada exitosamente!")

if __name__ == "__main__":
    main()