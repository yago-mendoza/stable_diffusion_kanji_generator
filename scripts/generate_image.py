import os
import torch
from transformers import CLIPTokenizer, CLIPTextModel
from diffusers import StableDiffusionControlNetPipeline, UNet2DConditionModel, AutoencoderKL, DDPMScheduler
from PIL import Image
import argparse
import yaml

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

# def load_models(config: dict, device: torch.device):
#     """
#     Carga los modelos necesarios para la generación de imágenes.

#     Args:
#         config (dict): Diccionario de configuración.
#         device (torch.device): Dispositivo para cargar los modelos.

#     Returns:
#         tuple: Tokenizador, Text Encoder, UNet, VAE, Noise Scheduler.
#     """
#     logger.info("Cargando modelos para inferencia...")

#     try:
#         tokenizer = CLIPTokenizer.from_pretrained(
#             config['model']['tokenizer_pretrained'],
#             cache_dir=config.get('cache_dir', 'cache')
#         )
#         text_encoder = CLIPTextModel.from_pretrained(
#             config['model']['text_encoder_pretrained'],
#             cache_dir=config.get('cache_dir', 'cache')
#         ).to(device)
#         unet = UNet2DConditionModel.from_pretrained(
#             config['model']['unet_pretrained'],
#             cache_dir=config.get('cache_dir', 'cache')
#         ).to(device)
#         vae = AutoencoderKL.from_pretrained(
#             config['model']['vae_pretrained'],
#             cache_dir=config.get('cache_dir', 'cache')
#         ).to(device)
#         noise_scheduler = DDPMScheduler.from_pretrained(
#             config['training']['noise_scheduler_config'],
#             cache_dir=config.get('cache_dir', 'cache')
#         )
#         logger.info("Modelos cargados exitosamente.")
#         return tokenizer, text_encoder, unet, vae, noise_scheduler
#     except Exception as e:
#         logger.error(f"Error al cargar los modelos: {e}")
#         raise e

def load_pipeline(config: dict, device: torch.device):
    """
    Carga el pipeline de Stable Diffusion con ControlNet.
    """
    try:
        controlnet = UNet2DConditionModel.from_pretrained(
            config['model']['controlnet_pretrained'],
            cache_dir=config.get('cache_dir', 'cache')
        ).to(device)

        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "./pretrained_model/stable-diffusion-v1-5",
            controlnet=controlnet,
            safety_checker=None,         # Desactiva el safety_checker
            torch_dtype=torch.float16
        ).to(device)
        logger.info("Pipeline cargado exitosamente sin safety_checker.")
        return pipe
    except Exception as e:
        logger.error(f"Error al cargar el pipeline: {e}")
        raise e
    
def generate_image(prompt: str, pipe: StableDiffusionControlNetPipeline, config: dict, device: torch.device) -> Image.Image:
    """
    Genera una imagen a partir de un prompt de texto.
    """
    try:
        logger.info(f"Generando imagen para el prompt: {prompt}")
        with torch.no_grad():
            image = pipe(prompt).images[0]
        logger.info("Generación de imagen completada.")
        return image
    except Exception as e:
        logger.error(f"Error durante la generación de la imagen: {e}")
        raise e

def parse_arguments():
    """
    Analiza los argumentos de la línea de comandos.

    Returns:
        argparse.Namespace: Namespace con los argumentos.
    """
    parser = argparse.ArgumentParser(description="Generar Imágenes Kanji a partir de Prompts de Texto")
    parser.add_argument("prompt", type=str, help="Prompt de texto para generar la imagen Kanji")
    parser.add_argument("--config", type=str, default="configs/train_config.yaml",
                        help="Ruta al archivo de configuración YAML")
    parser.add_argument("--output", type=str, default="generated_image.png",
                        help="Ruta para guardar la imagen generada")
    return parser.parse_args()

def main():
    args = parse_arguments()
    logger.info("Iniciando generación de imagen.")

    try:
        config = load_config(args.config)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Usando dispositivo: {device}")

        pipe = load_pipeline(config, device)

        pil_image = generate_image(
            prompt=args.prompt,
            pipe=pipe,
            config=config,
            device=device
        )

        pil_image.save(args.output)
        logger.info(f"Imagen guardada en: {args.output}")

    except Exception as e:
        logger.error(f"Error durante la generación de la imagen: {e}")
        exit(1)

if __name__ == "__main__":
    main()