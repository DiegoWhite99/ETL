import pandas as pd

# ==================================================
# 1. Cargar archivo original
# ==================================================
ruta = r"D:\Documents\Diego 2025\Aca BI\BD.xlsx"
df = pd.read_excel(ruta)

print("📂 Archivo cargado correctamente")
print("➡️ Filas iniciales:", len(df))
print("➡️ Columnas:", list(df.columns))

# ==================================================
# 2. Limpieza básica de columnas
# ==================================================
# Quitar espacios en nombres de columnas
df.columns = df.columns.str.strip()

# Poner nombres en minúsculas
df.columns = df.columns.str.lower()

# ==================================================
# 3. Eliminar duplicados y valores nulos
# ==================================================
df = df.drop_duplicates()
df = df.dropna(how="all")
df = df.fillna("SinDato")

print("✅ Duplicados y vacíos eliminados")

# ==================================================
# 4. Estandarizar texto y formatos
# ==================================================
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].astype(str).str.strip().str.lower()

# Estandarizar fechas (ejemplo: columna 'fecha_nacimiento')
if "fecha_nacimiento" in df.columns:
    df["fecha_nacimiento"] = pd.to_datetime(df["fecha_nacimiento"], errors="coerce").dt.date

# Intentar convertir columnas a número si es posible
for col in df.columns:
    if df[col].dtype == "object":
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

print("✅ Formatos de texto, fechas y números estandarizados")

# ==================================================
# 5. Correcciones específicas solicitadas
# ==================================================
# Corrección de ciudades
if "ciudad_act" in df.columns:
    correcciones_ciudad = {
        "vogotá": "bogotá",
        "bogota%%": "bogotá",
        "bogota": "bogotá",
        "santiagho de caly": "santiago de cali",
        "medellin": "medellín",
        "barranquila": "barranquilla"
    }
    df["ciudad_act"] = df["ciudad_act"].replace(correcciones_ciudad)

# CodDANE a entero
if "coddane" in df.columns:
    df["coddane"] = pd.to_numeric(df["coddane"], errors="coerce").fillna(0).astype(int)

# Teléfono como texto (sin decimales)
if "telefono" in df.columns:
    df["telefono"] = df["telefono"].astype(str).str.replace(".0", "", regex=False)

print("✅ Correcciones específicas aplicadas (ciudad, CodDANE, teléfono)")

# ==================================================
# 6. Validación de campos obligatorios
# ==================================================
columnas_obligatorias = ["nombre", "apellido", "matricula"]

for col in columnas_obligatorias:
    if col in df.columns:
        faltantes = df[df[col].isin(["", "SinDato"])]
        if not faltantes.empty:
            print(f"⚠️ Registros incompletos en columna '{col}': {len(faltantes)}")
        else:
            print(f"✅ Columna '{col}' completa")

# ==================================================
# 7. Guardar archivo limpio
# ==================================================
ruta_final = r"D:\Documents\Diego 2025\Aca BI\BD_Limpio.xlsx"
df.to_excel(ruta_final, index=False)
print("\n📊 Archivo limpio generado:", ruta_final)

# ==================================================
# 8. Crear diccionario de datos
# ==================================================
diccionario = pd.DataFrame({
    "columna": df.columns,
    "tipo_dato": [str(df[col].dtype) for col in df.columns],
    "descripcion": ["Por definir"] * len(df.columns),
    "regla_limpieza": ["Estandarizada en Sprint 1"] * len(df.columns)
})

ruta_dicc = r"D:\Documents\Diego 2025\Aca BI\Diccionario_Datos.xlsx"
diccionario.to_excel(ruta_dicc, index=False)
print("📘 Diccionario de datos actualizado:", ruta_dicc)

print("\n==================================================")
print("✅ PROCESO DE LIMPIEZA FINALIZADO CORRECTAMENTE ✅")
print("==================================================")
