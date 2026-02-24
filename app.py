import streamlit as st
import pandas as pd
import requests

# --- CONFIGURACIÓN DEL FORMULARIO ---
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd34CrtzbRvU-hQXG5SIrD5mrDhIbCG6H0I7DxUomb5E5ektA/formResponse"

ENTRY_NOMBRE = "entry.1513057760" 
ENTRY_MATERIAS = "entry.368515193"
ENTRY_HORARIOS = "entry.1222451054"

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Liceo IEP - Horarios", page_icon="📅", layout="wide")

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("📅 Selección Disponibilidad de Horas Liceo IEP")
st.info("ℹ️ **Nota importante:** Las horas seleccionadas son las que tiene disponible para ser asignadas.")
st.markdown("---")

# 1. Interfaz de usuario
nombre = st.text_input("Nombre y Apellido *")
materias_lista = ["Matemáticas", "Lengua", "Historia", "Física", "Química", "Inglés", "Biología", "Informática"]
materias_profe = st.multiselect("Asignaturas que dicta en el Liceo *", materias_lista)

# 2. Grilla de Horarios (8:00 a 15:00 cada 45 min)
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
horas_labels = []
h, m = 8, 0
while h < 15:
    inicio = f"{h:02d}:{m:02d}"
    m += 45
    if m >= 60: h += 1; m -= 60
    fin = f"{h:02d}:{m:02d}"
    horas_labels.append(f"{inicio} - {fin}")

df_horarios = pd.DataFrame(False, index=horas_labels, columns=dias)

st.subheader("Seleccione sus bloques de disponibilidad")
grid_editable = st.data_editor(
    df_horarios, 
    column_config={dia: st.column_config.CheckboxColumn() for dia in dias},
    use_container_width=True
)

# 3. Envío de datos
if st.button("Confirmar y Enviar Disponibilidad"):
    if not nombre or not materias_profe:
        st.error("❌ Por favor, complete su nombre y seleccione al menos una asignatura.")
    else:
        seleccionados = [f"{d} ({h})" for d in dias for h in horas_labels if grid_editable.loc[h, d]]
        
        if not seleccionados:
            st.warning("⚠️ Debe seleccionar al menos un bloque horario.")
        else:
            datos_form = {
                ENTRY_NOMBRE: nombre,
                ENTRY_MATERIAS: ", ".join(materias_profe),
                ENTRY_HORARIOS: " | ".join(seleccionados)
            }
            
            try:
                respuesta = requests.post(FORM_URL, data=datos_form)
                if respuesta.status_code == 200:
                    st.success(f"✅ ¡Muchas gracias, {nombre}! Su disponibilidad ha sido enviada con éxito.")
                    st.balloons()
                else:
                    st.error("Hubo un error al conectar con el servidor. Intente nuevamente.")
            except Exception as e:
                st.error(f"Error de conexión: {e}")