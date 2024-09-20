import os
import yaml
import json
import torch
from torch.utils.data import DataLoader
from transformers import AdamW, get_scheduler, CLIPTextModel, CLIPTokenizer
from diffusers import UNet2DConditionModel, AutoencoderKL, DDPMScheduler, StableDiffusionControlNetPipeline
from torch import nn
from torchvision import transforms
from rich.progress import track
from torch.utils.data import Dataset
from PIL import Image

from src.utils.logger import get_logger

logger = get_logger()

class KanjiDataset(Dataset):
    def __init__(self, dataset_path: str, transform=None, tokenizer=None, max_length: int = 77):
        """
        Inicializa el dataset de Kanji.

        Args:
            dataset_path (str): Ruta al archivo JSON del dataset.
            transform (callable, optional): Transformaciones a aplicar a las imágenes.
            tokenizer (transformers.PreTrainedTokenizer, optional): Tokenizador para los textos.
            max_length (int, optional): Longitud máxima para el tokenizado.
        """
        with open(dataset_path, 'r') as f:
            self.data = json.load(f)
        self.transform = transform
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx: int):
        item = self.data[idx]
        image_path = item['image_path']
        text = item['text']

        # Cargar y transformar la imagen
        image = Image.open(image_path).convert('RGB')
        if self.transform:
            image = self.transform(image)

        # Tokenizar el texto
        if self.tokenizer:
            encoding = self.tokenizer(
                text,
                truncation=True,
                padding='max_length',
                max_length=self.max_length,
                return_tensors='pt'
            )
            input_ids = encoding['input_ids'].squeeze()
            attention_mask = encoding['attention_mask'].squeeze()
        else:
            input_ids = None
            attention_mask = None

        return {
            'pixel_values': image,
            'input_ids': input_ids,
            'attention_mask': attention_mask
        }
    
class Trainer:
    def __init__(self, config: dict):
        """
        Inicializa el entrenador con la configuración dada.
        
        Args:
            config (dict): Diccionario de configuración.
        """
        self.config = config

        # Configuración del dispositivo
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Usando dispositivo: {self.device}")

        # Configuración del caché de Hugging Face
        self.cache_dir = os.path.abspath(self.config.get('cache_dir', 'cache'))
        os.makedirs(self.cache_dir, exist_ok=True)
        logger.info(f"Usando directorio de caché personalizado: {self.cache_dir}")

        # Cargar el tokenizador y el modelo de texto
        self.tokenizer = CLIPTokenizer.from_pretrained(
            self.config['model']['tokenizer_pretrained'],
            cache_dir=self.cache_dir
        )
        self.text_encoder = CLIPTextModel.from_pretrained(
            self.config['model']['text_encoder_pretrained'],
            cache_dir=self.cache_dir
        ).to(self.device)
        logger.info("Tokenizador y Text Encoder cargados.")

        # Cargar el modelo UNet
        self.unet = UNet2DConditionModel.from_pretrained(
            self.config['model']['unet_pretrained'],
            cache_dir=self.cache_dir
        ).to(self.device)
        logger.info("UNet cargado.")

        # Cargar el VAE
        self.vae = AutoencoderKL.from_pretrained(
            self.config['model']['vae_pretrained'],
            cache_dir=self.cache_dir
        ).to(self.device)
        logger.info("VAE cargado.")

        # Configurar el optimizador
        self.optimizer = AdamW(self.unet.parameters(), lr=float(self.config['training']['learning_rate']))
        logger.info("Optimizador inicializado.")

        # Configurar el scheduler
        self.scheduler = get_scheduler(
            self.config['training']['scheduler_type'],
            optimizer=self.optimizer,
            num_warmup_steps=self.config['training']['warmup_steps'],
            num_training_steps=self.config['training']['total_steps']
        )
        logger.info("Scheduler inicializado.")

        # Función de pérdida
        self.criterion = nn.MSELoss()
        logger.info("Función de pérdida (MSELoss) establecida.")

        # Configurar el dataset y dataloader utilizando KanjiDataset
        transform = transforms.Compose([
            transforms.Resize((self.config['data']['image_size'], self.config['data']['image_size'])),
            transforms.ToTensor(),
            transforms.Normalize([0.5]*3, [0.5]*3)
        ])

        self.dataset = KanjiDataset(
            dataset_path=self.config['data']['dataset_path'],
            transform=transform,
            tokenizer=self.tokenizer,
            max_length=77
        )

        self.dataloader = DataLoader(
            self.dataset,
            batch_size=self.config['training']['batch_size'],
            shuffle=True,
            num_workers=self.config['data']['num_workers']
        )
        logger.info("Dataset y DataLoader inicializados.")

        self.load_pipeline()

    def load_pipeline(self):
        """
        Carga el pipeline de Stable Diffusion con ControlNet.
        """
        try:
            controlnet = UNet2DConditionModel.from_pretrained(
                self.config['model']['controlnet_pretrained'],
                cache_dir=self.cache_dir
            ).to(self.device)

            self.pipeline = StableDiffusionControlNetPipeline.from_pretrained(
                self.config['model']['pretrained_model_name_or_path'],
                controlnet=controlnet,
                safety_checker=None,        # Desactiva el safety_checker
                torch_dtype=torch.float32    # Cambiado a float32 para compatibilidad con CPU
            ).to(self.device)
            logger.info("Pipeline cargado exitosamente sin safety_checker.")
        except Exception as e:
            logger.error(f"Error al cargar el pipeline: {e}")
            raise e

    def train(self):
        """
        Ejecuta el proceso de entrenamiento.
        """
        logger.info("Iniciando proceso de entrenamiento.")
        self.unet.train()

        noise_scheduler = DDPMScheduler.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            subfolder="scheduler",
            cache_dir=self.cache_dir
        )
        
        for step in track(range(self.config['training']['total_steps']), description="Entrenando..."):
            for batch in self.dataloader:
                pixel_values = batch['pixel_values'].to(self.device)
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)

                # Codificar texto
                with torch.no_grad():
                    encoder_hidden_states = self.text_encoder(input_ids, attention_mask=attention_mask).last_hidden_state

                # Muestrear timesteps aleatorios
                timesteps = torch.randint(0, noise_scheduler.num_train_timesteps, (pixel_values.shape[0],), device=self.device).long()

                # Añadir ruido a las imágenes
                noisy_images = noise_scheduler.add_noise(pixel_values, torch.randn_like(pixel_values), timesteps)

                # Predicción del ruido con UNet
                noise_pred = self.unet(noisy_images, timesteps, encoder_hidden_states).sample

                # Cálculo de la pérdida
                loss = self.criterion(noise_pred, noisy_images)

                # Backpropagation
                loss.backward()
                self.optimizer.step()
                self.scheduler.step()
                self.optimizer.zero_grad()

                logger.info(f"Paso {step+1}/{self.config['training']['total_steps']} - Pérdida: {loss.item():.4f}")

                # Guardar checkpoint
                if (step + 1) % self.config['training']['checkpoint_interval'] == 0:
                    self.save_checkpoint(step + 1)

                # Avanzar al siguiente paso
                break

        logger.info("Entrenamiento completado exitosamente.")
        
    def save_checkpoint(self, step: int):
        """
        Guarda el estado actual del modelo.

        Args:
            step (int): Número del paso actual.
        """
        checkpoint_dir = os.path.join(self.config['training']['output_dir'], f"step_{step}")
        os.makedirs(checkpoint_dir, exist_ok=True)
        self.unet.save_pretrained(checkpoint_dir)
        logger.info(f"Checkpoint guardado en el paso {step} en {checkpoint_dir}")