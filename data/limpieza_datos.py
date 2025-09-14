#!/usr/bin/env python3
"""
Fase 1 - Limpieza y Transformación de Datos (Sprint 1)
Objetivo: Depurar y transformar los datos del archivo BD.xlsx
Entregables: 
1. Archivo limpio (datos_limpios.csv y datos_limpios.xlsx)
2. Diccionario de datos actualizado (diccionario_datos.csv)
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

def configurar_entorno():
    """Configura las rutas y crea directorios necesarios"""
    base_dir = Path.cwd()
    data_dir = base_dir / "data"
    raw_data_dir = data_dir / "raw"
    output_data_dir = data_dir / "output"
    
    # Crear directorios si no existen
    output_data_dir.mkdir(parents=True, exist_ok=True)
    
    return {
        'base_dir': base_dir,
        'raw_data_dir': raw_data_dir,
        'output_data_dir': output_data_dir
    }

def cargar_datos(ruta_archivo):
    """Carga los datos desde el archivo Excel"""
    try:
        print("Cargando datos...")
        df = pd.read_excel(ruta_archivo)
        print(f"Datos cargados correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
        return df
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None

def normalizar_texto(texto):
    """Normaliza texto: convierte a mayúsculas, elimina espacios extras y caracteres especiales"""
    if pd.isna(texto):
        return texto
    
    texto = str(texto)
    
    # Eliminar caracteres especiales excepto letras, números, espacios y ñ/Ñ
    texto = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s]', '', texto)
    
    # Convertir a mayúsculas y eliminar espacios extras
    texto = texto.upper().strip()
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto

def normalizar_ciudad(ciudad):
    """Normaliza los nombres de ciudades usando un diccionario de correcciones"""
    if pd.isna(ciudad):
        return ciudad
    
    ciudad = str(ciudad).strip()
    
    # Diccionario de correcciones de ciudades
    city_corrections = {
        "VOGOTÁ": "BOGOTÁ",
        "BOGOTA%%": "BOGOTÁ",
        "BOGOTAAA": "BOGOTÁ",
        "BOGO)))T2": "BOGOTÁ",
        "BOGOTAAÁ": "BOGOTÁ",
        "SANTIAGHO DE CALY": "SANTIAGO DE CALI",
        "SANTIAGGOPOOO": "SANTIAGO DE CALI",
        "CALY": "CALI",
        "ZANTIAGO DE CALLI": "SANTIAGO DE CALI",
        "POPAYÁNOPO": "POPAYÁN",
        "SAN JUAN DE PPASTO": "SAN JUAN DE PASTO",
        "SAN JOSÉ DEL": "SAN JOSÉ DEL GUAVIARE",
        "SAN JOSÉ DE QÚCUTA": "SAN JOSÉ DE CÚCUTA",
        "LETICIHA": "LETICIA",
        "MANIZALESS": "MANIZALES",
        "P)=STO": "PASTO",
        "PAZT0": "PASTO",
        "TUNJAASSAS": "TUNJA",
        "LICA": "VILLAVICENCIO",
        "FLORENCIATRT": "FLORENCIA",
        "CARTAGENA DE INDIASZZ": "CARTAGENA",
        "YOPAL?)=": "YOPAL",
        "MEDELLÍNN": "MEDELLÍN"
    }
    
    # Buscar corrección en el diccionario
    for patron, correccion in city_corrections.items():
        if patron in ciudad:
            return correccion
    
    # Si no encuentra corrección, normalizar el texto
    return normalizar_texto(ciudad)

def normalizar_telefono(telefono):
    """Normaliza números de teléfono"""
    if pd.isna(telefono) or telefono == "":
        return np.nan
    
    # Convertir a string y eliminar caracteres no numéricos
    telefono_str = str(telefono)
    telefono_limpio = re.sub(r'\D', '', telefono_str)
    
    # Si está vacío después de limpiar, devolver NaN
    if not telefono_limpio:
        return np.nan
    
    # Validar longitud
    if len(telefono_limpio) < 7 or len(telefono_limpio) > 10:
        return np.nan
    
    # Añadir indicativo de Colombia si es necesario
    if len(telefono_limpio) == 7:
        # Asumir que es un número de Bogotá (1) si tiene 7 dígitos
        telefono_limpio = "1" + telefono_limpio
    elif len(telefono_limpio) == 8 and not telefono_limpio.startswith("1"):
        # Asumir que es un número de Bogotá sin el 1
        telefono_limpio = "1" + telefono_limpio
    
    return telefono_limpio

def validar_codigo_dane(codigo):
    """Valida que el código DANE tenga 8 dígitos"""
    if pd.isna(codigo):
        return np.nan
    
    codigo_str = str(codigo)
    
    # Eliminar caracteres no numéricos
    codigo_limpio = re.sub(r'\D', '', codigo_str)
    
    # Validar longitud
    if len(codigo_limpio) != 8:
        return np.nan
    
    return codigo_limpio

def corregir_nombres_propios(texto):
    """Corrige la capitalización de nombres propios"""
    if pd.isna(texto):
        return texto
    
    texto = str(texto).title()
    
    # Lista de excepciones (preposiciones, artículos, etc.)
    excepciones = ['De', 'Del', 'La', 'Las', 'Los', 'Y', 'E', 'I', 'O', 'U']
    
    palabras = texto.split()
    palabras_corregidas = []
    
    for i, palabra in enumerate(palabras):
        if i > 0 and palabra in excepciones:
            palabras_corregidas.append(palabra.lower())
        else:
            palabras_corregidas.append(palabra)
    
    return ' '.join(palabras_corregidas)

def limpiar_datos(df):
    """Función principal para limpiar el dataframe"""
    print("Iniciando limpieza de datos...")
    
    # Hacer una copia para no modificar el original
    df_clean = df.copy()
    
    # 1. Normalizar nombres de columnas
    df_clean.columns = [col.strip() for col in df_clean.columns]
    
    # 2. Eliminar filas completamente vacías
    filas_antes = len(df_clean)
    df_clean = df_clean.dropna(how='all')
    filas_despues = len(df_clean)
    print(f"Eliminadas {filas_antes - filas_despues} filas completamente vacías")
    
    # 3. Normalizar texto en todas las columnas de texto
    text_columns = [col for col in df_clean.columns if df_clean[col].dtype == 'object']
    for col in text_columns:
        df_clean[col] = df_clean[col].apply(normalizar_texto)
    
    # 4. Corregir nombres propios en columnas de nombres
    name_columns = [col for col in df_clean.columns if 'nombre' in col.lower() or 'apellido' in col.lower()]
    for col in name_columns:
        df_clean[col] = df_clean[col].apply(corregir_nombres_propios)
    
    # 5. Normalizar ciudades
    if 'Ciudad_Act' in df_clean.columns:
        df_clean['Ciudad_Act'] = df_clean['Ciudad_Act'].apply(normalizar_ciudad)
    
    # 6. Validar y normalizar código DANE
    if 'CodDANE' in df_clean.columns:
        df_clean['CodDANE'] = df_clean['CodDANE'].apply(validar_codigo_dane)
    
    # 7. Normalizar teléfonos
    phone_columns = [col for col in df_clean.columns if 'telefono' in col.lower()]
    for col in phone_columns:
        df_clean[col] = df_clean[col].apply(normalizar_telefono)
    
    # 8. Manejar valores NULL/NaN
    # Para nombres, reemplazar NULL por NaN
    for col in name_columns:
        df_clean[col] = df_clean[col].replace(['NULL', 'NAN', ''], np.nan)
    
    # 9. Eliminar duplicados exactos
    duplicados_antes = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicados_eliminados = duplicados_antes - len(df_clean)
    print(f"Eliminados {duplicados_eliminados} registros duplicados")
    
    return df_clean

def generar_diccionario_datos(df):
    """Genera un diccionario de datos a partir del dataframe limpio"""
    print("Generando diccionario de datos...")
    
    # Definir descripciones para cada campo
    descripciones = {
        'NombresGerenteGeneral_Act': 'Nombres del gerente general',
        'ApellidosGerenteGeneral_Act': 'Apellidos del gerente general',
        'NombresGerenteFinanciero_Act': 'Nombres del gerente financiero',
        'ApellidosGerenteFinanciero_Act': 'Apellidos del gerente financiero',
        'Ciudad_Act': 'Ciudad de la empresa',
        'CodDANE': 'Código DANE de la ciudad',
        'Telefono_Act1': 'Teléfono principal',
        'Telefono_Act2': 'Teléfono secundario'
    }
    
    # Definir restricciones para cada campo
    restricciones = {
        'NombresGerenteGeneral_Act': 'Máximo 100 caracteres, formato título',
        'ApellidosGerenteGeneral_Act': 'Máximo 100 caracteres, formato título',
        'NombresGerenteFinanciero_Act': 'Máximo 100 caracteres, formato título',
        'ApellidosGerenteFinanciero_Act': 'Máximo 100 caracteres, formato título',
        'Ciudad_Act': 'Valores normalizados de lista predefinida',
        'CodDANE': 'Exactamente 8 dígitos numéricos',
        'Telefono_Act1': '10 dígitos numéricos',
        'Telefono_Act2': '10 dígitos numéricos (opcional)'
    }
    
    # Crear el diccionario de datos
    diccionario = pd.DataFrame({
        'Campo': df.columns,
        'Tipo': df.dtypes.astype(str),
        'Descripción': [descripciones.get(col, '') for col in df.columns],
        'Restricciones': [restricciones.get(col, '') for col in df.columns],
        'Ejemplo': df.iloc[0] if len(df) > 0 else [''] * len(df.columns)
    })
    
    return diccionario

def generar_ciudades_normalizadas():
    """Genera la lista de ciudades normalizadas"""
    ciudades = [
        "BOGOTÁ", "MEDELLÍN", "CALI", "BARRANQUILLA", "CARTAGENA", 
        "CÚCUTA", "BUCARAMANGA", "PEREIRA", "SANTA MARTA", "IBAGUÉ",
        "PASTO", "MANIZALES", "NEIVA", "VILLAVICENCIO", "MONTERÍA",
        "VALLEDUPAR", "SINCELEJO", "POPAYÁN", "TUNJA", "RIOHACHA",
        "QUIBDÓ", "ARMENIA", "FLORENCIA", "YOPAL", "LETICIA",
        "SAN JOSÉ DEL GUAVIARE", "SANTIAGO DE CALI", "SAN JUAN DE PASTO"
    ]
    
    return pd.DataFrame({
        'Ciudad_Normalizada': sorted(ciudades)
    })

def main():
    """Función principal"""
    print("=" * 60)
    print("FASE 1 - LIMPIEZA Y TRANSFORMACIÓN DE DATOS (SPRINT 1)")
    print("=" * 60)
    
    # Configurar entorno
    config = configurar_entorno()
    
    # Cargar datos
    ruta_archivo = config['raw_data_dir'] / "BD.xlsx"
    df = cargar_datos(ruta_archivo)
    
    if df is None:
        print("No se pudo cargar el archivo. Verifique la ruta y el formato.")
        return
    
    # Limpiar datos
    df_clean = limpiar_datos(df)
    
    # Generar diccionario de datos
    diccionario_datos = generar_diccionario_datos(df_clean)
    
    # Generar lista de ciudades normalizadas
    ciudades_normalizadas = generar_ciudades_normalizadas()  # CORREGIDO: nombre correcto de la función
    
    # Guardar resultados
    ruta_csv = config['output_data_dir'] / "datos_limpios.csv"
    ruta_excel = config['output_data_dir'] / "datos_limpios.xlsx"
    ruta_diccionario = config['output_data_dir'] / "diccionario_datos.csv"
    ruta_ciudades = config['output_data_dir'] / "ciudades_normalizadas.csv"
    
    df_clean.to_csv(ruta_csv, index=False, encoding='utf-8')
    df_clean.to_excel(ruta_excel, index=False)
    diccionario_datos.to_csv(ruta_diccionario, index=False, encoding='utf-8')
    ciudades_normalizadas.to_csv(ruta_ciudades, index=False, encoding='utf-8')
    
    print("\n" + "=" * 60)
    print("RESULTADOS DE LA LIMPIEZA")
    print("=" * 60)
    print(f"Registros originales: {len(df)}")
    print(f"Registros después de limpieza: {len(df_clean)}")
    print(f"Columnas procesadas: {len(df_clean.columns)}")
    print("\nArchivos generados:")
    print(f"- Datos limpios (CSV): {ruta_csv}")
    print(f"- Datos limpios (Excel): {ruta_excel}")
    print(f"- Diccionario de datos: {ruta_diccionario}")
    print(f"- Ciudades normalizadas: {ruta_ciudades}")
    
    # Mostrar resumen de calidad de datos
    print("\n" + "=" * 60)
    print("MÉTRICAS DE CALIDAD DE DATOS")
    print("=" * 60)
    
    # Calcular métricas
    total_registros = len(df_clean)
    
    # Porcentaje de valores nulos por columna
    nulos_por_columna = (df_clean.isnull().sum() / total_registros * 100).round(2)
    
    print("\nPorcentaje de valores nulos por columna:")
    for columna, porcentaje in nulos_por_columna.items():
        print(f"- {columna}: {porcentaje}%")
    
    # Validar teléfonos
    telefonos_validos = df_clean['Telefono_Act1'].apply(lambda x: x is not np.nan and len(str(x)) == 10).sum()
    porcentaje_telefonos_validos = (telefonos_validos / total_registros * 100).round(2)
    print(f"\nTeléfonos válidos: {porcentaje_telefonos_validos}%")
    
    # Validar códigos DANE
    dane_validos = df_clean['CodDANE'].apply(lambda x: x is not np.nan and len(str(x)) == 8).sum()
    porcentaje_dane_validos = (dane_validos / total_registros * 100).round(2)
    print(f"Códigos DANE válidos: {porcentaje_dane_validos}%")
    
    print("\n¡Proceso completado exitosamente!")

if __name__ == "__main__":
    main()