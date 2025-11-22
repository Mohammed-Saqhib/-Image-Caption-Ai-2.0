from deep_translator import GoogleTranslator

class TranslationEngine:
    def __init__(self):
        """
        Initialize the Translation Engine using Google Translator.
        """
        self.supported_languages = {
            'English': 'en',
            'Hindi': 'hi',
            'Kannada': 'kn',
            'Tamil': 'ta',
            'Telugu': 'te',
            'Marathi': 'mr',
            'Bengali': 'bn',
            'Gujarati': 'gu',
            'Malayalam': 'ml',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Italian': 'it',
            'Portuguese': 'pt',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Chinese': 'zh-CN',
            'Russian': 'ru',
            'Arabic': 'ar'
        }

    def translate(self, text, target_language='Hindi', source_language='auto'):
        """
        Translate text to target language.
        :param text: Text to translate
        :param target_language: Target language name (e.g., 'Hindi')
        :param source_language: Source language code (default 'auto' for auto-detection)
        :return: Translated text
        """
        try:
            if not text.strip():
                return ""
            
            # Get language code
            target_code = self.supported_languages.get(target_language, 'hi')
            
            # Translate
            translator = GoogleTranslator(source=source_language, target=target_code)
            translated = translator.translate(text)
            
            return translated
        except Exception as e:
            raise Exception(f"Translation error: {e}")

    def get_supported_languages(self):
        """
        Get list of supported language names.
        :return: List of language names
        """
        return list(self.supported_languages.keys())


if __name__ == "__main__":
    # Test the translation engine
    translation_engine = TranslationEngine()
    test_text = "Hello, how are you?"
    translated = translation_engine.translate(test_text, 'Hindi')
    print(f"Original: {test_text}")
    print(f"Translated: {translated}")
