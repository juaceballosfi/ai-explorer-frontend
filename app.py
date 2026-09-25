"""
Módulo Principal de la Aplicación Frontend.

Este script sirve como punto de entrada para la aplicación web basada en Streamlit.
Presenta la interfaz de usuario principal que permite:
1. Subir nuevos documentos de texto al backend.
2. Visualizar la lista de documentos previamente subidos.
3. Navegar hacia la vista de detalle y análisis de un documento específico.
"""

import streamlit as st
from api_client import list_documents, upload_document

st.set_page_config(page_title="AI Knowledge Explorer", layout="wide")

st.title("AI Knowledge Explorer")

# --- SECCIÓN: SUBIDA DE DOCUMENTOS ---
st.subheader("Subir documentos")

# Componente para carga múltiple de archivos de texto
archivos = st.file_uploader(
    "Selecciona uno o varios archivos de texto",
    type=["txt"],
    accept_multiple_files=True,
)

if archivos:
    if st.button("Subir"):
        # Procesar cada archivo seleccionado individualmente
        for archivo in archivos:
            try:
                resultado = upload_document(archivo)
                st.success(f"Documento '{resultado['name']}' subido exitosamente (ID: {resultado['id']})")
            except Exception as e:
                st.error(f"Error al subir el documento '{archivo.name}': {e}")
        # Recargar la página para actualizar la lista de documentos
        st.rerun()

st.divider()

# --- SECCIÓN: LISTADO DE DOCUMENTOS ---
st.subheader("Documentos subidos")

# Obtener los documentos almacenados en el backend
try:
    documentos = list_documents()
except Exception as e:
    st.error(f"No se pudo establecer conexión con la API del backend: {e}")
    documentos = []

if not documentos:
    st.info("No hay documentos subidos en este momento.")
else:
    # Mostrar cada documento en una fila con su nombre, tamaño y botón de acceso
    for doc in documentos:
        col1, col2, col3 = st.columns([4, 2, 1])
        col1.write(doc["name"])
        col2.write(f"{doc['size']} bytes")
        
        # Almacenar los datos en la sesión y redirigir a la vista de detalle
        if col3.button("Abrir", key=f"abrir_{doc['id']}"):
            st.session_state["doc_id"] = doc["id"]
            st.session_state["doc_name"] = doc["name"]
            st.switch_page("pages/1_Detalle.py")
