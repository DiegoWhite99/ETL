# conexion sqlserver
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# configuración
CONFIG = {
    'server': 'localhost\\SQLEXPRESS',  # ← Así se conecta a SQL Server Express
    'database': 'master',               # ← Usamos master por ahora
    'username': 'sa',                   # ← Usuario por defecto
    'password': '123456cun',            # ← CAMBIA ESTO por la password de la instalación
    'driver': 'ODBC Driver 17 for SQL Server'
}

def conectar_sqlserver():    
    print("🔌 Intentando conectar a SQL Server...")
    
    try:
        # Método 1: Conexión directa con pyodbc
        connection_string = f"""
            DRIVER={{{CONFIG['driver']}}};
            SERVER={CONFIG['server']};
            DATABASE={CONFIG['database']};
            UID={CONFIG['username']};
            PWD={CONFIG['password']};
            Trusted_Connection=no;
        """
        
        conn = pyodbc.connect(connection_string)
        print("✅ ¡CONEXIÓN EXITOSA con pyodbc!")
        return conn
        
    except Exception as e:
        print(f"❌ Error con pyodbc: {e}")
        print("⚠️  Probando método alternativo...")
        
        try:
            # Método 2: Conexión con SQLAlchemy
            connection_string = (
                f"mssql+pyodbc://{CONFIG['username']}:{quote_plus(CONFIG['password'])}"
                f"@{CONFIG['server']}/{CONFIG['database']}?"
                f"driver={CONFIG['driver'].replace(' ', '+')}"
            )
            
            engine = create_engine(connection_string)
            conn = engine.connect()
            print("✅ ¡CONEXIÓN EXITOSA con SQLAlchemy!")
            return conn
            
        except Exception as e2:
            print(f"❌ Error con SQLAlchemy: {e2}")
            return None

def probar_conexion():
    """Probar la conexión y mostrar información"""
    conn = conectar_sqlserver()   # ✅ ahora sí llamamos a la correcta
    
    if conn:
        try:
            print("\n" + "="*50)
            print("📊 INFORMACIÓN DE LA CONEXIÓN")
            print("="*50)
            
            # Ejecutar una consulta simple
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION as version")
            version = cursor.fetchone()
            
            print(f"✅ Versión de SQL Server: {version[0]}")
            print("✅ Conexión establecida correctamente!")
            
            # Cerrar conexión
            conn.close()
            print("✅ Conexión cerrada correctamente")
            
        except Exception as e:
            print(f"❌ Error en la consulta: {e}")
    else:
        print("\n" + "="*50)
        print("❌ NO SE PUDO CONECTAR")
        print("="*50)
        print("💡 Posibles soluciones:")
        print("1. Verifica que SQL Server esté ejecutándose")
        print("2. Revisa la contraseña en el código")
        print("3. Asegúrate de tener el ODBC Driver instalado")
        print("4. Prueba reiniciar SQL Server")

# Ejecutar la prueba
if __name__ == "__main__":
    probar_conexion()
