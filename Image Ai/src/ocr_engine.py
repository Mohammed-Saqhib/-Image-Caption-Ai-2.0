import easyocr
import numpy as np
from PIL import Image

class OCREngine:
    def __init__(self, languages=['en']):
        """
        Initialize the OCR engine with specified languages.
        :param languages: List of language codes (e.g., ['en', 'hi', 'kn'])
        """
        self.reader = easyocr.Reader(languages)

    def extract_text(self, image):
        """
        Extract text from an image.
        :param image: Image file (PIL Image or numpy array)
        :return: Extracted text as a string
        """
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        result = self.reader.readtext(image, detail=0)
        return " ".join(result)

if __name__ == "__main__":
    # Test the OCR engine
    ocr = OCREngine(languages=['en'])
    print("OCR Engine Initialized")
