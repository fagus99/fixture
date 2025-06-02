import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="📊 Visualizador de Predicciones", layout="wide")
st.title("📋 Predicciones Registradas")

FILE = "participaciones.csv"

if not os.path.exists(FILE):
    st.warning("Aún no hay predicciones registradas.")
    st.stop()

# Leer predicciones
df = pd.read_csv(FILE)

# Filtros
st.sidebar.header("🔍 Filtros")
correo = st.sidebar.text_input("Buscar por correo")
dni = st.sidebar.text_input("Buscar por DNI")

if correo:
    df = df[df["correo"].str.contains(correo, case=False)]
if dni:
    df = df[df["dni"].astype(str).str.contains(dni)]

# Mostrar datos
st.dataframe(df)

# Descargar
st.download_button(
    label="📥 Descargar como Excel",
    data=df.to_excel(index=False, engine='openpyxl'),
    file_name="participaciones.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
