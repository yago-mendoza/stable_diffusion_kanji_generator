import os
import yaml
from src.model.training import Trainer
from src.utils.logger import get_logger

logger = get_logger()

def load_config(config_path: str) -> dict:
    """
    Carga la configuración desde un archivo YAML.

    Args:
        config_path (str): Ruta al archivo de configuración.

    Returns:
        dict: Diccionario de configuración.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"El archivo de configuración no se encontró: {config_path}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def main():
    """
    Función principal para iniciar el entrenamiento.
    """
    config_path = 'configs/train_config.yaml'

    try:
        config = load_config(config_path)
        trainer = Trainer(config)
        trainer.train()
    except Exception as e:
        logger.error(f"Error durante el entrenamiento: {e}")
        exit(1)

if __name__ == "__main__":
    main()