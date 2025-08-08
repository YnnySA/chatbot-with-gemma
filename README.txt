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
1. Clona o copia este proyecto en tu equipo, crea en la raiz del directorio del proyecto una carpeta models.
2. Coloca el modelo GGUF en la carpeta `models/` o define la variable de entorno `LLAMA_GGUF_PATH`.
link de descarga del modelo: https://huggingface.co/ironlanderl/gemma-2-2b-it-Q5_K_M-GGUF/resolve/main/gemma-2-2b-it-q5_k_m.gguf
3. Instala las dependencias:
   pip install -r requirements.txt
4. Ejecuta la aplicación:
   streamlit run chatbot_gemma_st.py

## Archivos grandes y uso local

Este proyecto utiliza modelos GGUF que no se incluyen en el repositorio por su tamaño. Para usar el chatbot localmente:

1. Descarga el modelo `gemma-2-2b-it-Q5_K_M.gguf` y colócalo en la carpeta `models/`.
2. El archivo está excluido del repositorio mediante `.gitignore` para facilitar la subida en entornos con conexión limitada.


En caso de que LlamaCpp te dé problemas sigue estas instrucciones para instalarlo:
1. Asegúrate de tener instalado Visual Studio Tool para el manejo de los binarios precomplilados (o algo así, jjjj)
2. En el entorno virtual de trabajo del proyecto ejecuta: 
    ''python -m install --upgrade pip wheel setuptools''
3. pip install "cmake>=3.27" --no-cache-dir
4. pip install llama-cpp-python --no-cache-dir --verbose

Notas:
- Puedes recargar el modelo desde la barra lateral.
- Si usas una USB, asegúrate de que el modelo esté incluido en la carpeta `models/`.


Autor: Yenny Sánchez Aguilar (Proyecto educativo para entornos sin conexión)
