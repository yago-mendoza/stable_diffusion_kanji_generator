import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.logger import log
from src.data_preprocessing import decompress_data, kanjidic_parser, svg_to_pixel, dataset_builder

def main():
    steps = [
        ("Decompressing data", decompress_data.main),
        ("Parsing KANJIDIC2 data", kanjidic_parser.main),
        ("Converting SVG to pixel images", svg_to_pixel.main),
        ("Building the dataset", dataset_builder.main)
    ]

    for step_name, step_function in steps:
        log.info(f"Starting: {step_name}")
        try:
            step_function()
            log.info(f"Completed: {step_name}")
        except Exception as e:
            log.error(f"Error in {step_name}: {e}")
            sys.exit(1)

    log.info("Preprocessing complete.")

if __name__ == "__main__":
    main()