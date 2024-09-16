import gzip
from pathlib import Path
from src.utils.logger import log

def decompress_file(compressed_path, decompressed_path):
    try:
        with gzip.open(compressed_path, 'rb') as f_in:
            with open(decompressed_path, 'wb') as f_out:
                f_out.write(f_in.read())
        log.info(f"Decompressed {compressed_path} to {decompressed_path}")
    except Exception as e:
        log.error(f"Failed to decompress {compressed_path}: {e}")

def main():
    data_dir = Path('data/raw')
    
    # Decompress KANJIDIC2
    kanjidic_compressed = data_dir / 'kanjidic2' / 'kanjidic2.xml.gz'
    kanjidic_decompressed = data_dir / 'kanjidic2' / 'kanjidic2.xml'
    decompress_file(kanjidic_compressed, kanjidic_decompressed)
    
    # Decompress KanjiVG
    kanjivg_compressed = data_dir / 'kanjivg' / 'kanjivg-20220427.xml.gz'
    kanjivg_decompressed = data_dir / 'kanjivg' / 'kanjivg.xml'
    decompress_file(kanjivg_compressed, kanjivg_decompressed)

if __name__ == "__main__":
    main()