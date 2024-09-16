import xml.etree.ElementTree as ET
import json
import os
import cairosvg
import io
from PIL import Image
from config import log

def parse_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        return tree.getroot()
    except Exception as e:
        log.error(f"Failed to parse XML file {xml_file}: {e}")
        return None

def extract_kanji_elements(root):
    return root.findall('.//kanji')

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

    svg_path = os.path.join(image_output_dir, f"{literal}.svg")
    os.makedirs(image_output_dir, exist_ok=True)
    with open(svg_path, 'w', encoding='utf-8') as svg_file:
        svg_file.write(svg_content)

    try:
        png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'))
        img = Image.open(io.BytesIO(png_data))
        img_path = os.path.join(image_output_dir, f"{literal}.png")
        img.save(img_path)
        log.info(f"Successfully processed kanji {literal} and saved to {img_path}")
    except Exception as e:
        log.error(f"Error converting SVG to PNG for kanji {literal}: {e}")
        return None

    return {
        'id': kanji_id,
        'image_path': img_path
    }

def parse_kanjivg(xml_file, output_file, image_output_dir, limit=None):
    root = parse_xml(xml_file)
    if root is None:
        return

    kanji_elements = extract_kanji_elements(root)
    log.info(f"Found {len(kanji_elements)} kanji elements.")

    kanji_data = {}
    count = 0

    for kanji in kanji_elements:
        if limit is not None and count >= limit:
            break

        result = process_kanji_element(kanji, image_output_dir)
        if result:
            kanji_data[result['id']] = result
            count += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(kanji_data, f, ensure_ascii=False, indent=2)

    log.info(f"Processed {count} kanji characters and saved to {output_file}")

def main():
    input_file = 'data/raw/kanjivg/kanjivg.xml'
    output_file = 'data/processed/definitions/kanjivg_processed.json'
    image_output_dir = 'data/processed/images'
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    os.makedirs(image_output_dir, exist_ok=True)
    parse_kanjivg(input_file, output_file, image_output_dir, limit=10)

if __name__ == "__main__":
    main()