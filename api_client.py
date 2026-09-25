"""
Cliente HTTP Centralizado para AI Knowledge Explorer.

Este módulo encapsula todas las interacciones de red entre el frontend (Streamlit) 
y el backend (FastAPI). Centralizar las peticiones HTTP aquí evita redundancia de 
código, unifica el manejo de la URL base y automatiza la inyección de la cabecera 
de autenticación (`x-api-key`) en cada solicitud de forma segura.
"""
from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("AI_EXPLORER_API_KEY")

HEADERS = {"x-api-key": API_KEY}


def list_documents() -> list[dict]:
    """
    Obtiene la lista de todos los documentos disponibles en el backend.
    
    Returns:
        list[dict]: Una lista de diccionarios con metadatos de documentos.
    """
    response = requests.get(f"{API_BASE_URL}/documents", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def upload_document(file) -> dict:
    """
    Sube un archivo de texto al backend para ser procesado.
    
    Args:
        file: Un objeto de archivo subido a través de st.file_uploader.
        
    Returns:
        dict: Metadatos del archivo subido (incluyendo su ID).
    """
    files = {"file": (file.name, file.getvalue(), file.type)}
    response = requests.post(f"{API_BASE_URL}/documents/upload", headers=HEADERS, files=files, timeout=30)
    response.raise_for_status()
    return response.json()


def analyze_document(doc_id: int) -> dict:
    """
    Desencadena el análisis estructurado (LLM) de un documento en el backend.
    
    Args:
        doc_id (int): ID del documento a analizar.
        
    Returns:
        dict: Resultado del análisis.
    """
    response = requests.post(f"{API_BASE_URL}/documents/{doc_id}/analyze", headers=HEADERS, timeout=60)
    response.raise_for_status()
    return response.json()


def get_analysis(doc_id: int) -> dict:
    """
    Recupera el análisis estructurado previamente generado para un documento.
    
    Args:
        doc_id (int): ID del documento.
        
    Returns:
        dict: El JSON del análisis (resumen, keywords, etc.).
    """
    response = requests.get(f"{API_BASE_URL}/documents/{doc_id}/analysis", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_chat_history(doc_id: int) -> list[dict]:
    """
    Obtiene el historial de chat persistido para un documento específico.
    
    Args:
        doc_id (int): ID del documento.
        
    Returns:
        list[dict]: Lista de mensajes del chat.
    """
    response = requests.get(f"{API_BASE_URL}/documents/{doc_id}/chat", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def send_chat_message(doc_id: int, content: str) -> dict:
    """
    Envía un nuevo mensaje al chat contextual de un documento.
    
    Args:
        doc_id (int): ID del documento.
        content (str): La pregunta del usuario.
        
    Returns:
        dict: Respuesta generada por el asistente.
    """
    payload = {"role": "user", "content": content}
    response = requests.post(f"{API_BASE_URL}/documents/{doc_id}/chat", headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
