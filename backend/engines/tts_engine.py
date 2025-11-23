"""
Text-to-Speech Engine for FastAPI Backend
"""
import subprocess
import platform
from pathlib import Path
import uuid
import re
from deep_translator import GoogleTranslator

# Only import pyttsx3 on macOS
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except:
    PYTTSX3_AVAILABLE = False

# Import gTTS for Linux servers
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except:
    GTTS_AVAILABLE = False

class TTSEngine:
    def __init__(self):
        """Initialize TTS engine"""
        self.system = platform.system()
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)
        self.engine = None
        
        # Only initialize pyttsx3 on macOS
        if self.system == "Darwin" and PYTTSX3_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
            except Exception as e:
                print(f"⚠️ pyttsx3 initialization failed: {e}")
                self.engine = None
        
        print(f"🎧 TTS Engine initialized ({self.system}, gTTS: {GTTS_AVAILABLE}, pyttsx3: {PYTTSX3_AVAILABLE})")
        self.lang_codes = {
            'hi': 'hi',     # Hindi
            'bn': 'bn',     # Bengali
            'ta': 'ta',     # Tamil
            'te': 'te',     # Telugu
            'kn': 'kn',     # Kannada
            'ml': 'ml',     # Malayalam
            'gu': 'gu',     # Gujarati
            'mr': 'mr',     # Marathi
            'pa': 'pa',     # Punjabi
            'or': 'or',     # Odia
            'as': 'as',     # Assamese
            'ur': 'ur',     # Urdu
            'ar': 'ar',     # Arabic
            'es': 'es',     # Spanish
            'fr': 'fr',     # French
            'de': 'de',     # German
            'it': 'it',     # Italian
            'pt': 'pt',     # Portuguese
            'ru': 'ru',     # Russian
            'ja': 'ja',     # Japanese
            'ko': 'ko',     # Korean
            'zh': 'zh-CN',  # Chinese
            'th': 'th',     # Thai
            'tr': 'tr',     # Turkish
            'nl': 'nl',     # Dutch
            'sv': 'sv',     # Swedish
            'id': 'id',     # Indonesian
            'vi': 'vi',     # Vietnamese
        }
        
        print(f"🎧 TTS Engine initialized ({self.system})")
    
    def _is_english_text(self, text):
        """Check if text is primarily English (Latin alphabet)"""
        # Remove spaces and punctuation
        clean_text = re.sub(r'[^\w]', '', text)
        if not clean_text:
            return True
        
        # Count Latin characters (English, European languages)
        latin_chars = len(re.findall(r'[a-zA-Z]', clean_text))
        total_chars = len(clean_text)
        
        # If more than 80% Latin characters, consider it English
        return (latin_chars / total_chars) > 0.8 if total_chars > 0 else True
    
    def _translate_if_needed(self, text, language):
        """Translate text to target language if it's in English"""
        # Don't translate if already English or if language not supported
        if language.lower() in ['en', 'en-us', 'en-gb', 'en-au']:
            return text
        
        # Check if text is English
        if not self._is_english_text(text):
            print(f"  Text appears to be in target language already, no translation needed")
            return text
        
        # Translate English to target language
        target_lang = self.lang_codes.get(language.lower())
        if not target_lang:
            print(f"  Translation not supported for {language}, using original text")
            return text
        
        try:
            translator = GoogleTranslator(source='auto', target=target_lang)
            translated = translator.translate(text)
            print(f"  📝 Auto-translated: '{text[:50]}...' → '{translated[:50]}...' ({language})")
            return translated
        except Exception as e:
            print(f"  ⚠ Translation failed: {e}, using original text")
            return text
    
    def generate_speech(self, text, language="en", rate=200):
        """
        Generate speech from text with auto-translation
        
        Args:
            text: Text to convert to speech
            language: Language code
            rate: Speech rate (50-400)
            
        Returns:
            dict with audio file path
        """
        try:
            # Auto-translate if needed (English → target language)
            processed_text = self._translate_if_needed(text, language)
            
            # Generate unique filename
            audio_file = self.output_dir / f"speech_{uuid.uuid4()}.mp3"
            
            if self.system == "Darwin":  # macOS
                # For macOS, use AIFF format with 'say' command
                audio_file = self.output_dir / f"speech_{uuid.uuid4()}.aiff"
                return self._generate_macos(processed_text, language, rate, audio_file)
            elif GTTS_AVAILABLE:
                # For Linux/servers, use gTTS (Google TTS)
                return self._generate_gtts(processed_text, language, audio_file)
            elif self.engine is not None:
                # Fallback to pyttsx3 if available
                audio_file = self.output_dir / f"speech_{uuid.uuid4()}.wav"
                return self._generate_pyttsx3(processed_text, language, rate, audio_file)
            else:
                raise Exception("No TTS engine available. Please install gTTS or pyttsx3.")
                
        except Exception as e:
            print(f"TTS Error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_macos(self, text, language, rate, audio_file):
        """Generate speech using macOS 'say' command with enhanced language support"""
        # Enhanced voice mapping with better language-specific voices
        voice_map = {
            # English variants
            "en": "Alex",           # English (US) - Clear male voice
            "en-us": "Alex",        # English (US)
            "en-gb": "Daniel",      # English (UK)
            "en-au": "Karen",       # English (Australia)
            
            # Indian languages
            "hi": "Lekha",          # Hindi - Female voice (native)
            "kn": "Soumya",         # Kannada - Female voice (native)
            "bn": "Piya",           # Bengali - Female voice (native)
            "ta": "Vani",           # Tamil - Female voice (native)
            "te": "Geeta",          # Telugu - Female voice (native)
            "ml": "Lekha",          # Malayalam - Using Hindi voice (no native voice)
            "gu": "Lekha",          # Gujarati - Using Hindi voice (no native voice)
            "mr": "Lekha",          # Marathi - Using Hindi voice (no native voice)
            "pa": "Lekha",          # Punjabi - Using Hindi voice (no native voice)
            "or": "Lekha",          # Odia - Using Hindi voice (no native voice)
            "as": "Lekha",          # Assamese - Using Hindi voice (no native voice)
            "ur": "Majed",          # Urdu - Using Arabic voice (similar script)
            
            # Middle Eastern
            "ar": "Majed",          # Arabic - Male voice
            
            # European languages
            "es": "Monica",         # Spanish - Female voice
            "es-mx": "Paulina",     # Spanish (Mexico)
            "fr": "Thomas",         # French - Male voice
            "de": "Anna",           # German - Female voice
            "it": "Alice",          # Italian - Female voice
            "pt": "Luciana",        # Portuguese - Female voice
            "ru": "Yuri",           # Russian - Male voice
            "nl": "Xander",         # Dutch - Male voice
            "sv": "Alva",           # Swedish - Female voice
            "no": "Nora",           # Norwegian - Female voice
            "da": "Sara",           # Danish - Female voice
            "fi": "Satu",           # Finnish - Female voice
            "pl": "Zosia",          # Polish - Female voice
            "tr": "Yelda",          # Turkish - Female voice
            
            # Asian languages
            "ja": "Kyoko",          # Japanese - Female voice
            "ko": "Yuna",           # Korean - Female voice
            "zh": "Tingting",       # Chinese (Mandarin) - Female voice
            "zh-cn": "Tingting",    # Chinese (China)
            "zh-tw": "Mei-Jia",     # Chinese (Taiwan)
            "th": "Kanya",          # Thai - Female voice
            "id": "Damayanti",      # Indonesian - Female voice
            "vi": "Linh",           # Vietnamese - Female voice
        }
        
        # Get the appropriate voice for the language
        voice = voice_map.get(language.lower(), "Alex")
        
        # Adjust rate based on language (some languages sound better at different rates)
        adjusted_rate = rate
        # Indian languages, Asian languages, and Arabic - slower for better clarity
        if language.lower() in ["hi", "bn", "ta", "te", "kn", "ml", "gu", "mr", "pa", "or", "as", "ur", "ar", "ja", "ko", "zh", "th", "vi"]:
            adjusted_rate = int(rate * 0.85)
        
        # Generate AIFF file first
        temp_aiff = audio_file
        
        # Run say command to generate AIFF
        cmd = [
            "say", 
            "-v", voice, 
            "-r", str(adjusted_rate),
            "-o", str(temp_aiff),
            text
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✓ Generated speech: {voice} ({language}) at rate {adjusted_rate}")
        except subprocess.CalledProcessError as e:
            print(f"✗ TTS generation failed: {e.stderr}")
            # Try with default voice if language-specific voice fails
            if voice != "Alex":
                print(f"  Retrying with default voice (Alex)...")
                cmd[2] = "Alex"
                subprocess.run(cmd, check=True)
        
        # Convert AIFF to WAV using ffmpeg if available, otherwise return AIFF
        wav_file = audio_file.with_suffix('.wav')
        try:
            convert_cmd = [
                "ffmpeg", 
                "-i", str(temp_aiff), 
                "-acodec", "pcm_s16le",  # PCM 16-bit
                "-ar", "44100",           # 44.1kHz sample rate
                "-ac", "1",               # Mono channel
                str(wav_file), 
                "-y",
                "-loglevel", "error"      # Suppress ffmpeg output
            ]
            result = subprocess.run(convert_cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                # Conversion successful, remove AIFF and use WAV
                temp_aiff.unlink()
                print(f"✓ Converted to WAV format")
                return {
                    "success": True,
                    "audio_file": str(wav_file),
                    "voice": voice,
                    "language": language,
                    "format": "wav",
                    "rate": adjusted_rate
                }
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            # ffmpeg not available or conversion failed, use AIFF
            print(f"⚠ FFmpeg conversion skipped: {str(e)}")
            pass
        
        return {
            "success": True,
            "audio_file": str(temp_aiff),
            "voice": voice,
            "language": language,
            "format": "aiff",
            "rate": adjusted_rate
        }
    
    def _generate_gtts(self, text, language, audio_file):
        """Generate speech using Google TTS (gTTS) - Works on Linux servers"""
        if not GTTS_AVAILABLE:
            raise Exception("gTTS not available. Please install: pip install gTTS")
        
        # Map language codes to gTTS compatible codes
        gtts_lang_map = {
            'en': 'en', 'en-us': 'en', 'en-gb': 'en', 'en-au': 'en',
            'hi': 'hi',  # Hindi
            'kn': 'kn',  # Kannada  
            'bn': 'bn',  # Bengali
            'ta': 'ta',  # Tamil
            'te': 'te',  # Telugu
            'ml': 'ml',  # Malayalam
            'gu': 'gu',  # Gujarati
            'mr': 'mr',  # Marathi
            'pa': 'pa',  # Punjabi
            'ur': 'ur',  # Urdu
            'ar': 'ar',  # Arabic
            'es': 'es',  # Spanish
            'fr': 'fr',  # French
            'de': 'de',  # German
            'it': 'it',  # Italian
            'pt': 'pt',  # Portuguese
            'ru': 'ru',  # Russian
            'ja': 'ja',  # Japanese
            'ko': 'ko',  # Korean
            'zh': 'zh-cn',  # Chinese
            'th': 'th',  # Thai
            'tr': 'tr',  # Turkish
            'nl': 'nl',  # Dutch
            'sv': 'sv',  # Swedish
            'id': 'id',  # Indonesian
            'vi': 'vi',  # Vietnamese
        }
        
        # Get gTTS language code
        gtts_lang = gtts_lang_map.get(language.lower(), 'en')
        
        try:
            # Generate speech using gTTS
            tts = gTTS(text=text, lang=gtts_lang, slow=False)
            tts.save(str(audio_file))
            
            print(f"✓ Generated speech with gTTS: {gtts_lang}")
            
            return {
                "success": True,
                "audio_file": str(audio_file),
                "engine": "gTTS",
                "language": language,
                "format": "mp3"
            }
        except Exception as e:
            print(f"✗ gTTS generation failed: {e}")
            raise
    
    def _generate_pyttsx3(self, text, language, rate, audio_file):
        """Generate speech using pyttsx3 with language support"""
        # Set properties for better quality
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', 0.9)
        
        # Try to find a voice matching the language
        voices = self.engine.getProperty('voices')
        selected_voice = None
        
        # Language code mapping
        lang_prefixes = {
            # Indian languages
            'hi': 'hindi',
            'bn': 'bengali',
            'ta': 'tamil',
            'te': 'telugu',
            'kn': 'kannada',
            'ml': 'malayalam',
            'gu': 'gujarati',
            'mr': 'marathi',
            'pa': 'punjabi',
            'or': 'odia',
            'as': 'assamese',
            'ur': 'urdu',
            # Other languages
            'en': 'english',
            'es': 'spanish',
            'fr': 'french',
            'de': 'german',
            'ja': 'japanese',
            'ko': 'korean',
            'zh': 'chinese',
            'ar': 'arabic',
            'it': 'italian',
            'pt': 'portuguese',
            'ru': 'russian',
            'tr': 'turkish',
            'th': 'thai',
            'id': 'indonesian',
            'vi': 'vietnamese'
        }
        
        # Try to find a matching voice
        lang_name = lang_prefixes.get(language.lower().split('-')[0], 'english')
        for voice in voices:
            if lang_name.lower() in voice.name.lower():
                selected_voice = voice.id
                print(f"✓ Selected voice: {voice.name} for {language}")
                break
        
        if selected_voice:
            self.engine.setProperty('voice', selected_voice)
        else:
            print(f"⚠ No specific voice found for {language}, using default")
        
        # Adjust rate for Indian and Asian languages
        adjusted_rate = rate
        if language.lower() in ['hi', 'bn', 'ta', 'te', 'kn', 'ml', 'gu', 'mr', 'pa', 'or', 'as', 'ur', 'ar', 'ja', 'ko', 'zh', 'th', 'vi']:
            adjusted_rate = int(rate * 0.85)
            self.engine.setProperty('rate', adjusted_rate)
        
        # Generate speech
        self.engine.save_to_file(text, str(audio_file))
        self.engine.runAndWait()
        
        return {
            "success": True,
            "audio_file": str(audio_file),
            "engine": "pyttsx3",
            "language": language,
            "rate": adjusted_rate
        }
    
    def get_available_voices(self):
        """Get list of high-quality voices - Focus on English, Hindi, and Kannada"""
        if self.system == "Darwin" and self.engine is not None:
            # macOS with pyttsx3
            return [
                # English variants - Premium quality
                {"code": "en", "name": "English (US) - Premium", "voice": "Alex", "gender": "male", "quality": "premium"},
                {"code": "en-gb", "name": "English (UK) - Premium", "voice": "Daniel", "gender": "male", "quality": "premium"},
                {"code": "en-au", "name": "English (Australia)", "voice": "Karen", "gender": "female", "quality": "high"},
                
                # Hindi - Premium quality native voice
                {"code": "hi", "name": "हिंदी Hindi - Premium", "voice": "Lekha", "gender": "female", "quality": "premium"},
                
                # Kannada - Premium quality native voice
                {"code": "kn", "name": "ಕನ್ನಡ Kannada - Premium", "voice": "Soumya", "gender": "female", "quality": "premium"},
            ]
        elif GTTS_AVAILABLE:
            # Linux/Server with gTTS - Return supported languages
            return [
                # English variants
                {"code": "en", "name": "English (US) - Premium", "engine": "gTTS", "quality": "premium"},
                {"code": "en-gb", "name": "English (UK)", "engine": "gTTS", "quality": "high"},
                
                # Hindi - Premium quality
                {"code": "hi", "name": "हिंदी Hindi - Premium", "engine": "gTTS", "quality": "premium"},
                
                # Kannada - Premium quality
                {"code": "kn", "name": "ಕನ್ನಡ Kannada - Premium", "engine": "gTTS", "quality": "premium"},
            ]
        elif self.engine is not None:
            # Fallback to pyttsx3 voices
            try:
                voices = self.engine.getProperty('voices')
                filtered_voices = []
                
                # Priority languages
                priority_langs = ['english', 'hindi', 'kannada']
                
                for voice in voices:
                    voice_name_lower = voice.name.lower()
                    for lang in priority_langs:
                        if lang in voice_name_lower:
                            filtered_voices.append({
                                "code": lang[:2],
                                "name": voice.name,
                                "id": voice.id,
                                "quality": "high"
                            })
                            break
                
                # If no specific voices found, return first 3 voices
                if not filtered_voices and len(voices) > 0:
                    filtered_voices = [
                        {"code": "en", "name": voices[i].name if i < len(voices) else "Default", 
                         "id": voices[i].id if i < len(voices) else 0, "quality": "standard"}
                        for i in range(min(3, len(voices)))
                    ]
                
                return filtered_voices if filtered_voices else [{"code": "en", "name": "Default", "quality": "standard"}]
            except:
                return [{"code": "en", "name": "English (Default)", "quality": "standard"}]
        else:
            # No TTS engine available, return default
            return [
                {"code": "en", "name": "English (US) - Premium", "engine": "none", "quality": "premium"},
                {"code": "hi", "name": "हिंदी Hindi - Premium", "engine": "none", "quality": "premium"},
                {"code": "kn", "name": "ಕನ್ನಡ Kannada - Premium", "engine": "none", "quality": "premium"},
            ]
