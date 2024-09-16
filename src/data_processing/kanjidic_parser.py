import xml.etree.ElementTree as ET
import json
import os
from config import log

def parse_kanjidic(xml_file, output_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        kanji_data = {}

        for character in root.findall('.//character'):
            literal = character.find('literal').text
            meanings = [meaning.text for meaning in character.findall('.//meaning')]
            kanji_data[literal] = {'meanings': meanings}

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(kanji_data, f, ensure_ascii=False, indent=2)

        log.info(f"Successfully parsed KANJIDIC2 data from {xml_file} to {output_file}")
    except Exception as e:
        log.error(f"Failed to parse KANJIDIC2 data: {e}")

def main():
    input_file = 'data/raw/kanjidic2/kanjidic2.xml'
    output_file = 'data/processed/definitions/kanjidic_processed.json'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    parse_kanjidic(input_file, output_file)

if __name__ == "__main__":
    main()