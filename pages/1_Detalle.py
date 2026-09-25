"""
Módulo de Detalle y Análisis de Documento.

Esta página de Streamlit muestra la información detallada de un documento seleccionado.
Permite a los usuarios:
1. Visualizar el análisis estructurado generado por el LLM (Resumen, Categoría, Keywords, Q&A).
2. Solicitar la generación de un nuevo análisis si el documento no lo posee.
3. Mantener una conversación interactiva (chat) con el contexto del documento.
"""

import streamlit as st
from api_client import analyze_document, get_analysis, get_chat_history, send_chat_message

st.set_page_config(page_title="Detalle del documento", layout="wide")

# --- VALIDACIÓN DE ESTADO ---
# Redirigir al inicio si no se ha seleccionado un documento en la sesión actual
if "doc_id" not in st.session_state:
    st.warning("Por favor selecciona un documento desde la página principal primero.")
    st.stop()

doc_id = st.session_state["doc_id"]
doc_name = st.session_state["doc_name"]

st.title(doc_name)

if st.button("← Volver a la lista"):
    st.switch_page("app.py")

# --- SECCIÓN: ANÁLISIS ESTRUCTURADO ---
st.subheader("Análisis del Documento")

# Intentar recuperar el análisis previo del documento desde la API
try:
    analisis = get_analysis(doc_id)
except Exception:
    analisis = None

if analisis:
    st.write("**Resumen Ejecutivo:**", analisis["resumen"])
    st.write("**Categoría:**", analisis["categoria"])
    st.write("**Palabras Clave:**", ", ".join(analisis["keywords"]))
    
    with st.expander("Preguntas y Respuestas (Q&A)"):
        for pr in analisis["preguntas_respuestas"]:
            st.markdown(f"**P: {pr['pregunta']}**")
            st.write(f"R: {pr['respuesta']}")
else:
    st.info("Este documento todavía no ha sido procesado ni analizado.")
    # Botón para iniciar el análisis LLM bajo demanda
    if st.button("Analizar ahora"):
        with st.spinner("Ejecutando modelo de lenguaje para extraer información..."):
            try:
                analyze_document(doc_id)
                st.rerun()
            except Exception as e:
                st.error(f"Se produjo un error al analizar el documento: {e}")

st.divider()

# --- SECCIÓN: CHAT INTERACTIVO ---
st.subheader("Conversación con el Documento")

# Obtener y renderizar el historial de mensajes persistido en la base de datos
try:
    historial = get_chat_history(doc_id)
except Exception as e:
    st.error(f"No se pudo cargar el historial de chat: {e}")
    historial = []

for mensaje in historial:
    with st.chat_message(mensaje["role"]):
        st.write(mensaje["content"])

# Input de usuario para enviar nuevas consultas
pregunta = st.chat_input("Escribe tu pregunta sobre el contenido de este documento...")

if pregunta:
    # Renderizar el mensaje del usuario inmediatamente
    with st.chat_message("user"):
        st.write(pregunta)

    # Solicitar la respuesta al asistente virtual a través de la API
    with st.chat_message("assistant"):
        with st.spinner("Consultando el contexto y redactando respuesta..."):
            try:
                respuesta = send_chat_message(doc_id, pregunta)
                st.write(respuesta["respuesta"])
            except Exception as e:
                st.error(f"Hubo un error al comunicarse con el asistente: {e}")

    # Recargar la interfaz para actualizar el historial correctamente
    st.rerun()
