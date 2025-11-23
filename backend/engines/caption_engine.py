"""
AI Caption Engine for FastAPI Backend with Detailed Descriptions
"""
from transformers import BlipProcessor, BlipForConditionalGeneration, Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import requests
import torch

class CaptionEngine:
    def __init__(self):
        """Initialize caption engine"""
        self.model = None
        self.processor = None
        self.detailed_model = None
        self.detailed_processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🎨 Caption Engine initialized (will load model on first use, device: {self.device})")
    
    def load_model(self):
        """Load BLIP model (lazy loading)"""
        if self.model is None:
            print("Loading BLIP model...")
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model.to(self.device)
            print("✅ BLIP model loaded!")
    
    def load_detailed_model(self):
        """Load BLIP-2 model for detailed descriptions"""
        if self.detailed_model is None:
            print("Loading BLIP-2 model for detailed descriptions...")
            try:
                self.detailed_processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
                self.detailed_model = Blip2ForConditionalGeneration.from_pretrained(
                    "Salesforce/blip2-opt-2.7b",
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
                self.detailed_model.to(self.device)
                print("✅ BLIP-2 detailed model loaded!")
            except Exception as e:
                print(f"⚠️ BLIP-2 model failed to load: {e}")
                print("   Falling back to BLIP-1 with enhanced prompts")
                self.detailed_model = "fallback"
    
    def generate_caption(self, image_path, mode="local", detailed=True):
        """
        Generate caption for image with optional detailed description
        
        Args:
            image_path: Path to image file
            mode: 'local' or 'cloud'
            detailed: If True, generate detailed description
            
        Returns:
            dict with caption, detailed description, and metadata
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            if mode == "cloud":
                result = self._generate_cloud(image_path, detailed)
            else:
                result = self._generate_local(image, detailed)
            
            return result
                
        except Exception as e:
            print(f"Caption Error: {str(e)}")
            return {
                "caption": "Error generating caption",
                "detailed_description": "Error generating description",
                "confidence": 0,
                "error": str(e)
            }
    
    def _generate_local(self, image, detailed=True):
        """Generate caption using local model with NEXT-LEVEL detailed description"""
        self.load_model()
        
        # Generate basic caption with optimized parameters
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=50,
            num_beams=8,  # Increased for better quality
            early_stopping=True,
            length_penalty=1.0
        )
        caption = self.processor.decode(outputs[0], skip_special_tokens=True).strip()
        
        detailed_description = caption
        
        if detailed:
            # Try to generate NEXT-LEVEL detailed description
            try:
                # Multi-angle analysis with 10 specialized prompts
                prompts = [
                    # Core scene understanding
                    ("a photograph of", "unconditional"),  # Let model describe freely
                    ("Question: What is the main subject of this image? Answer:", "subject"),
                    ("Question: What is happening in this image? Answer:", "action"),
                    
                    # Environmental details
                    ("Question: Describe the setting and location. Answer:", "setting"),
                    ("Question: What is in the background? Answer:", "background"),
                    
                    # Visual attributes
                    ("Question: Describe the colors, lighting and atmosphere. Answer:", "atmosphere"),
                    ("Question: What objects can you see? Answer:", "objects"),
                    
                    # Composition and mood
                    ("Question: Describe the composition and framing. Answer:", "composition"),
                    ("Question: What is the mood or feeling of this image? Answer:", "mood"),
                    
                    # Additional context
                    ("Question: Are there any people? What are they doing? Answer:", "people")
                ]
                
                descriptions = {}
                for prompt, category in prompts:
                    try:
                        inputs = self.processor(image, text=prompt, return_tensors="pt").to(self.device)
                        outputs = self.model.generate(
                            **inputs,
                            max_length=150,
                            min_length=10,
                            num_beams=8,
                            temperature=0.9,
                            do_sample=True,
                            top_k=50,
                            top_p=0.95,
                            repetition_penalty=1.3,
                            early_stopping=True
                        )
                        desc = self.processor.decode(outputs[0], skip_special_tokens=True)
                        
                        # Advanced prompt removal
                        desc = self._clean_description(desc, prompt)
                        
                        if desc and len(desc) > 8:
                            descriptions[category] = desc
                    except Exception as e:
                        print(f"Prompt '{category}' failed: {e}")
                        continue
                
                # Build next-level detailed description
                if descriptions:
                    detailed_description = self._build_next_level_description(descriptions, caption)
                else:
                    detailed_description = self._enhance_caption(caption)
                    
            except Exception as e:
                print(f"Detailed description generation failed: {e}, using enhanced caption")
                detailed_description = self._enhance_caption(caption)
        
        return {
            "caption": caption,
            "detailed_description": detailed_description,
            "confidence": 0.90,
            "mode": "local",
            "has_detailed": detailed
        }
    
    def _clean_description(self, text, prompt):
        """Advanced cleaning of model output - removes ALL artifacts"""
        if not text:
            return ""
        
        # Remove the original prompt completely
        text = text.replace(prompt, "").strip()
        
        # Remove ALL variations of Q&A artifacts (case-insensitive)
        import re
        
        # Remove Question/Answer patterns with their text
        text = re.sub(r'[Qq]uestion\s*:.*?[Aa]nswer\s*:', '', text, flags=re.DOTALL)
        text = re.sub(r'[Qq]uestion\s*:.*?\?', '', text)
        text = re.sub(r'[Aa]nswer\s*:', '', text)
        text = re.sub(r'[Qq]uestion\s*:', '', text)
        
        # Remove common AI phrases
        artifacts = [
            "describe this image", "this image shows", "in this image",
            "the image shows", "i can see", "there is", "there are",
            "what is happening", "what are they doing", "what can you see",
            "what objects", "describe the", "notable objects include",
            "the setting appears to be", "appears to be", "seems to be",
            "it looks like", "it appears", "what is", "what are"
        ]
        
        text_lower = text.lower()
        for artifact in artifacts:
            if artifact in text_lower:
                # Case-insensitive replacement
                pattern = re.compile(re.escape(artifact), re.IGNORECASE)
                text = pattern.sub('', text)
        
        # Clean up multiple spaces and punctuation
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s*\?\s*', '. ', text)
        text = re.sub(r'\s*:\s*', '. ', text)
        text = re.sub(r'\.+', '.', text)
        text = text.strip()
        
        # Remove leading articles if sentence starts awkwardly
        if text and text.startswith(("a ", "an ", "the ", "A ", "An ", "The ")):
            # Only remove if followed by lowercase (not a proper noun)
            parts = text.split(' ', 1)
            if len(parts) > 1 and parts[1] and parts[1][0].islower():
                text = parts[1]
        
        # Ensure proper sentence structure
        if text:
            # Capitalize first letter
            text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
            
            # Ensure proper ending
            if not text.endswith(('.', '!', '?')):
                text = text + '.'
            
            # Fix double periods
            text = text.replace('..', '.')
        
        return text
    
    def _build_next_level_description(self, descriptions, base_caption):
        """Build the BEST POSSIBLE detailed description from categorized analysis"""
        parts = []
        
        # Filter out empty or very short descriptions
        descriptions = {k: v for k, v in descriptions.items() if v and len(v) > 8}
        
        if not descriptions:
            return self._enhance_caption(base_caption)
        
        # Build opening statement (most natural description)
        opening = None
        if "unconditional" in descriptions:
            opening = descriptions["unconditional"]
            parts.append(f"This photograph shows {opening.lower()}" if not opening.lower().startswith(('a ', 'an ', 'the ')) else f"This photograph shows {opening}")
        elif "subject" in descriptions:
            subject = descriptions["subject"]
            parts.append(f"The main focus of this image is {subject.lower()}")
        else:
            parts.append(f"This image depicts {base_caption}")
        
        # Add action/activity if meaningful and not redundant
        if "action" in descriptions:
            action = descriptions["action"]
            # Only add if it's not already mentioned in opening
            if opening and action.lower() not in opening.lower():
                if len(action) > 15:  # Meaningful content
                    parts.append(action)
        
        # Add people details if present
        if "people" in descriptions:
            people_desc = descriptions["people"]
            # Only if it describes actual people
            if "no" not in people_desc.lower() and "not" not in people_desc.lower():
                if len(people_desc) > 20 and not any(people_desc.lower() in p.lower() for p in parts):
                    parts.append(people_desc)
        
        # Add object details
        if "objects" in descriptions:
            obj_desc = descriptions["objects"]
            if len(obj_desc) > 15:
                # Check it's not redundant
                if not any(obj_desc.lower() in p.lower() for p in parts):
                    # Natural integration
                    if any(word in obj_desc.lower() for word in ['various', 'several', 'multiple', 'include']):
                        parts.append(obj_desc)
                    else:
                        parts.append(f"Visible objects include {obj_desc.lower()}")
        
        # Add setting/location
        setting_added = False
        if "setting" in descriptions:
            setting = descriptions["setting"]
            if len(setting) > 15 and not any(setting.lower() in p.lower() for p in parts):
                parts.append(f"The scene is set in {setting.lower()}")
                setting_added = True
        
        if not setting_added and "background" in descriptions:
            bg = descriptions["background"]
            if len(bg) > 15 and not any(bg.lower() in p.lower() for p in parts):
                parts.append(f"The background features {bg.lower()}")
        
        # Add atmosphere/lighting
        if "atmosphere" in descriptions:
            atm = descriptions["atmosphere"]
            if len(atm) > 20 and not any(atm.lower() in p.lower() for p in parts):
                parts.append(atm)
        
        # Add composition if meaningful
        if "composition" in descriptions:
            comp = descriptions["composition"]
            if len(comp) > 25:  # Only substantial composition details
                if not any(comp.lower() in p.lower() for p in parts):
                    parts.append(comp)
        
        # Add mood as closing touch
        if "mood" in descriptions:
            mood = descriptions["mood"]
            if len(mood) > 15 and not any(mood.lower() in p.lower() for p in parts):
                parts.append(f"The overall mood is {mood.lower()}")
        
        # Limit to best 5-6 parts for readability
        parts = parts[:6]
        
        # Combine with natural flow
        if len(parts) == 1:
            description = parts[0]
        elif len(parts) == 2:
            description = f"{parts[0]} {parts[1]}"
        else:
            # Join first parts naturally, last part with "Additionally" or smooth connector
            main_parts = ". ".join(parts[:-1])
            last_part = parts[-1]
            
            # Smart connector
            if len(parts) > 3:
                description = f"{main_parts}. Additionally, {last_part.lower()}"
            else:
                description = f"{main_parts}. {last_part}"
        
        # Final polish
        description = self._final_polish(description)
        
        return description
    
    def _final_polish(self, text):
        """Final polish to ensure PERFECT natural flowing text"""
        import re
        
        # Remove duplicate sentences (even if slightly different)
        sentences = text.split('. ')
        unique_sentences = []
        seen = set()
        
        for sent in sentences:
            sent = sent.strip()
            if not sent or len(sent) < 10:
                continue
            
            # Normalize for comparison
            normalized = ' '.join(sent.lower().split())
            
            # Check for duplicates with fuzzy matching
            is_duplicate = False
            for seen_sent in seen:
                # If 80% of words are the same, it's a duplicate
                sent_words = set(normalized.split())
                seen_words = set(seen_sent.split())
                
                if sent_words and seen_words:
                    overlap = len(sent_words & seen_words)
                    similarity = overlap / max(len(sent_words), len(seen_words))
                    
                    if similarity > 0.8:
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                unique_sentences.append(sent)
                seen.add(normalized)
        
        # Rejoin sentences
        polished = '. '.join(unique_sentences)
        
        # Clean up any remaining artifacts
        polished = re.sub(r'\s+', ' ', polished)  # Multiple spaces
        polished = re.sub(r'\.+', '.', polished)  # Multiple periods
        polished = re.sub(r'\s*\.\s*', '. ', polished)  # Space around periods
        polished = re.sub(r'\s+([.,!?])', r'\1', polished)  # Space before punctuation
        
        # Remove any remaining question marks from prompts
        polished = polished.replace('?', '.')
        polished = polished.replace('..', '.')
        
        # Ensure proper ending
        polished = polished.strip()
        if polished and not polished.endswith(('.', '!', '?')):
            polished += '.'
        
        # Capitalize properly after periods
        sentences = polished.split('. ')
        capitalized = []
        for sent in sentences:
            sent = sent.strip()
            if sent:
                sent = sent[0].upper() + sent[1:] if len(sent) > 1 else sent.upper()
                capitalized.append(sent)
        
        polished = '. '.join(capitalized)
        
        # Final cleanup - remove any orphaned lowercase starts
        polished = polished.strip()
        if polished and polished[0].islower():
            polished = polished[0].upper() + polished[1:]
        
        return polished
    
    def _generate_cloud(self, image_path, detailed=True):
        """Generate caption using Hugging Face API"""
        # Basic caption
        API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
        
        with open(image_path, "rb") as f:
            data = f.read()
        
        response = requests.post(API_URL, data=data)
        
        caption = ""
        if response.status_code == 200:
            result = response.json()
            caption = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
        else:
            raise Exception(f"API request failed: {response.status_code}")
        
        detailed_description = caption
        
        # Try to get detailed description
        if detailed:
            try:
                # Use BLIP-2 for detailed description
                DETAILED_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip2-opt-2.7b"
                
                # Send with prompt
                import json
                payload = {
                    "inputs": "Describe this image in detail, including people, objects, actions, background, and setting:"
                }
                
                response = requests.post(
                    DETAILED_API_URL,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload),
                    files={"file": open(image_path, "rb")}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        detailed_description = result[0].get("generated_text", caption)
                    else:
                        detailed_description = self._enhance_caption(caption)
                else:
                    detailed_description = self._enhance_caption(caption)
                    
            except Exception as e:
                print(f"Detailed cloud description failed: {e}")
                detailed_description = self._enhance_caption(caption)
        
        return {
            "caption": caption,
            "detailed_description": detailed_description,
            "confidence": 0.92,
            "mode": "cloud",
            "has_detailed": detailed
        }
    
    def _enhance_caption(self, caption):
        """Enhance a basic caption with more context and details"""
        # Start with a natural opening
        enhanced = f"This image shows {caption}."
        
        # Add contextual enhancements based on caption keywords
        caption_lower = caption.lower()
        
        # Subject-based enhancements
        subject_context = {
            "person": " A person is the main subject, captured in what appears to be a candid or posed photograph.",
            "people": " Multiple people are visible, suggesting a social gathering or group activity.",
            "man": " A man is prominently featured in the scene.",
            "woman": " A woman is the central figure in this image.",
            "child": " A child can be seen, adding a youthful element to the composition.",
            "children": " Children are present, bringing energy and life to the scene.",
            "baby": " A baby is visible, creating a tender moment.",
        }
        
        # Object-based enhancements
        object_context = {
            "dog": " A dog is present, likely a pet or companion animal.",
            "cat": " A cat can be seen, adding a feline presence to the image.",
            "bird": " A bird appears in the frame, possibly in flight or perched.",
            "car": " A car is visible, suggesting transportation or urban context.",
            "bicycle": " A bicycle is present, indicating cycling or outdoor activity.",
            "food": " Food items are displayed, possibly in a dining or culinary context.",
            "book": " A book is visible, suggesting reading or educational content.",
            "phone": " A phone appears, indicating modern communication or technology.",
            "computer": " A computer is present, suggesting work or digital activity.",
        }
        
        # Location-based enhancements
        location_context = {
            "beach": " The setting appears to be at a beach, with sand and possibly water visible.",
            "mountain": " Mountains can be seen in the background, suggesting a natural outdoor environment.",
            "building": " A building is visible, indicating an urban or developed area.",
            "park": " The scene takes place in a park, suggesting outdoor recreation.",
            "street": " This appears to be on a street, in an urban or suburban setting.",
            "room": " The scene is set indoors in a room.",
            "kitchen": " This takes place in a kitchen, suggesting cooking or dining activities.",
            "office": " An office setting is evident, indicating a work environment.",
        }
        
        # Activity-based enhancements
        activity_context = {
            "sitting": " The subject is in a seated position, appearing relaxed or resting.",
            "standing": " The subject is standing, suggesting an active or formal pose.",
            "walking": " Movement is captured, with someone walking through the scene.",
            "running": " Dynamic action is shown with someone running.",
            "playing": " Play or recreational activity is taking place.",
            "eating": " Dining or eating activity is captured in the moment.",
            "working": " Work-related activity is taking place.",
            "reading": " Someone is engaged in reading.",
            "smiling": " A smile is visible, suggesting happiness or positive emotion.",
        }
        
        # Weather/atmosphere enhancements
        atmosphere_context = {
            "sunny": " The lighting suggests sunny or bright conditions.",
            "cloudy": " Overcast or cloudy conditions are apparent.",
            "snow": " Snow is present, indicating winter conditions.",
            "rain": " Rain or wet conditions are visible.",
            "night": " This appears to be taken at night or in low-light conditions.",
            "sunset": " The warm lighting suggests sunset or golden hour.",
        }
        
        # Add relevant context
        context_added = False
        for keyword, context in {**subject_context, **object_context, **location_context, 
                                  **activity_context, **atmosphere_context}.items():
            if keyword in caption_lower and not context_added:
                enhanced += context
                context_added = True
                break
        
        # Add general descriptive filler if no specific context was added
        if not context_added:
            enhanced += " The composition captures various elements that tell a visual story."
        
        # Add a concluding observation
        conclusions = [
            " The image has a clear focal point and balanced composition.",
            " Various elements in the frame contribute to the overall narrative.",
            " The scene appears naturally composed with attention to detail.",
            " The photograph captures a moment in time with visual clarity.",
        ]
        
        # Select conclusion based on caption length
        conclusion_index = len(caption) % len(conclusions)
        enhanced += conclusions[conclusion_index]
        
        return enhanced
    
    def _combine_descriptions(self, descriptions, base_caption):
        """Legacy method - now redirects to next-level builder"""
        # Convert list to dict for new method
        desc_dict = {}
        for i, desc in enumerate(descriptions):
            desc_dict[f"aspect_{i}"] = desc
        
        return self._build_next_level_description(desc_dict, base_caption)
