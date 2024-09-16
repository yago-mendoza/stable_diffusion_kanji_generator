import os
import subprocess
from utils.logger import log

def run_script(script_path):
    """
    Run a Python script from the current directory.
    """
    full_path = os.path.join(os.path.dirname(__file__), script_path)
    try:
        subprocess.run(['python', full_path], check=True)
        log.info(f"Successfully ran script: {script_path}")
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to run script {script_path}: {e}")

def main():
    scripts = [
        'decompress_data.py',  # Decompress the data
        'kanjidic_parser.py',  # Parse the KANJIDIC2 data
        'svg_to_pixel.py',     # Convert SVG files to pixel images
        'dataset_builder.py'  # Build the dataset
    ]

    for script in scripts:
        log.info(f"Running {script}...")
        run_script(f'../src/data_preprocessing/{script}')

    log.info("Preprocessing complete.")

if __name__ == "__main__":
    main()