import json
import os
from PIL import Image
import numpy as np
from utils.logger import log

def build_dataset(definitions_file, images_dir, output_file):
    log.info("Starting dataset build process...")

    try:
        with open(definitions_file, 'r', encoding='utf-8') as f:
            kanji_data = json.load(f)

        dataset = []
        skipped_count = 0

        for kanji, data in kanji_data.items():
            image_path = os.path.join(images_dir, f"{kanji}.png")
            
            if os.path.exists(image_path):
                with Image.open(image_path) as img:
                    img_array = np.array(img) / 255.0

                entry = {
                    "kanji": kanji,
                    "meanings": data["meanings"],
                    "image": img_array.tolist()
                }
                dataset.append(entry)
            else:
                log.warning(f"Image not found for kanji: {kanji}")
                skipped_count += 1

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)

        log.info(f"Dataset build complete. Total entries: {len(dataset)}. Skipped {skipped_count} kanji due to missing images.")
        log.info(f"Dataset saved to {output_file}")
    except Exception as e:
        log.error(f"Failed to build dataset: {e}")

def main():
    output_file = 'data/dataset/kanji_dataset.json'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    definitions_file = 'data/processed/definitions/kanjidic_processed.json'
    images_dir = 'data/processed/images'
    build_dataset(definitions_file, images_dir, output_file)

if __name__ == "__main__":
    main()