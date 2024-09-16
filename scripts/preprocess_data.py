"""
This script runs a series of preprocessing steps, including:
1. Decompressing data                    (scripts/decompress_data.py)
2. Processing KANJIDIC2 data             (src/data_processing/kanjidic_parser.py)
3. Converting SVG files to pixel images  (src/data_processing/svg_to_pixel.py)
4. Building the dataset                  (src/data_processing/dataset_builder.py)
"""

import os
import subprocess
from config import log

def run_script(script_path):
    full_path = os.path.join(os.path.dirname(__file__), script_path)
    try:
        subprocess.run(['python', full_path], check=True)
        log.info(f"Successfully ran script: {script_path}")
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to run script {script_path}: {e}")

def main():
    # Step 1: Decompress the data
    log.info("Decompressing data...")
    run_script('decompress_data.py')

    # Step 2: Process the KANJIDIC2 data
    log.info("Processing KANJIDIC2...")
    run_script('../src/data_processing/kanjidic_parser.py')

    # Step 3: Convert SVG files to pixel images
    log.info("Converting SVG to pixel images...")
    run_script('../src/data_processing/svg_to_pixel.py')

    # Step 4: Build the dataset
    log.info("Building the dataset...")
    run_script('../src/data_processing/dataset_builder.py')

    log.info("Preprocessing complete.")

if __name__ == "__main__":
    main()