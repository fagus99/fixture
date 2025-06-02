
import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Mundial de Clubes 2025 - Quiniela", layout="wide")
st.title("⚽ Quiniela Mundial de Clubes 2025")

FIXTURE_FILE = "fixture_mundial_clubes_2025.xlsx"
if not os.path.exists(FIXTURE_FILE):
    st.error(f"No se encontró el archivo {FIXTURE_FILE}.")
    st.stop()

fixture_df = pd.read_excel(FIXTURE_FILE)

st.header("📝 Registro")
with st.form("registro_form"):
    correo = st.text_input("Correo electrónico")
    dni = st.text_input("DNI")
    submitted = st.form_submit_button("Registrarse")

    if submitted:
        if not correo or not dni:
            st.warning("Por favor, completa todos los campos.")
        else:
            PARTICIPACIONES_FILE = "participaciones.csv"
            if os.path.exists(PARTICIPACIONES_FILE):
                participaciones_df = pd.read_csv(PARTICIPACIONES_FILE)
                if ((participaciones_df["correo"] == correo) & (participaciones_df["dni"] == dni)).any():
                    st.error("Ya has participado.")
                    st.stop()
            else:
                participaciones_df = pd.DataFrame(columns=["correo", "dni"])

            st.success("Registro exitoso. Realiza tus predicciones.")
            st.header("📅 Predicciones")
            predicciones = []
            for _, row in fixture_df.iterrows():
                partido_id = row["ID"]
                local = row["Local"]
                visitante = row["Visitante"]
                fecha = row["Fecha"]
                hora = row["Hora"]
                estadio = row["Estadio"]

                st.subheader(f"{local} vs {visitante}")
                st.write(f"📅 {fecha} 🕒 {hora} 🏟️ {estadio}")

                resultado = st.radio(
                    f"¿Quién gana?", options=["Local", "Empate", "Visitante"],
                    key=f"pred_{partido_id}"
                )

                predicciones.append({
                    "correo": correo,
                    "dni": dni,
                    "partido_id": partido_id,
                    "fecha": fecha,
                    "hora": hora,
                    "local": local,
                    "visitante": visitante,
                    "estadio": estadio,
                    "prediccion": resultado,
                    "timestamp": datetime.now().isoformat()
                })

            if st.button("Enviar predicciones"):
                predicciones_df = pd.DataFrame(predicciones)
                if os.path.exists(PARTICIPACIONES_FILE):
                    predicciones_df.to_csv(PARTICIPACIONES_FILE, mode='a', header=False, index=False)
                else:
                    predicciones_df.to_csv(PARTICIPACIONES_FILE, index=False)
                st.success("¡Predicciones guardadas!")
                st.balloons()
