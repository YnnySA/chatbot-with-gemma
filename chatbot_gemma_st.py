#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import streamlit as st
from langchain_community.llms import LlamaCpp

# -------------------------------
# Configuración base y utilidades
# -------------------------------

# Ruta del modelo GGUF, configurable por variable de entorno o por defecto en carpeta 'models'
DEFAULT_MODEL_PATH = os.environ.get(
    "LLAMA_GGUF_PATH",
    os.path.join("models", "gemma-2-2b-it-Q5_K_M.gguf"),
)

# Prompt del sistema (igual que en tu script)
SYSTEM_PROMPT = (
    "Eres un asistente educativo útil y claro. Responde en español, "
    "con explicaciones breves y adaptadas a un nivel básico-intermedio.\n"
)

# Historial y construcción del prompt
def formatear_historial(history):
    """
    Convierte la lista de mensajes a un texto tipo chat con el formato:
    Usuario: ...
    Asistente: ...
    """
    partes = []
    for m in history:
        if m["role"] == "user":
            partes.append(f"Usuario: {m['content']}\n")
        elif m["role"] == "assistant":
            partes.append(f"Asistente: {m['content']}\n")
    return "".join(partes)

def construir_prompt(history, user_input):
    """
    Construye el prompt completo: system + historial + turno actual
    """
    historial_txt = formatear_historial(history)
    return f"{SYSTEM_PROMPT}{historial_txt}Usuario: {user_input}\nAsistente:"

# -----------------------------------
# Carga del modelo (cacheado)
# -----------------------------------

@st.cache_resource(show_spinner="Cargando modelo GGUF en memoria…")         #evita recargar el modelo en cada interacción. 
def get_llm(model_path: str,
            n_ctx: int,
            n_threads: int,
            n_batch: int,
            n_gpu_layers: int,
            f16_kv: bool,
            temperature: float,
            top_p: float,
            max_tokens: int,
            cache_bust: int = 0) -> LlamaCpp:
    """
    Carga y devuelve una instancia de LlamaCpp cacheada por Streamlit.
    cache_bust permite forzar recarga al cambiar parámetros.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No se encontró el modelo en: {model_path}")

    # Inicializa con tu misma configuración base (ajustable desde la UI)
    return LlamaCpp(
        model_path=model_path,
        n_ctx=n_ctx,                #tamaño de contexto (memoria conversacional). 512–1024 es razonable en CPU de pocos recursos. A más grande, más RAM y más lento.    
        n_threads=n_threads,        #número de hilos de CPU para la inferencia. 4 es razonable en CPU de pocos recursos. A más, más RAM y más lento.
        n_batch=n_batch,            #número de tokens por lote. 64 es razonable en CPU de pocos recursos. A más, más RAM y más lento.
        n_gpu_layers=n_gpu_layers,  #número de capas GPU para la inferencia. 0 es CPU. A más, más GPU y más rápido.
        f16_kv=f16_kv,              #reduce RAM del caché KV usando 16 bits. En CPU de bajos recursos suele ayudar activarlo.
        verbose=False,
        temperature=temperature,     #temperatura de la respuesta. 0.0 es más determinista, 1.0 más aleatorio.
        top_p=top_p,                #filtra el muestreo a los tokens más probables.(0.8–0.95)
        max_tokens=max_tokens,      #máximo de tokens por respuesta. 256 es razonable en CPU de pocos recursos. A más, más RAM y más lento.
    )

# -------------------------------
# UI de Streamlit
# -------------------------------

st.set_page_config(page_title="Chatbot educativo — GGUF local", page_icon="🎓", layout="centered")
st.title("Chatbot educativo — GGUF local (Gemma 2B)")

# Esto inicializa variables en la sesión de Streamlit para mantener el historial del chat
# y un contador para forzar la recarga del modelo si es necesario.
if "history" not in st.session_state:
    st.session_state.history = []  # Guarda la conversación como una lista de mensajes.
if "reload_key" not in st.session_state:
    st.session_state.reload_key = 0  # Permite recargar el modelo al cambiar este valor.

# Barra lateral: configuración
with st.sidebar:
    st.subheader("Configuración del modelo")

    model_path = st.text_input(
        "Ruta del modelo (GGUF)",
        value=DEFAULT_MODEL_PATH,
        help="Puedes dejarla por defecto o pegar la ruta completa al .gguf"
    )

    # Valores por defecto inspirados en tu script
    default_threads = min(4, os.cpu_count() or 1)
    n_ctx = st.number_input("n_ctx (contexto)", min_value=256, max_value=8192, value=1024, step=256)
    n_threads = st.number_input("n_threads", min_value=1, max_value=16, value=default_threads, step=1)
    n_batch = st.number_input("n_batch", min_value=16, max_value=512, value=64, step=16)
    n_gpu_layers = st.number_input("n_gpu_layers (0 = CPU)", min_value=0, max_value=64, value=0, step=1)
    f16_kv = st.checkbox("f16_kv", value=False)

    st.markdown("---")
    st.subheader("Muestreo")
    temperature = st.slider("temperature", 0.0, 1.5, 0.2, 0.05)
    top_p = st.slider("top_p", 0.1, 1.0, 0.9, 0.05)
    max_tokens = st.number_input("max_tokens (por respuesta)", min_value=64, max_value=2048, value=256, step=32)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Recargar modelo"):
            st.session_state.reload_key += 1
            
    with col2:
        if st.button("Nuevo chat", type="secondary"):
            st.session_state.history = []
            

# Carga del modelo (o muestra error claro)
# Da mensajes claros si la ruta es incorrecta o si el backend falla. Muy útil para usuarios no técnicos.
try:
    llm = get_llm(
        model_path=model_path,
        n_ctx=n_ctx,
        n_threads=n_threads,
        n_batch=n_batch,
        n_gpu_layers=n_gpu_layers,
        f16_kv=f16_kv,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        cache_bust=st.session_state.reload_key,
    )
    st.caption(f"Modelo: {os.path.basename(model_path)} | n_ctx={n_ctx}, threads={n_threads}")
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()
except Exception as e:
    st.error(f"No se pudo inicializar el modelo: {e}")
    st.stop()

# -------------------------------
# Historial y entrada de chat
# -------------------------------

# Muestra el historial arriba (tipo chat)
for m in st.session_state.history:
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.write(m["content"])

# Entrada de usuario (abajo)
user_input = st.chat_input("Escribe tu consulta (o 'salir')")

if user_input:
    # Comando para salir (coherente con tu CLI)
    if user_input.strip().lower() in {"salir", "exit", "quit"}:
        st.info("Sesión finalizada. Puedes iniciar un nuevo chat cuando quieras.")
    else:
        # Muestra el mensaje del usuario
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Construye el prompt con tu mismo esquema y stop tokens
        prompt = construir_prompt(st.session_state.history[:-1], user_input)

        # Llamada al modelo
        with st.chat_message("assistant"):
            placeholder = st.empty()
            try:
                # Respuesta única (no streaming), respetando tus stop tokens
                response = llm.invoke(prompt, stop=["Usuario:", "Asistente:"])
                text = getattr(response, "content", str(response)).strip()
            except Exception as e:
                text = f"[ERROR] Falló la inferencia: {e}"

            # Muestra y guarda la respuesta
            placeholder.write(text)
            st.session_state.history.append({"role": "assistant", "content": text})

        # Pequeña pausa para fluidez (opcional)
        time.sleep(0.05)
