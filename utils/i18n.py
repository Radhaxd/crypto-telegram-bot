
import json
from utils.logger import main_logger

class I18n:
    def __init__(self):
        self.translations = {}
        self.default_language = 'en'

    def load_translations(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except Exception as e:
            main_logger.error(f"Error loading translations: {str(e)}", exc_info=True)

    def get_text(self, key, language='en'):
        if language not in self.translations:
            language = self.default_language
        return self.translations.get(language, {}).get(key, key)

i18n = I18n()
i18n.load_translations('data/translations.json')
