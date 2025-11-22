import streamlit as st
from PIL import Image
import os
import time
from ocr_engine import OCREngine
from tts_engine import TTSEngine

# Set page configuration
st.set_page_config(page_title="Image AI Platform", layout="wide")

st.title("🖼️ Image AI Platform")
st.markdown("Upload an image to extract text and listen to it in different languages.")

# Sidebar for settings
st.sidebar.header("Settings")
languages = st.sidebar.multiselect(
    "Select OCR Languages",
    ['en', 'hi', 'kn', 'ta', 'te', 'mr'],
    default=['en', 'hi']
)

if not languages:
    st.sidebar.warning("Please select at least one language for OCR.")

# Initialize Engines
@st.cache_resource
def get_ocr_engine(langs):
    return OCREngine(languages=langs)

@st.cache_resource
def get_tts_engine():
    return TTSEngine()

try:
    ocr_engine = get_ocr_engine(languages)
    tts_engine = get_tts_engine()
except Exception as e:
    st.error(f"Error initializing engines: {e}")
    st.stop()

# Main Content
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Uploaded Image")
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width=True)
        
    with col2:
        st.subheader("Extracted Text")
        with st.spinner('Extracting text...'):
            try:
                extracted_text = ocr_engine.extract_text(image)
                if extracted_text.strip():
                    st.text_area("Text", extracted_text, height=300)
                else:
                    st.warning("No text found in the image.")
                    extracted_text = ""
            except Exception as e:
                st.error(f"Error during OCR: {e}")
                extracted_text = ""

    if extracted_text:
        st.divider()
        st.subheader("🎧 Listen to Text")
        
        # TTS Settings
        voices = tts_engine.get_voices()
        
        # Helper to map language codes to names
        def get_language_name(lang_code):
            code = str(lang_code).split('_')[0].lower()
            lang_map = {
                'en': 'English',
                'hi': 'Hindi',
                'kn': 'Kannada',
                'ta': 'Tamil',
                'te': 'Telugu',
                'mr': 'Marathi',
                'bn': 'Bengali',
                'gu': 'Gujarati',
                'ml': 'Malayalam',
                'de': 'German',
                'fr': 'French',
                'es': 'Spanish',
                'it': 'Italian',
                'pt': 'Portuguese',
                'ja': 'Japanese',
                'ko': 'Korean',
                'zh': 'Chinese',
                'ru': 'Russian',
                'ar': 'Arabic'
            }
            return lang_map.get(code, 'Other')

        voices_by_lang = {}
        for voice in voices:
            if voice.languages:
                lang_code = voice.languages[0]
                if isinstance(lang_code, bytes):
                    lang_code = lang_code.decode('utf-8')
                
                lang_name = get_language_name(lang_code)
                if lang_name == 'Other': continue

                if lang_name not in voices_by_lang:
                    voices_by_lang[lang_name] = []
                voices_by_lang[lang_name].append(voice)
        
        available_languages = sorted(voices_by_lang.keys())
        
        # Default to English if available
        default_index = 0
        if 'English' in available_languages:
            default_index = available_languages.index('English')

        selected_lang = st.selectbox("Select Audio Language", available_languages, index=default_index)
        
        selected_voice_id = None
        selected_voice_name = None
        if selected_lang:
            lang_voices = voices_by_lang[selected_lang]
            # Simple heuristic to pick a good voice
            selected_voice = lang_voices[0]
            
            if selected_lang == 'English':
                for v in lang_voices:
                    # Check for Indian English first
                    if 'IN' in str(v.languages[0]) or 'India' in v.name:
                        selected_voice = v
                        break
                    # Check for US English as fallback preference over others
                    elif 'US' in str(v.languages[0]) and 'IN' not in str(selected_voice.languages[0]):
                         selected_voice = v
            
            selected_voice_id = selected_voice.id
            selected_voice_name = selected_voice.name
        
        st.info(f"🎙️ Selected Voice: **{selected_voice_name}** ({selected_lang})")
        
        rate = st.slider("Speech Rate", 100, 300, 200)
        
        if st.button("Generate Audio"):
            with st.spinner('Generating audio...'):
                try:
                    tts_engine.set_voice(selected_voice_id)
                    tts_engine.set_rate(rate)
                    
                    # Use a unique filename to avoid caching/locking issues
                    timestamp = int(time.time())
                    output_file = f"output_audio_{timestamp}.wav"
                    
                    tts_engine.save_to_file(extracted_text, output_file)
                    
                    # Display audio player
                    st.audio(output_file, format='audio/wav')
                    
                except Exception as e:
                    st.error(f"Error generating audio: {e}")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, EasyOCR, and Pyttsx3")
