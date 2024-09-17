import xml.etree.ElementTree as ET
import json
import io
from PIL import Image
from pathlib import Path
import cairosvg
from src.utils.logger import get_logger

log = get_logger()

class SvgToPixelConverter:
    def __init__(self, input_file, output_file, image_output_dir, svg_output_dir, limit=10, width=128, height=128):
        self.input_file = input_file
        self.output_file = output_file
        self.image_output_dir = Path(image_output_dir)
        self.svg_output_dir = Path(svg_output_dir)
        self.limit = limit
        self.width = width
        self.height = height

    @staticmethod
    def parse_xml(xml_file):
        try:
            tree = ET.parse(xml_file)
            return tree.getroot()
        except Exception as e:
            log.error(f"Failed to parse XML file {xml_file}: {e}")
            return None

    def create_image_from_svg(self, svg_content, literal):
        try:
            png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'))
            img = Image.open(io.BytesIO(png_data))
            img_path = self.image_output_dir / f"{literal}.png"
            img_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(img_path)
            log.info(f"Successfully processed kanji {literal} and saved to {img_path}")
            return img_path
        except Exception as e:
            log.error(f"Error converting SVG to PNG for kanji {literal}: {e}")
            return None

    def process_kanji_element(self, kanji):
        kanji_id = kanji.get('id')
        g_element = kanji.find("g")
        literal = g_element.get('{http://kanjivg.tagaini.net}element') if g_element is not None else None

        if literal is None or g_element is None or not list(g_element):
            log.warning(f"Skipping kanji with ID {kanji_id} due to missing literal or <g> elements.")
            return None

        path_elements = g_element.findall(".//path")
        for path in path_elements:
            path.set('stroke', 'black')
            path.set('fill', 'none')

        svg_content = f'''
        <svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 109 109">
            <rect width="109" height="109" fill="white"/>
            {ET.tostring(g_element, encoding="unicode")}
        </svg>
        '''

        svg_path = self.svg_output_dir / f"{literal}.svg"
        svg_path.parent.mkdir(parents=True, exist_ok=True)
        with svg_path.open('w', encoding='utf-8') as svg_file:
            svg_file.write(svg_content)

        img_path = self.create_image_from_svg(svg_content, literal)
        if img_path is None:
            return None

        return {
            'id': kanji_id,
            'image_path': str(img_path),
            'svg_path': str(svg_path)
        }

    def process(self):
        root = self.parse_xml(self.input_file)
        if root is None:
            log.error(f"Failed to parse XML file: {self.input_file}")
            return

        kanji_elements = root.findall('.//kanji')
        log.info(f"Found {len(kanji_elements)} kanji elements in the XML.")

        kanji_images = {}
        processed_count = 0

        for kanji_element in kanji_elements:
            if self.limit is not None and processed_count >= self.limit:
                break
            processed_kanji = self.process_kanji_element(kanji_element)
            if processed_kanji:
                kanji_images[processed_kanji['id']] = processed_kanji
                processed_count += 1

        with Path(self.output_file).open('w', encoding='utf-8') as json_file:
            json.dump(kanji_images, json_file, ensure_ascii=False, indent=2)

        log.info(f"Successfully processed {processed_count} kanji characters.")
        log.info(f"Saved processed data to: {self.output_file}")

if __name__ == "__main__":
    converter = SvgToPixelConverter(
        input_file="data/raw/kanjivg/kanjivg.xml",
        output_file="data/processed/svg/kanjivg_processed.json",
        image_output_dir="data/processed/images",
        svg_output_dir="data/processed/svg",
        limit=10  # Set a limit of 10 kanji for testing
    )
    converter.process()

