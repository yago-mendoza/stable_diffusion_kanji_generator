import json
import os
from src.utils.logger import get_logger

log = get_logger()

class DatasetBuilder:
    def __init__(self, definitions_file, images_dir, output_file):
        self.definitions_file = definitions_file
        self.images_dir = images_dir
        self.output_file = output_file

    def process(self):
        try:
            with open(self.definitions_file, 'r', encoding='utf-8') as f:
                kanji_data = json.load(f)

            log.info(f"Loaded {len(kanji_data)} kanji definitions from {self.definitions_file}")

            dataset = []
            missing_images = []
            for kanji, data in kanji_data.items():
                image_path = os.path.join(self.images_dir, f"{kanji}.png")
                if os.path.exists(image_path):
                    dataset.append({
                        "kanji": kanji,
                        "meanings": data["meanings"],
                        "on_readings": data["on_readings"],
                        "kun_readings": data["kun_readings"],
                        "image_path": image_path
                    })
                else:
                    missing_images.append(kanji)

            log.info(f"Found images for {len(dataset)} kanji")
            log.warning(f"Missing images for {len(missing_images)} kanji")

            if missing_images:
                log.info(f"First 10 missing kanji: {', '.join(missing_images[:10])}")

            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, ensure_ascii=False, indent=2)

            log.info(f"Dataset built and saved to {self.output_file}")
        except Exception as e:
            log.error(f"Error building dataset: {e}")
            raise

    def verify_data(self):
        log.info(f"Verifying data sources...")
        log.info(f"Definitions file: {os.path.exists(self.definitions_file)}")
        log.info(f"Images directory: {os.path.exists(self.images_dir)}")
        if os.path.exists(self.images_dir):
            image_count = len([f for f in os.listdir(self.images_dir) if f.endswith('.png')])
            log.info(f"Number of PNG files in images directory: {image_count}")

if __name__ == "__main__":
    builder = DatasetBuilder(
        definitions_file="data/processed/definitions/kanjidic_processed.json",
        images_dir="data/processed/images",
        output_file="data/processed/dataset.json"
    )
    builder.verify_data()
    builder.process()