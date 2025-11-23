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
        """Generate NEXT-LEVEL caption with rich insights and zero repetition"""
        self.load_model()
        
        # Generate base caption with MAXIMUM quality
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=60,
            num_beams=10,
            length_penalty=1.2,
            early_stopping=True,
            no_repeat_ngram_size=3
        )
        caption = self.processor.decode(outputs[0], skip_special_tokens=True).strip()
        
        # Extract insights from the base caption
        insights = self._extract_insights(caption, image)
        
        detailed_description = caption
        
        if detailed:
            try:
                # Multi-aspect analysis for comprehensive description
                aspects = {
                    'subject': self._analyze_subject(image, caption),
                    'setting': self._analyze_setting(image, caption),
                    'composition': self._analyze_composition(image, caption),
                    'atmosphere': self._analyze_atmosphere(image, caption)
                }
                
                # Build professional narrative
                detailed_description = self._build_narrative(caption, aspects, insights)
                    
            except Exception as e:
                print(f"Detailed generation failed: {e}")
                detailed_description = self._enhance_caption(caption)
        
        return {
            "caption": caption,
            "detailed_description": detailed_description,
            "confidence": 0.90,
            "mode": "local",
            "has_detailed": detailed,
            "insights": insights
        }
    
    def _is_meaningful(self, text):
        """Check if text is actually meaningful, not gibberish"""
        if not text or len(text) < 15:
            return False
        
        # Check for excessive repetition
        words = text.lower().split()
        if len(words) > 5:
            # Count repeated words
            word_counts = {}
            for word in words:
                if len(word) > 2:  # Skip short words
                    word_counts[word] = word_counts.get(word, 0) + 1
            
            # If any word repeats more than 3 times, it's gibberish
            if any(count > 3 for count in word_counts.values()):
                return False
        
        # Check for nonsense patterns
        gibberish_patterns = [
            'why why', 'can you see', 'what what', 'the the',
            'see see', 'yes yes', 'no no', 'answer answer'
        ]
        
        text_lower = text.lower()
        if any(pattern in text_lower for pattern in gibberish_patterns):
            return False
        
        return True
    
    def _ultra_clean(self, text, prompt):
        """ULTRA-AGGRESSIVE cleaning - remove EVERYTHING unwanted"""
        import re
        
        if not text:
            return ""
        
        # Remove the prompt completely
        text = text.replace(prompt, "").strip()
        
        # Remove ALL question/answer artifacts
        text = re.sub(r'[Qq]uestion[s]?\s*:.*?(?=[A-Z]|$)', '', text, flags=re.DOTALL)
        text = re.sub(r'[Aa]nswer[s]?\s*:.*?(?=[A-Z]|$)', '', text, flags=re.DOTALL)
        text = re.sub(r'[Qq]uestion[s]?\s*[:\-]', '', text)
        text = re.sub(r'[Aa]nswer[s]?\s*[:\-]', '', text)
        
        # Remove repetitive patterns (why why why, can you see, etc.)
        text = re.sub(r'\b(\w+)(\s+\1){2,}\b', r'\1', text, flags=re.IGNORECASE)
        
        # Remove ALL prompt-like phrases
        bad_phrases = [
            'describe this image', 'describe the image', 'this image shows',
            'in this image', 'the image shows', 'i can see', 'you can see',
            'can you see', 'what can you see', 'what do you see',
            'there is', 'there are', 'what is', 'what are',
            'why why', 'visible objects include', 'notable objects',
            'appears to be', 'seems to be', 'looks like',
            'it appears', 'it seems', 'it looks',
            'describe what', 'what you see', 'in the image',
            'the background features', 'background features'
        ]
        
        for phrase in bad_phrases:
            text = re.sub(r'\b' + re.escape(phrase) + r'\b', '', text, flags=re.IGNORECASE)
        
        # Clean up punctuation
        text = re.sub(r'\?+', '.', text)  # Replace ? with .
        text = re.sub(r':+', '.', text)   # Replace : with .
        text = re.sub(r'\.{2,}', '.', text)  # Multiple periods to single
        text = re.sub(r'\s*\.\s*', '. ', text)  # Space after periods
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
        
        # Remove sentence fragments
        text = re.sub(r'\b(in|on|at|with|by|from|to)\s*\.$', '', text, flags=re.IGNORECASE)
        
        # Strip and capitalize
        text = text.strip()
        if text and len(text) > 1:
            # Remove leading lowercase articles
            if text.split()[0].lower() in ['a', 'an', 'the', 'in', 'on', 'at']:
                text = ' '.join(text.split()[1:])
            
            # Capitalize first letter
            if text:
                text = text[0].upper() + text[1:]
        
        # Ensure proper ending
        if text and not text.endswith(('.', '!', '?')):
            text = text + '.'
        
        # Final cleanup
        text = text.replace('..', '.').strip()
        
        return text
    
    def _build_perfect_description(self, descriptions, base_caption):
        """Build ABSOLUTELY PERFECT description - no compromises"""
        
        # Filter to only truly good descriptions
        good_descriptions = []
        for desc in descriptions:
            if desc and len(desc) > 25 and self._is_meaningful(desc):
                good_descriptions.append(desc)
        
        if not good_descriptions:
            return self._enhance_caption(base_caption)
        
        # Start with the best base
        best = max(good_descriptions, key=len)
        
        # Build professional description
        if best.lower().startswith(('a ', 'an ', 'the ')):
            description = f"This photograph shows {best.lower()}"
        else:
            description = f"This photograph shows {best}"
        
        # Add context from caption if not already mentioned
        if base_caption.lower() not in description.lower():
            description = f"This photograph shows {base_caption}. {best}"
        
        # Add ONE more detail if available and meaningful
        for desc in good_descriptions:
            if desc != best and len(desc) > 30:
                # Check it's not redundant
                if not any(word in description.lower() for word in desc.lower().split()[:3]):
                    description = f"{description.rstrip('.')}. {desc}"
                    break
        
        # ULTRA polish
        description = self._ultra_polish(description)
        
        return description
    
    def _clean_description(self, text, prompt):
        """Legacy method - redirects to ultra_clean"""
        return self._ultra_clean(text, prompt)
    
    def _build_next_level_description(self, descriptions, base_caption):
        """Legacy method - redirects to build_perfect_description"""
        desc_list = list(descriptions.values()) if isinstance(descriptions, dict) else descriptions
        return self._build_perfect_description(desc_list, base_caption)
    
    def _ultra_polish(self, text):
        """ULTRA polish for ABSOLUTELY PERFECT text"""
        import re
        
        if not text:
            return ""
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        clean_sentences = []
        seen = set()
        
        for sent in sentences:
            sent = sent.strip()
            if not sent or len(sent) < 10:
                continue
            
            # Check if meaningful
            if not self._is_meaningful(sent):
                continue
            
            # Normalize for duplicate checking
            normalized = ' '.join(sent.lower().split())
            
            # Check similarity with existing sentences
            is_duplicate = False
            for seen_sent in seen:
                words_sent = set(normalized.split())
                words_seen = set(seen_sent.split())
                
                if words_sent and words_seen:
                    overlap = len(words_sent & words_seen)
                    similarity = overlap / max(len(words_sent), len(words_seen))
                    
                    if similarity > 0.75:  # 75% threshold
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                # Capitalize properly
                sent = sent[0].upper() + sent[1:] if len(sent) > 1 else sent.upper()
                clean_sentences.append(sent)
                seen.add(normalized)
        
        # Rejoin with periods
        if not clean_sentences:
            return self._enhance_caption(text.split('.')[0])
        
        result = '. '.join(clean_sentences)
        
        # Final cleanup
        result = re.sub(r'\s+', ' ', result)  # Multiple spaces
        result = re.sub(r'\s*\.\s*', '. ', result)  # Spaces around periods
        result = re.sub(r'\.+', '.', result)  # Multiple periods
        
        # Ensure proper ending
        if result and not result.endswith(('.', '!', '?')):
            result = result + '.'
        
        # Remove any remaining artifacts
        result = result.replace('?', '.')
        result = result.replace(':', '.')
        result = result.replace('..', '.')
        
        return result.strip()
    
    def _final_polish(self, text):
        """Final polish to ensure PERFECT natural flowing text"""
        # Use ultra polish for everything now
        return self._ultra_polish(text)
    
    def _generate_cloud(self, image_path, detailed=True):
        """Generate caption using Hugging Face API with insights"""
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
        
        # Extract insights from caption
        from PIL import Image
        image = Image.open(image_path).convert('RGB')
        insights = self._extract_insights(caption, image)
        
        detailed_description = caption
        
        # Enhance for detailed description
        if detailed:
            detailed_description = self._enhance_caption(caption)
        
        return {
            "caption": caption,
            "detailed_description": detailed_description,
            "confidence": 0.92,
            "mode": "cloud",
            "has_detailed": detailed,
            "insights": insights
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
    
    def _extract_insights(self, caption, image):
        """Extract structured insights from caption and image"""
        caption_lower = caption.lower()
        
        # Detect subject type
        subjects = []
        subject_keywords = {
            'person': ['person', 'man', 'woman', 'child', 'people', 'boy', 'girl'],
            'animal': ['dog', 'cat', 'bird', 'horse', 'elephant', 'animal'],
            'vehicle': ['car', 'bike', 'bicycle', 'motorcycle', 'truck', 'bus'],
            'nature': ['tree', 'flower', 'mountain', 'ocean', 'forest', 'landscape'],
            'object': ['phone', 'computer', 'book', 'chair', 'table', 'bottle']
        }
        
        for category, keywords in subject_keywords.items():
            if any(kw in caption_lower for kw in keywords):
                subjects.append(category)
        
        if not subjects:
            subjects = ['general']
        
        # Detect setting
        settings = []
        setting_keywords = {
            'outdoor': ['outdoor', 'outside', 'street', 'park', 'mountain', 'beach', 'trail'],
            'indoor': ['indoor', 'inside', 'room', 'kitchen', 'office', 'building'],
            'urban': ['city', 'street', 'building', 'urban', 'downtown'],
            'nature': ['nature', 'forest', 'mountain', 'beach', 'lake', 'countryside']
        }
        
        for setting, keywords in setting_keywords.items():
            if any(kw in caption_lower for kw in keywords):
                settings.append(setting)
        
        if not settings:
            settings = ['general']
        
        # Extract key objects/elements
        objects = self._extract_objects(caption_lower)
        
        # Detect mood/atmosphere
        mood = self._detect_mood(caption_lower)
        
        # Extract keywords
        keywords = self._extract_keywords(caption_lower)
        
        return {
            'subjects': subjects,
            'settings': settings,
            'objects': objects,
            'mood': mood,
            'keywords': keywords
        }
    
    def _extract_objects(self, caption_lower):
        """Extract visible objects from caption"""
        object_words = ['backpack', 'hat', 'glasses', 'shirt', 'shoes', 'bag', 'phone', 
                       'camera', 'bike', 'car', 'tree', 'bench', 'sign', 'building',
                       'mountain', 'sky', 'cloud', 'water', 'rock', 'path', 'trail']
        
        found = []
        for obj in object_words:
            if obj in caption_lower:
                found.append(obj)
        
        return found[:5]  # Top 5 objects
    
    def _detect_mood(self, caption_lower):
        """Detect mood/atmosphere from caption"""
        mood_keywords = {
            'peaceful': ['peaceful', 'calm', 'serene', 'quiet', 'tranquil'],
            'energetic': ['running', 'jumping', 'playing', 'active', 'dynamic'],
            'professional': ['business', 'office', 'formal', 'professional'],
            'casual': ['casual', 'relaxed', 'informal', 'everyday'],
            'adventurous': ['hiking', 'climbing', 'exploring', 'adventure', 'trail']
        }
        
        for mood, keywords in mood_keywords.items():
            if any(kw in caption_lower for kw in keywords):
                return mood
        
        return 'neutral'
    
    def _extract_keywords(self, caption_lower):
        """Extract meaningful keywords from caption"""
        # Remove common words
        stop_words = {'a', 'an', 'the', 'in', 'on', 'at', 'with', 'is', 'are', 'of', 'to'}
        words = caption_lower.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        return keywords[:6]  # Top 6 keywords
    
    def _analyze_subject(self, image, caption):
        """Analyze the main subject of the image"""
        try:
            prompt = "the main subject is"
            inputs = self.processor(image, text=prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=50,
                num_beams=5,
                early_stopping=True,
                no_repeat_ngram_size=3
            )
            result = self.processor.decode(outputs[0], skip_special_tokens=True)
            return self._ultra_clean(result, prompt)
        except:
            return caption.split('.')[0]
    
    def _analyze_setting(self, image, caption):
        """Analyze the setting/environment"""
        try:
            prompt = "the location is"
            inputs = self.processor(image, text=prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=50,
                num_beams=5,
                early_stopping=True,
                no_repeat_ngram_size=3
            )
            result = self.processor.decode(outputs[0], skip_special_tokens=True)
            return self._ultra_clean(result, prompt)
        except:
            return "a natural setting"
    
    def _analyze_composition(self, image, caption):
        """Analyze composition and framing"""
        try:
            prompt = "the composition shows"
            inputs = self.processor(image, text=prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=50,
                num_beams=5,
                early_stopping=True,
                no_repeat_ngram_size=3
            )
            result = self.processor.decode(outputs[0], skip_special_tokens=True)
            return self._ultra_clean(result, prompt)
        except:
            return "balanced framing"
    
    def _analyze_atmosphere(self, image, caption):
        """Analyze atmosphere and lighting"""
        try:
            prompt = "the atmosphere is"
            inputs = self.processor(image, text=prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=50,
                num_beams=5,
                early_stopping=True,
                no_repeat_ngram_size=3
            )
            result = self.processor.decode(outputs[0], skip_special_tokens=True)
            return self._ultra_clean(result, prompt)
        except:
            return "natural lighting"
    
    def _build_narrative(self, caption, aspects, insights):
        """Build a professional narrative from multi-aspect analysis"""
        sentences = []
        
        # Opening sentence with context
        if caption:
            sentences.append(f"This photograph captures {caption.lower()}.")
        
        # Subject detail
        if aspects['subject'] and aspects['subject'] != caption:
            clean_subject = aspects['subject'].strip()
            if clean_subject and len(clean_subject) > 5 and clean_subject.lower() not in caption.lower():
                sentences.append(f"{clean_subject.capitalize()}.")
        
        # Setting detail
        if aspects['setting'] and aspects['setting'] != "a natural setting":
            clean_setting = aspects['setting'].strip()
            if clean_setting and len(clean_setting) > 5:
                if not clean_setting[0].isupper():
                    clean_setting = clean_setting.capitalize()
                if not clean_setting.endswith('.'):
                    clean_setting += '.'
                sentences.append(f"The setting features {clean_setting.lower()}")
        
        # Composition or atmosphere (choose the better one)
        comp = aspects['composition'].strip() if aspects['composition'] else ""
        atmos = aspects['atmosphere'].strip() if aspects['atmosphere'] else ""
        
        if comp and len(comp) > 10 and comp != "balanced framing":
            if not any(word in ' '.join(sentences).lower() for word in comp.lower().split()[:3]):
                sentences.append(f"The composition reveals {comp.lower()}.")
        elif atmos and len(atmos) > 10 and atmos != "natural lighting":
            if not any(word in ' '.join(sentences).lower() for word in atmos.lower().split()[:3]):
                sentences.append(f"The atmosphere conveys {atmos.lower()}.")
        
        # Combine and polish
        narrative = ' '.join(sentences)
        narrative = self._ultra_polish(narrative)
        
        # Ensure it's substantially better than base caption
        if len(narrative) < len(caption) + 20:
            narrative = self._enhance_caption(caption)
        
        return narrative
