# 🖥️ AI Knowledge Explorer — Frontend

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-005571?style=for-the-badge&logo=python&logoColor=white)

Interfaz de usuario moderna y reactiva construida con **Streamlit** para interactuar con la API del proyecto [AI Knowledge Explorer Backend](https://github.com/juaceballosfi/ai-explorer-backend). Proporciona un entorno visual para gestionar documentos, solicitar análisis inteligentes estructurados y entablar una conversación interactiva con el contenido mediante un asistente de inteligencia artificial.

---

## ✨ Características Principales

- **📂 Carga Múltiple de Documentos:** Sube fácilmente uno o varios archivos de texto hacia la API backend en un solo paso.
- **📊 Lista de Documentos en Tiempo Real:** Visualiza rápidamente los documentos almacenados en la base de datos centralizada.
- **🧠 Dashboard de Análisis Estructurado:** Observa de manera clara el resumen, palabras clave, categorías y posibles Q&A generadas por el modelo de razonamiento.
- **💬 Interfaz de Chat Estilo Mensajería:** Interactúa con el contexto del documento mediante un chat visual que carga el historial desde el backend automáticamente.
- **🔒 Integración Segura:** Todas las peticiones al backend viajan autenticadas a través de una API Key configurada globalmente.

---

## 🏗️ Estructura del Proyecto

```text
├── app.py                 # Punto de entrada y página principal (Subida de archivos y listado).
├── api_client.py          # Cliente HTTP centralizado. Orquesta las peticiones al backend e inyecta headers.
├── pages/
│   └── 1_Detalle.py       # Vista específica por documento. Muestra análisis estructurado y la interfaz de chat.
├── requirements.txt       # Dependencias de Python necesarias.
├── .env.example           # Plantilla de variables de entorno.
└── README.md              # Documentación del proyecto.
```

---

## 📋 Requisitos Previos

- **Python 3.8+**
- El proyecto backend (`ai-explorer-api`) en ejecución (local o remoto).

---

## ⚙️ Configuración del Entorno

1. **Clonar y Acceder:**
   ```bash
   cd ai-explorer-frontend
   ```

2. **Variables de Entorno (`.env`):**
   Copia el archivo `.env.example` a `.env` y configura lo siguiente:

   ```env
   # URL base del backend (Sin / al final). Ej: http://localhost:8000 o https://apps.fi-group.com/...
   API_BASE_URL=http://localhost:8000
   
   # API Key de seguridad que debe ser idéntica a la configurada en tu backend
   AI_EXPLORER_API_KEY=tu_api_key_secreta_configurada_en_el_backend
   ```

3. **Instalar Dependencias:**
   Es muy recomendable usar un entorno virtual:
   ```bash
   python -m venv venv
   
   # Activar en Windows:
   venv\Scripts\activate
   # Activar en Linux/macOS:
   # source venv/bin/activate
   
   pip install -r requirements.txt
   ```

---

## 🚀 Ejecución en Local

Para levantar la interfaz de usuario en modo desarrollo:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador por defecto (usualmente en `http://localhost:8501`).

---

## ☁️ Despliegue en Fi Apps

La aplicación está preparada para ser desplegada como una plantilla estándar de Streamlit:
1. Conecta este repositorio mediante **git-sync**.
2. En la configuración de la aplicación dentro de Fi Apps, establece el punto de entrada como `app.py`.
3. Inyecta `API_BASE_URL` y `AI_EXPLORER_API_KEY` directamente como Variables de Entorno desde el panel de control de despliegue.
