# Proyecto de Business Intelligence - Empresas Colombianas

## 📊 Descripción del Proyecto

Sistema integral de Business Intelligence para el análisis, limpieza y visualización de datos de empresas colombianas. El proyecto transforma datos crudos en información valiosa mediante un proceso estructurado de 3 fases.

## 🎯 Objetivos

- Limpiar y estandarizar datos empresariales
- Realizar análisis exploratorio avanzado
- Integrar con fuentes de datos externas
- Crear dashboards interactivos
- Implementar sistema de monitorización de calidad

## 🏗️ Estructura del Proyecto
proyecto_bi_empresas/
│
├── data/
│ ├── raw/ # Datos originales (BD.xlsx)
│ ├── processed/ # Datos procesados
│ └── output/ # Resultados finales
│
├── database/ # Base de datos SQLite
├── dashboards/ # Dashboards interactivos
├── reports/ # Reportes de análisis
├── src/ # Código fuente
│ ├── fase1_limpieza.py
│ ├── fase2_analisis.py
│ └── fase3_integracion.py
│
├── requirements.txt # Dependencias
└── README.md # Documentación

text

## 📋 Prerrequisitos

- Python 3.8+
- pip (gestor de paquetes de Python)
- Git (opcional)

## 🚀 Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone <url-del-repositorio>
   cd proyecto_bi_empresas
Crear entorno virtual (recomendado)

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
Instalar dependencias

bash
pip install -r requirements.txt
Colocar los datos iniciales

Copiar el archivo BD.xlsx a la carpeta data/raw/

🎮 Uso del Proyecto
Ejecución secuencial de las fases:
bash
# Fase 1 - Limpieza de datos
python src/fase1_limpieza.py

# Fase 2 - Análisis y enriquecimiento
python src/fase2_analisis.py

# Fase 3 - Integración y dashboard
python src/fase3_integracion.py
Ejecutar la aplicación web:
bash
streamlit run dashboards/app_empresas.py
📊 Entregables Generados
Fase 1 - Limpieza:
datos_limpios.csv - Datos normalizados

diccionario_datos.csv - Metadatos de los campos

ciudades_normalizadas.csv - Catálogo de ciudades

Fase 2 - Análisis:
datos_enriquecidos.csv - Datos con información adicional

Reportes de análisis (JSON y TXT)

Visualizaciones estáticas

Fase 3 - Integración:
datos_integrados.csv - Datos con fuentes externas

empresas_colombia.db - Base de datos SQLite

Dashboards interactivos (HTML)

Aplicación Streamlit

Sistema de monitorización

🛠️ Tecnologías Utilizadas
Python: Lenguaje principal

Pandas: Manipulación de datos

Plotly: Visualizaciones interactivas

Streamlit: Aplicación web

SQLAlchemy: Base de datos

Matplotlib/Seaborn: Visualizaciones estáticas

📈 Características Principales
🔧 Limpieza de Datos
Normalización de textos y formatos

Corrección de nombres de ciudades

Validación de teléfonos y códigos DANE

Eliminación de duplicados

📊 Análisis Avanzado
Análisis exploratorio (EDA)

Enriquecimiento con datos externos

Cálculo de métricas de calidad

Clasificación por riesgo

🎨 Visualización
Dashboards interactivos

Gráficos dinámicos

Métricas en tiempo real

Filtros personalizables

📋 Monitorización
Sistema de alertas de calidad

Reportes automáticos

Indicadores de desempeño

Detección de anomalías

🚦 Flujo de Trabajo
Carga: Datos crudos en Excel

Limpieza: Normalización y validación

Análisis: Exploración y enriquecimiento

Integración: Fuentes externas y BD

Visualización: Dashboards interactivos

Monitorización: Control de calidad continuo

🔮 Próximas Mejoras
Integración con APIs reales

Machine Learning para predicción de riesgo

Sistema de alertas en tiempo real

Panel de administración web

Exportación a múltiples formatos

Autenticación de usuarios

🤝 Contribución
Fork del proyecto

Crear rama para feature (git checkout -b feature/AmazingFeature)

Commit de cambios (git commit -m 'Add AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abrir Pull Request

📝 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

🆘 Soporte
Si encuentras algún problema o tienes preguntas:

Revisar la documentación

Buscar en issues existentes

Crear un nuevo issue con:

Descripción del problema

Pasos para reproducir

Capturas de pantalla (si aplica)

🎉 Reconocimientos
Datos proporcionados por [Nombre de la organización]

Equipo de desarrollo de Business Intelligence

Comunidad de Python por las librerías utilizadas

¡Este proyecto transforma datos en insights valiosos para la toma de decisiones empresariales! 🚀

text

## Instrucciones de uso:

1. **Guarda el archivo `requirements.txt`** en la raíz de tu proyecto
2. **Guarda el archivo `README.md`** en la raíz de tu proyecto
3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
Sigue las instrucciones del README para ejecutar el proyecto

El requirements.txt contiene todas las librerías necesarias para que el proyecto funcione correctamente, y el README.md proporciona documentación completa para cualquier persona que quiera usar o contribuir al proyecto.
