import os

from dotenv import load_dotenv


def load_environment_variables():
    """Cargar las variables de entorno basadas en el entorno configurado"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, "../.."))

    env_name = os.getenv(
        "FLASK_ENV", "development"
    )  # Establecer desarrollo como predeterminado
    env_file = ".env" if env_name == "development" else ".env.test"

    env_path = os.path.join(parent_dir, env_file)

    loaded = load_dotenv(env_path)
    if loaded:
        print(f"Variables de entorno cargadas correctamente desde {env_path}")
    else:
        print(f"No se pudieron cargar las variables de entorno desde {env_path}")
    return loaded