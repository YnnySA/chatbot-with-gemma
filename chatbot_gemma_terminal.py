#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from langchain_community.llms import LlamaCpp  # Importa el wrapper para modelos GGUF usando Llama.cpp

# Ruta del modelo GGUF, configurable por variable de entorno o por defecto en carpeta 'models'
MODEL_PATH = os.environ.get(
    "LLAMA_GGUF_PATH",
    os.path.join("models", "gemma-2-2b-it-Q5_K_M.gguf"),
)

# Función para cargar el modelo LlamaCpp con parámetros personalizados
def load_llm(model_path: str) -> LlamaCpp:
    # Verifica si el archivo del modelo existe
    if not os.path.exists(model_path):
        print(f"[ERROR] No se encontró el modelo en: {model_path}")
        sys.exit(1)  # Termina el programa si no se encuentra el modelo

    # Inicializa el modelo con configuración optimizada para rendimiento local
    return LlamaCpp(
        model_path=model_path,  # Ruta del archivo GGUF
        n_ctx=1024,             # Tamaño del contexto (tokens que puede manejar)
        n_threads=4,            # Número de hilos para procesamiento
        n_batch=64,             # Tamaño de lote para inferencia
        n_gpu_layers=0,         # Capas en GPU (0 si no se usa GPU)
        f16_kv=False,           # Desactiva uso de claves en float16 (más compatible)
        verbose=False,          # No mostrar logs detallados
        temperature=0.2,        # Controla la aleatoriedad (más bajo = más preciso)
        top_p=0.9,              # Probabilidad acumulada para muestreo
        max_tokens=256,         # Máximo de tokens generados por respuesta
    )

# Función principal del chatbot
def main():
    llm = load_llm(MODEL_PATH)  # Carga el modelo GGUF

    # Prompt del sistema que define el rol del asistente
    system_prompt = (
        "Eres un asistente educativo útil y claro. Responde en español, "
        "con explicaciones breves y adaptadas a un nivel básico-intermedio.\n"
    )

    # Mensaje de bienvenida
    print("Chatbot educativo — Gemma 2B (GGUF local)")
    print("Escribe tu consulta y presiona Enter. Escribe 'salir' para terminar.")

    history = ""  # Historial de conversación acumulado

    # Bucle principal del chatbot
    while True:
        try:
            user_input = input("\nTú: ").strip()  # Captura entrada del usuario
        except (EOFError, KeyboardInterrupt):     # Maneja interrupciones
            print("\n[INFO] Sesión finalizada.")
            break

        # Comando para salir del chatbot
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("[INFO] ¡Hasta luego!")
            break

        # Construye el prompt completo con historial y entrada actual
        prompt = f"{system_prompt}{history}Usuario: {user_input}\nAsistente:"
        try:
            # Invoca el modelo con tokens de parada para evitar simulaciones
            response = llm.invoke(prompt, stop=["Usuario:", "Asistente:"])
        except Exception as e:
            print(f"[ERROR] Falló la inferencia: {e}")
            continue

        # Extrae el texto generado por el modelo
        text = getattr(response, "content", str(response)).strip()
        print(f"Bot: {text}")  # Muestra la respuesta en consola

        # Actualiza el historial con el nuevo turno
        history += f"Usuario: {user_input}\nAsistente: {text}\n"
        time.sleep(0.05)  # Pequeña pausa para fluidez

# Punto de entrada del script
if __name__ == "__main__":
    main()
