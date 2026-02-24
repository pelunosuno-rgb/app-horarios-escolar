import streamlit as st
import pandas as pd
import requests

# --- CONFIGURACIÓN DEL FORMULARIO ---
# Cambiado /viewform por /formResponse
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd34CrtzbRvU-hQXG5SIrD5mrDhIbCG6H0I7DxUomb5E5ektA/formResponse"

# IDs de las preguntas (Verifica que no tengan espacios extra al final)
ENTRY_NOMBRE = "entry.1513057760" 
ENTRY_MATERIAS = "entry.368515193"
ENTRY_HORARIOS = "entry.1222451054"

st.title("📅 Sistema de Horarios (Vía Google)")

# 1. Interfaz de usuario
nombre = st.text_input("Nombre y Apellido *")
materias_lista = ["Matemáticas", "Lengua", "Historia", "Física"]
materias_profe = st.multiselect("Asignaturas *", materias_lista)

# 2. Grilla de Horarios
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
horas = [f"{h:02d}:00" for h in range(8, 15)]
df_horarios = pd.DataFrame(False, index=horas, columns=dias)

st.subheader("Seleccione su disponibilidad")
grid_editable = st.data_editor(df_horarios, use_container_width=True)

# 3. Envío de datos
if st.button("Enviar Disponibilidad"):
    if not nombre or not materias_profe:
        st.error("❌ Completa los campos obligatorios.")
    else:
        # Extraer seleccionados de forma limpia
        seleccionados = []
        for d in dias:
            for h in horas:
                if grid_editable.loc[h, d]:
                    seleccionados.append(f"{d} {h}")
        
        if not seleccionados:
            st.warning("⚠️ No seleccionaste ningún horario.")
        else:
            # PREPARAR DATOS
            datos_form = {
                ENTRY_NOMBRE: nombre,
                ENTRY_MATERIAS: ", ".join(materias_profe),
                ENTRY_HORARIOS: " | ".join(seleccionados)
            }
            
            # ENVIAR USANDO POST
            try:
                # Importante: Google Forms espera un posteo de formulario estándar
                respuesta = requests.post(FORM_URL, data=datos_form)
                
                # Google devuelve 200 aunque los IDs estén mal, 
                # pero si la URL es /formResponse, debería funcionar.
                if respuesta.status_code == 200:
                    st.success("✅ ¡Datos enviados correctamente!")
                    st.balloons()
                else:
                    st.error(f"Error {respuesta.status_code}: No se pudo enviar.")
            except Exception as e:
                st.error(f"Error de conexión: {e}")