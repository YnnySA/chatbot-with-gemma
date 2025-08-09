Chatbot Educativo — GGUF local (Gemma 2B)

Este proyecto implementa un asistente educativo en español utilizando modelos GGUF locales (como Gemma 2B) y una interfaz web con Streamlit. Está diseñado para funcionar sin conexión a internet y en equipos con recursos limitados.

Características:
- Interfaz tipo chat con historial visible.
- Botón para enviar consultas y otro para iniciar nuevo chat.
- Configuración ajustable desde la barra lateral (modelo, temperatura, contexto, etc.).
- Compatible con modelos GGUF vía llama.cpp.

Requisitos:
- Python 3.9 o superior.
- CPU con al menos 2 núcleos y 4 GB de RAM.
- Modelo GGUF descargado localmente (ej. gemma-2-2b-it-Q5_K_M.gguf).

Instalación:
1. Clona o copia este proyecto en tu equipo.
2. (Opcional pero recomendado) Crea un entorno virtual en la raíz del repositorio o en esta carpeta `chatbot_with_LlamaCpp/`:
   - En la raíz: `python -m venv streamlit_venv`
   - O en esta carpeta: `python -m venv streamlit_venv`
3. Activa el entorno virtual y instala dependencias:
   - Windows: `streamlit_venv\Scripts\python.exe -m pip install --upgrade pip wheel setuptools`
   - Windows: `streamlit_venv\Scripts\python.exe -m pip install -r requirements.txt`
4. Modelo GGUF:
   - Opción A (por defecto): coloca el modelo en `chatbot_with_LlamaCpp/models/` con nombre `gemma-2-2b-it-Q5_K_M.gguf`.
   - Opción B: define la variable de entorno `LLAMA_GGUF_PATH` con la ruta completa al `.gguf`.
   - Descarga sugerida: `https://huggingface.co/ironlanderl/gemma-2-2b-it-Q5_K_M-GGUF/resolve/main/gemma-2-2b-it-q5_k_m.gguf`

Ejecución (sin usar terminal):
- Doble clic en `chatbot_with_LlamaCpp/launcher.pyw`.
  - El lanzador detecta automáticamente un entorno virtual `streamlit_venv` en esta carpeta o en la carpeta padre. Si no existe, usará el Python del sistema.
  - Si faltan dependencias, mostrará instrucciones para instalarlas.

Ejecución (por terminal, alternativa):
1. Abre una terminal en esta carpeta `chatbot_with_LlamaCpp/`.
2. (Opcional) Activa tu entorno virtual.
3. Ejecuta: `streamlit run chatbot_gemma_st.py`

## Archivos grandes y uso local

Este proyecto utiliza modelos GGUF que no se incluyen en el repositorio por su tamaño. Para usar el chatbot localmente:

1. Descarga el modelo `gemma-2-2b-it-Q5_K_M.gguf` y colócalo en la carpeta `chatbot_with_LlamaCpp/models/`.
2. Alternativamente, define `LLAMA_GGUF_PATH` apuntando a la ruta completa del modelo.
3. El archivo del modelo está excluido del repositorio mediante `.gitignore`.


En caso de que LlamaCpp te dé problemas, prueba:
1. Instala "Microsoft C++ Build Tools" (Visual Studio Build Tools) en Windows.
2. En el entorno virtual ejecuta:
   - `python -m pip install --upgrade pip wheel setuptools`
   - `pip install "cmake>=3.27" --no-cache-dir`
   - `pip install llama-cpp-python --no-cache-dir --verbose`

Notas:
- Puedes recargar el modelo desde la barra lateral.
- Si usas una USB, incluye la carpeta `chatbot_with_LlamaCpp/models/` con el `.gguf`.
- La app también permite establecer la ruta del modelo desde la barra lateral.


Autor: Yenny Sánchez Aguilar (Proyecto educativo para entornos sin conexión con gemma)
