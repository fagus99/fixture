
import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Mundial de Clubes 2025 - Quiniela", layout="wide")
st.title("⚽ Quiniela Mundial de Clubes 2025")

FIXTURE_FILE = "fixture_mundial_clubes_2025.xlsx"
PARTICIPACIONES_FILE = "participaciones.csv"

# Cargar el fixture
if not os.path.exists(FIXTURE_FILE):
    st.error(f"No se encontró el archivo {FIXTURE_FILE}.")
    st.stop()
fixture_df = pd.read_excel(FIXTURE_FILE)

# === Formulario de registro ===
st.header("📝 Registro (valor del fixture: $10.000)")
with st.form("registro_form"):
    correo = st.text_input("Correo electrónico")
    dni = st.text_input("DNI")
    aceptar = st.checkbox("Acepto los términos y condiciones")
    registro_submit = st.form_submit_button("Registrarse")

    if registro_submit:
        if not correo or not dni or not aceptar:
            st.warning("Completa todos los campos y acepta los términos.")
            st.stop()
        else:
            if os.path.exists(PARTICIPACIONES_FILE):
                participaciones_df = pd.read_csv(PARTICIPACIONES_FILE)
                if ((participaciones_df["correo"] == correo) & (participaciones_df["dni"] == dni)).any():
                    st.error("Ya has participado.")
                    st.stop()
            else:
                participaciones_df = pd.DataFrame(columns=["correo", "dni"])

            st.success("Registro exitoso. Ahora puedes realizar tus predicciones.")

# === Formulario de predicciones ===
st.header("📅 Predicciones")
with st.form("predicciones_form"):
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

    predicciones_submit = st.form_submit_button("Guardar predicciones")

    if predicciones_submit:
        predicciones_df = pd.DataFrame(predicciones)
        if os.path.exists(PARTICIPACIONES_FILE):
            predicciones_df.to_csv(PARTICIPACIONES_FILE, mode='a', header=False, index=False)
        else:
            predicciones_df.to_csv(PARTICIPACIONES_FILE, index=False)
        st.success("✅ ¡Tus predicciones fueron guardadas con éxito! 🎉")
        st.info("¡Buena suerte!")
