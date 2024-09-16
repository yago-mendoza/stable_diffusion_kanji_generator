import xml.etree.ElementTree as ET
import json
import io
from PIL import Image
from utils.logger import log
from pathlib import Path
import cairosvg

def parse_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        return tree.getroot()
    except Exception as e:
        log.error(f"Failed to parse XML file {xml_file}: {e}")
        return None

def create_image_from_svg(svg_content, image_output_dir, literal):
    try:
        png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'))
        img = Image.open(io.BytesIO(png_data))
        img_path = Path(image_output_dir) / f"{literal}.png"
        img.save(img_path)
        log.info(f"Successfully processed kanji {literal} and saved to {img_path}")
        return img_path
    except Exception as e:
        log.error(f"Error converting SVG to PNG for kanji {literal}: {e}")
        return None

def process_kanji_element(kanji, image_output_dir):
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
    <svg xmlns="http://www.w3.org/2000/svg" width="109" height="109" viewBox="0 0 109 109">
        <rect width="109" height="109" fill="white"/>
        {ET.tostring(g_element, encoding="unicode")}
    </svg>
    '''

    svg_path = Path(image_output_dir) / f"{literal}.svg"
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    with svg_path.open('w', encoding='utf-8') as svg_file:
        svg_file.write(svg_content)

    img_path = create_image_from_svg(svg_content, image_output_dir, literal)
    if img_path is None:
        return None

    return {
        'id': kanji_id,
        'image_path': str(img_path)
    }

def parse_kanjivg_xml(xml_file, output_file, image_output_dir, limit=None):
    # Parse the XML file
    root = parse_xml(xml_file)
    if root is None:
        log.error(f"Failed to parse XML file: {xml_file}")
        return

    # Extract kanji elements from the parsed XML
    kanji_elements = root.findall('.//kanji')
    log.info(f"Found {len(kanji_elements)} kanji elements in the XML.")

    kanji_images = {} # maps 'kanji character' -> 'id' and 'image_path'
    processed_count = 0

    # Process each kanji element
    for kanji_element in kanji_elements:
        # Stop processing if the limit is reached
        if limit is not None and processed_count >= limit:
            log.info(f"Reached processing limit of {limit} kanji.")
            break

        # Process the current kanji element
        processed_kanji = process_kanji_element(kanji_element, image_output_dir)
        if processed_kanji:
            kanji_images[processed_kanji['id']] = processed_kanji
            processed_count += 1

    # Save the processed kanji data to a JSON file
    with Path(output_file).open('w', encoding='utf-8') as json_file:
        json.dump(kanji_images, json_file, ensure_ascii=False, indent=2)

    log.info(f"Successfully processed {processed_count} kanji characters.")
    log.info(f"Saved processed data to: {output_file}")

def main():
    input_file = 'data/raw/kanjivg/kanjivg.xml'
    output_file = 'data/processed/definitions/kanjivg_processed.json'
    image_output_dir = 'data/processed/images'

    # Create necessary directories if they don't exist
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    Path(image_output_dir).mkdir(parents=True, exist_ok=True)

    parse_kanjivg_xml(input_file, output_file, image_output_dir, limit=10)

if __name__ == "__main__":
    main()