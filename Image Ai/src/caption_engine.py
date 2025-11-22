from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

class CaptionEngine:
    def __init__(self, use_cloud=False):
        """
        Initialize the Caption Engine with BLIP model.
        :param use_cloud: If True, use Hugging Face API instead of local model
        """
        self.use_cloud = use_cloud
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        if not use_cloud:
            print("Loading BLIP model locally...")
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model.to(self.device)
            print(f"BLIP model loaded on {self.device}")
        else:
            self.processor = None
            self.model = None
            print("Using cloud API mode for captioning")

    def generate_caption(self, image, max_length=50):
        """
        Generate a caption for the given image.
        :param image: PIL Image object
        :param max_length: Maximum length of the caption
        :return: Generated caption string
        """
        if self.use_cloud:
            return self._generate_caption_cloud(image)
        else:
            return self._generate_caption_local(image, max_length)

    def _generate_caption_local(self, image, max_length):
        """
        Generate caption using local BLIP model.
        """
        try:
            # Preprocess image
            inputs = self.processor(image, return_tensors="pt").to(self.device)
            
            # Generate caption
            out = self.model.generate(**inputs, max_length=max_length)
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            
            return caption
        except Exception as e:
            raise Exception(f"Error generating caption locally: {e}")

    def _generate_caption_cloud(self, image):
        """
        Generate caption using Hugging Face Inference API.
        """
        try:
            import requests
            import io
            
            # Convert PIL image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Hugging Face API endpoint
            API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
            
            # Note: For production, use an API token
            # headers = {"Authorization": f"Bearer {API_TOKEN}"}
            headers = {}
            
            response = requests.post(API_URL, headers=headers, data=img_byte_arr)
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'No caption generated')
            elif isinstance(result, dict) and 'generated_text' in result:
                return result['generated_text']
            else:
                return "Unable to generate caption using cloud API"
                
        except Exception as e:
            raise Exception(f"Error generating caption via cloud API: {e}")


if __name__ == "__main__":
    # Test the caption engine
    caption_engine = CaptionEngine(use_cloud=False)
    test_image = Image.new('RGB', (224, 224), color='red')
    caption = caption_engine.generate_caption(test_image)
    print(f"Generated Caption: {caption}")
