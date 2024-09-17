import gzip
from pathlib import Path
from src.utils.logger import get_logger

log = get_logger()

class DataDecompressor:
    def __init__(self, input_files, output_files):
        self.input_files = [Path(f) for f in input_files]
        self.output_files = [Path(f) for f in output_files]

    def decompress_file(self, compressed_path, decompressed_path):
        try:
            with gzip.open(compressed_path, 'rb') as f_in:
                with open(decompressed_path, 'wb') as f_out:
                    f_out.write(f_in.read())
            log.info(f"Decompressed {compressed_path} to {decompressed_path}")
        except Exception as e:
            log.error(f"Failed to decompress {compressed_path}: {e}")

    def process(self):
        for input_file, output_file in zip(self.input_files, self.output_files):
            self.decompress_file(input_file, output_file)

if __name__ == "__main__":
    decompressor = DataDecompressor(
        input_files=["data/raw/kanjidic2/kanjidic2.xml.gz", "data/raw/kanjivg/kanjivg-20220427.xml.gz"],
        output_files=["data/processed/kanjidic2/kanjidic2.xml", "data/processed/kanjivg/kanjivg.xml"]
    )
    decompressor.process()