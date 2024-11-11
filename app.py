import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

# Configuración inicial de la aplicación
st.title("Carga de Datos y Validación para DWH")
st.write("Sube tus datos en Excel y realiza una validación previa antes de la carga.")

# Paso 1: Seleccionar el tipo de plantilla de datos
plantillas = {
    "Ventas": ["Fecha", "Producto", "Cantidad", "Precio"],
    "Inventario": ["ID", "Producto", "Stock", "Ubicación"],
    "Clientes": ["ClienteID", "Nombre", "Email", "Teléfono"]
}

# Selección de plantilla
tipo_dato = st.selectbox("Selecciona el tipo de información que deseas cargar:", list(plantillas.keys()))
campos_esperados = plantillas[tipo_dato]

# Subir archivo de datos
uploaded_file = st.file_uploader("Sube tu archivo Excel", type="xlsx")

if uploaded_file:
    # Cargar el archivo en un DataFrame
    datos_usuario = pd.read_excel(uploaded_file)
    st.write("Vista previa de los datos cargados:")
    st.write(datos_usuario.head())

    # Paso 2: Validación de columnas
    columnas_usuario = datos_usuario.columns.tolist()
    columnas_faltantes = [col for col in campos_esperados if col not in columnas_usuario]

    if columnas_faltantes:
        st.warning(f"Tu archivo está incompleto. Faltan las columnas: {', '.join(columnas_faltantes)}.")
    else:
        # Paso 3: Limpieza básica de datos
        datos_limpios = datos_usuario.copy()
        
        # Ejemplo de limpieza de datos según tipo de plantilla
        if tipo_dato == "Ventas":
            datos_limpios["Fecha"] = pd.to_datetime(datos_limpios["Fecha"], errors="coerce")
            datos_limpios["Cantidad"] = pd.to_numeric(datos_limpios["Cantidad"], errors="coerce").fillna(0)
            datos_limpios["Precio"] = pd.to_numeric(datos_limpios["Precio"], errors="coerce").fillna(0)
        
        elif tipo_dato == "Inventario":
            datos_limpios["Stock"] = pd.to_numeric(datos_limpios["Stock"], errors="coerce").fillna(0)

        elif tipo_dato == "Clientes":
            datos_limpios["Email"] = datos_limpios["Email"].str.lower()
        
        # Paso 4: Comparación de datos
        st.write("Comparativa de datos originales vs. datos limpiados")
        st.write("Datos originales:")
        st.write(datos_usuario.head())
        st.write("Datos limpiados:")
        st.write(datos_limpios.head())

        # Visualización de datos inválidos
        st.write("Datos potencialmente inválidos:")
        datos_invalidos = datos_usuario[datos_usuario.isnull().any(axis=1)]
        if not datos_invalidos.empty:
            st.write(datos_invalidos)
        else:
            st.write("No se encontraron datos inválidos.")

        # Paso 5: Confirmación de carga
        if st.button("Confirmar y cargar datos al DWH"):
            # Función ficticia para cargar al DWH (reemplazar con lógica real)
            st.success("Datos cargados exitosamente al DWH.")
