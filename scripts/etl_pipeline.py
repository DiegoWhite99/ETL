# =====================================================
# ETL Pipeline - Proyecto BPO (SCRUM + ABP)
# Autor: Diego Castelblanco
# =====================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# =====================================================
# 0. Configuración inicial
# =====================================================
# Carpeta base (ajústala si cambia tu proyecto)
base_dir = r"D:\Documents\Diego 2025\Aca BI"
data_path = os.path.join(base_dir, "data", "BD.xlsx")
outputs_path = os.path.join(base_dir, "outputs")

os.makedirs(outputs_path, exist_ok=True)

# =====================================================
# 1. Sprint 1 - Limpieza y Transformación
# =====================================================
df = pd.read_excel(data_path)
print("✅ Datos originales:", df.shape)

df_limpio = df.copy()
df_limpio = df_limpio.drop_duplicates()
df_limpio = df_limpio.dropna(how="all")

# Validar campos requeridos (ajusta si tienes otros)
campos_requeridos = ["NombresGerenteGeneral_Act", "ApellidosGerenteGeneral_Act"]
for col in campos_requeridos:
    if col in df_limpio.columns:
        df_limpio = df_limpio[df_limpio[col].notna()]

# Estandarizar strings
for col in df_limpio.select_dtypes(include="object").columns:
    df_limpio[col] = df_limpio[col].astype(str).str.strip().str.title()

# Guardar resultados
df_limpio.to_excel(os.path.join(outputs_path, "datos_limpios.xlsx"), index=False)

diccionario = pd.DataFrame({
    "Columna": df_limpio.columns,
    "Tipo_Dato": df_limpio.dtypes.astype(str),
    "Valores_Unicos": [df_limpio[col].nunique() for col in df_limpio.columns]
})
diccionario.to_excel(os.path.join(outputs_path, "diccionario_datos.xlsx"), index=False)

print("✅ Sprint 1 completado:", df_limpio.shape)

# =====================================================
# 2. Sprint 2 - Campos Calculados
# =====================================================
df_calc = df_limpio.copy()
np.random.seed(42)
df_calc["Horas_trabajadas"] = np.random.randint(1, 25, df_calc.shape[0])

df_calc["Pago_Base"] = (df_calc["Horas_trabajadas"] // 8) * 10000
df_calc["Pago_Extra"] = np.where(
    df_calc["Horas_trabajadas"] > 8,
    (df_calc["Horas_trabajadas"] - 8) * 5000,
    0
)
df_calc["Pago_Total"] = df_calc["Pago_Base"] + df_calc["Pago_Extra"]

df_calc.to_excel(os.path.join(outputs_path, "datos_calculados.xlsx"), index=False)
print("✅ Sprint 2 completado:", df_calc.shape)

# =====================================================
# 3. Sprint 3 - Análisis Exploratorio (EDA)
# =====================================================
# Ciudad con mayor Pago_Total acumulado
if "Ciudad" in df_calc.columns:
    ciudad_top = df_calc.groupby("Ciudad")["Pago_Total"].sum().idxmax()
    print("📊 Ciudad con mayor pago acumulado:", ciudad_top)

# Filtrar por nombre "Diego Castelblanco"
col_nombres = [c for c in df_calc.columns if "Nombre" in c or "Nombres" in c]
if col_nombres:
    reporte_diego = df_calc[
        df_calc[col_nombres[0]].str.contains("Diego", case=False, na=False)
    ]
    reporte_diego.to_excel(os.path.join(outputs_path, "reporte_diego.xlsx"), index=False)

# Visualización: Top 5 ciudades
if "Ciudad" in df_calc.columns:
    top_ciudades = (
        df_calc.groupby("Ciudad")["Pago_Total"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    plt.figure(figsize=(8, 5))
    sns.barplot(x=top_ciudades.values, y=top_ciudades.index, palette="viridis")
    plt.title("Top 5 ciudades por Pago Total")
    plt.xlabel("Pago Total")
    plt.ylabel("Ciudad")
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_path, "top_ciudades.png"))
    plt.close()

print("✅ Sprint 3 completado")

# =====================================================
# 4. Sprint 4 - ETL + Dashboard
# =====================================================
df_calc.to_csv(os.path.join(outputs_path, "datos_final.csv"), index=False)

if "Ciudad" in df_calc.columns:
    fig = px.bar(
        df_calc.groupby("Ciudad")["Pago_Total"].sum().reset_index(),
        x="Ciudad", y="Pago_Total",
        title="Pago Total por Ciudad",
        color="Pago_Total",
        text_auto=True
    )
    fig.write_html(os.path.join(outputs_path, "dashboard.html"))

print("✅ Sprint 4 completado – Pipeline finalizado 🎉")

