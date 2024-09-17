import xml.etree.ElementTree as ET
import json
from src.utils.logger import get_logger

log = get_logger()

class KanjidicParser:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def process(self):
        try:
            tree = self.parse_xml()
            kanji_data = self.extract_kanji_data(tree)
            self.save_kanji_data(kanji_data)
            log.info(f"KANJIDIC2 data parsed and saved to {self.output_file}")
        except Exception as e:
            log.error(f"Error parsing KANJIDIC2 data: {e}")
            raise

    def parse_xml(self):
        try:
            tree = ET.parse(self.input_file)
            return tree.getroot()
        except ET.ParseError as e:
            log.error(f"Error parsing XML file: {e}")
            raise

    def extract_kanji_data(self, root):
        kanji_data = {}
        for character in root.findall('.//character'):
            kanji = character.find('literal').text
            kanji_data[kanji] = {
                "meanings": self.extract_meanings(character),
                "on_readings": self.extract_readings(character, 'ja_on'),
                "kun_readings": self.extract_readings(character, 'ja_kun')
            }
        return kanji_data

    def extract_meanings(self, character):
        return [m.text for m in character.findall('.//meaning')]

    def extract_readings(self, character, reading_type):
        return [r.text for r in character.findall(f".//reading[@r_type='{reading_type}']")]

    def save_kanji_data(self, kanji_data):
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(kanji_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    parser = KanjidicParser("data/processed/kanjidic2/kanjidic2.xml", "data/processed/kanjidic2/kanjidic2.json")
    parser.process()