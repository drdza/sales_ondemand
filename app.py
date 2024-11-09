import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de conexión al DWH
def connect_to_dwh():
    # Reemplaza con tus credenciales y detalles de conexión
    engine = create_engine("postgresql://usuario:contraseña@host:puerto/nombre_bd")
    return engine.connect()

# Función para cargar datos
def load_sales_data(query):
    conn = connect_to_dwh()
    data = pd.read_sql(query, conn)
    conn.close()
    return data

# Función principal de la aplicación
def main():
    st.title("Generador de Reportes de Ventas")
    
    # Parámetros de entrada del usuario
    st.sidebar.header("Parámetros de filtro")
    
    # Selección del cliente o grupo de clientes
    client_group = st.sidebar.selectbox("Seleccione Cliente o Grupo de Clientes", ["Cliente A", "Cliente B", "Grupo 1", "Grupo 2"])
    
    # Selección del periodo de tiempo
    date_option = st.sidebar.selectbox("Seleccione el Periodo", ["Mensual", "Trimestral", "Anual", "Personalizado"])
    
    if date_option == "Personalizado":
        start_date = st.sidebar.date_input("Fecha de inicio")
        end_date = st.sidebar.date_input("Fecha de fin")
    else:
        start_date, end_date = None, None  # Configurar estas fechas según la selección

    # Consultar datos en función de los parámetros
    query = f"""
        SELECT * FROM ventas 
        WHERE cliente_grupo = '{client_group}'
    """
    
    if start_date and end_date:
        query += f" AND fecha BETWEEN '{start_date}' AND '{end_date}'"
    
    # Cargar y mostrar los datos
    data = load_sales_data(query)
    st.write("Datos de Ventas", data)

    # Visualización de ventas por cliente
    if not data.empty:
        st.header("Visualización de Ventas")
        
        fig, ax = plt.subplots()
        sns.lineplot(data=data, x='fecha', y='ventas', hue='cliente', ax=ax)
        ax.set_title("Ventas por Cliente")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Ventas")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
