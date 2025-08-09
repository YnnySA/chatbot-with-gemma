import os
import sys
import subprocess


def show_message(text: str, title: str = "Lanzador Chatbot") -> None:
    try:
        import ctypes  # type: ignore
        ctypes.windll.user32.MessageBoxW(0, text, title, 0x40)  # MB_ICONINFORMATION
    except Exception:
        pass


def _find_app_script(base_dir: str) -> str | None:
    candidates = [
        os.path.join(base_dir, "chatbot_gemma_st.py"),
        os.path.join(base_dir, "..", "chatbot_with_LlamaCpp", "chatbot_gemma_st.py"),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return os.path.abspath(candidate)

    for root, _dirs, files in os.walk(base_dir):
        if "chatbot_gemma_st.py" in files:
            return os.path.join(root, "chatbot_gemma_st.py")
    parent = os.path.abspath(os.path.join(base_dir, ".."))
    for root, _dirs, files in os.walk(parent):
        if "chatbot_gemma_st.py" in files:
            return os.path.join(root, "chatbot_gemma_st.py")
    return None


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app_script = _find_app_script(base_dir)

    if not app_script:
        show_message(
            "No se encontró chatbot_gemma_st.py en el proyecto.\n\n"
            "Asegúrate de que el archivo existe y que el lanzador esté junto al proyecto."
        )
        return

    # Prioriza el pythonw.exe del venv en esta carpeta o en la carpeta padre
    parent_dir = os.path.abspath(os.path.join(base_dir, ".."))
    venv_candidates = [
        os.path.join(base_dir, "streamlit_venv", "Scripts", "pythonw.exe"),
        os.path.join(base_dir, "venv", "Scripts", "pythonw.exe"),
        os.path.join(base_dir, ".venv", "Scripts", "pythonw.exe"),
        os.path.join(parent_dir, "streamlit_venv", "Scripts", "pythonw.exe"),
        os.path.join(parent_dir, "venv", "Scripts", "pythonw.exe"),
        os.path.join(parent_dir, ".venv", "Scripts", "pythonw.exe"),
    ]
    pythonw_exe = next((p for p in venv_candidates if os.path.exists(p)), sys.executable)

    cmd = [pythonw_exe, "-m", "streamlit", "run", app_script]

    create_no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    detached_process = getattr(subprocess, "DETACHED_PROCESS", 0)
    creation_flags = create_no_window | detached_process

    try:
        subprocess.Popen(cmd, cwd=base_dir, creationflags=creation_flags)
    except FileNotFoundError:
        show_message(
            "No se pudo ejecutar Streamlit.\n\n"
            "Si usas un entorno virtual, asegúrate de que esté creado e instalado:\n"
            "  1) python -m venv streamlit_venv\n"
            "  2) streamlit_venv\\Scripts\\python.exe -m pip install --upgrade pip\n"
            "  3) streamlit_venv\\Scripts\\python.exe -m pip install streamlit langchain-community llama-cpp-python\n\n"
            "Luego vuelve a ejecutar este lanzador."
        )
    except Exception as exc:
        show_message(f"No se pudo iniciar la app:\n{exc}")


if __name__ == "__main__":
    main()




