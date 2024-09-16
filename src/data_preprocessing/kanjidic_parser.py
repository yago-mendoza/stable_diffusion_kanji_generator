import xml.etree.ElementTree as ET
import json
import os
from src.utils.logger import log

def extract_kanji_data(root: ET.Element) -> dict:
    # Extracts <literal> and <meaning> elements from the XML file
    kanji_data = {}
    for char in root.findall('.//character'):
        literal = char.find('literal').text
        meanings = [meaning.text for meaning in char.findall('.//meaning')]
        kanji_data[literal] = {'meanings': meanings}
    return kanji_data

def parse_kanjidic_xml(xml_file: str, output_file: str) -> None:
    try:
        tree = ET.parse(xml_file) # hierarchical structure of XML for easy access and edits
        root = tree.getroot() # top-level element in the XML file
        
        kanji_data = extract_kanji_data(root)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(kanji_data, f, ensure_ascii=False, indent=2)

        log.info(f"Successfully parsed KANJIDIC2 data from {xml_file} to {output_file}")
    except Exception as e:
        log.error(f"Failed to parse KANJIDIC2 data: {e}")

def main():
    input_file = 'data/raw/kanjidic2/kanjidic2.xml'
    output_file = 'data/processed/definitions/kanjidic_processed.json'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    parse_kanjidic_xml(input_file, output_file)

if __name__ == "__main__":
    main()