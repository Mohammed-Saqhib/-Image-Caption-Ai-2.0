import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import os
import time
import io
from ocr_engine import OCREngine
from tts_engine import TTSEngine
from caption_engine import CaptionEngine
from translation_engine import TranslationEngine

# Set page configuration
st.set_page_config(
    page_title="Image AI Platform - Next Level", 
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .stDownloadButton button {
        width: 100%;
        background-color: #667eea;
        color: white;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Image AI Platform - Next Level</h1>
    <p>AI-Powered OCR, Captioning, Translation & Text-to-Speech</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Settings
st.sidebar.header("⚙️ Settings")

# OCR Languages
ocr_languages = st.sidebar.multiselect(
    "OCR Languages",
    ['en', 'hi', 'kn', 'ta', 'te', 'mr', 'bn'],
    default=['en', 'hi']
)

if not ocr_languages:
    st.sidebar.warning("⚠️ Select at least one OCR language.")

# Caption Mode
st.sidebar.subheader("🎨 Caption Settings")
use_caption = st.sidebar.checkbox("Enable AI Captioning", value=True)
caption_mode = st.sidebar.radio(
    "Caption Mode",
    ["Local Model (Slower, Private)", "Cloud API (Faster)"],
    index=1
)

# Image Enhancement
st.sidebar.subheader("🖼️ Image Enhancement")
enable_enhancement = st.sidebar.checkbox("Enable Image Enhancement", value=False)

if enable_enhancement:
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
    sharpness = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0, 0.1)

# Initialize Engines
@st.cache_resource
def get_ocr_engine(langs):
    return OCREngine(languages=langs)

@st.cache_resource
def get_tts_engine():
    return TTSEngine()

@st.cache_resource
def get_caption_engine(use_cloud):
    return CaptionEngine(use_cloud=use_cloud)

@st.cache_resource
def get_translation_engine():
    return TranslationEngine()

# Initialize
try:
    ocr_engine = get_ocr_engine(ocr_languages)
    tts_engine = get_tts_engine()
    translation_engine = get_translation_engine()
    
    if use_caption:
        with st.spinner('Loading AI Caption Model...'):
            caption_engine = get_caption_engine(use_cloud=(caption_mode == "Cloud API (Faster)"))
    else:
        caption_engine = None
        
except Exception as e:
    st.error(f"❌ Error initializing engines: {e}")
    st.stop()

# Main Content - Image Upload Section
st.markdown("### 📸 Select Image Source")

# Create two columns for upload options
col_upload, col_sample = st.columns(2)

with col_upload:
    st.markdown("#### 📤 Upload from Device")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "webp"], label_visibility="collapsed")

with col_sample:
    st.markdown("#### 🖼️ Use Sample Image")
    
    # Get sample images from folder
    sample_folder = "sample_images"
    sample_images = []
    
    if os.path.exists(sample_folder):
        sample_files = [f for f in os.listdir(sample_folder) 
                       if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')) 
                       and not f.startswith('.')]
        sample_images = sorted(sample_files)
    
    if sample_images:
        # Add a "None" option at the beginning
        sample_options = ["-- Select Sample --"] + sample_images
        selected_sample = st.selectbox("Choose a sample", sample_options, label_visibility="collapsed")
        
        # Show preview of selected sample
        if selected_sample != "-- Select Sample --":
            sample_path = os.path.join(sample_folder, selected_sample)
            preview_img = Image.open(sample_path)
            st.image(preview_img, caption=f"Preview: {selected_sample}", width=200)
            # Load sample image
            uploaded_file = sample_path  # We'll handle this differently below
    else:
        st.info("ℹ️ No sample images available. Add images to the `sample_images` folder.")
        selected_sample = None

# Process the image (from upload or sample)
image = None
original_image = None

if uploaded_file is not None:
    # Check if it's a file upload or sample path
    if isinstance(uploaded_file, str):
        # It's a sample image path
        image = Image.open(uploaded_file)
        original_image = image.copy()
    else:
        # It's an uploaded file
        image = Image.open(uploaded_file)
        original_image = image.copy()

if image is not None:
    
    # Apply enhancements if enabled
    if enable_enhancement:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)
        
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)
        
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness)
    
    # Create tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Image & OCR", "🎨 AI Caption", "🌍 Translation", "🎧 Text-to-Speech"])
    
    # Tab 1: Image & OCR
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Image Preview")
            if enable_enhancement:
                st.image(image, caption='Enhanced Image', use_container_width=True)
                with st.expander("View Original"):
                    st.image(original_image, caption='Original Image', use_container_width=True)
            else:
                st.image(image, caption='Uploaded Image', use_container_width=True)
        
        with col2:
            st.subheader("📝 Extracted Text (OCR)")
            
            if 'extracted_text' not in st.session_state:
                with st.spinner('🔍 Extracting text from image...'):
                    try:
                        extracted_text = ocr_engine.extract_text(image)
                        st.session_state.extracted_text = extracted_text
                    except Exception as e:
                        st.error(f"❌ OCR Error: {e}")
                        st.session_state.extracted_text = ""
            else:
                extracted_text = st.session_state.extracted_text
            
            if extracted_text.strip():
                st.text_area("Extracted Text", extracted_text, height=300, key="ocr_text")
                
                # Download OCR text
                st.download_button(
                    label="📥 Download Text (TXT)",
                    data=extracted_text,
                    file_name=f"ocr_text_{int(time.time())}.txt",
                    mime="text/plain"
                )
            else:
                st.warning("⚠️ No text found in the image.")
    
    # Tab 2: AI Caption
    with tab2:
        if use_caption and caption_engine:
            st.subheader("🎨 AI-Generated Caption")
            
            if 'caption_text' not in st.session_state:
                with st.spinner('🤖 AI is analyzing the image...'):
                    try:
                        caption = caption_engine.generate_caption(image)
                        st.session_state.caption_text = caption
                    except Exception as e:
                        st.error(f"❌ Caption Error: {e}")
                        st.session_state.caption_text = ""
            
            # Always get caption from session state
            caption = st.session_state.get('caption_text', '')
            
            if caption:
                st.markdown(f"""
                <div class="success-box">
                    <h3>🎯 Generated Caption:</h3>
                    <p style="font-size: 1.2rem; font-weight: 500;">{caption}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download caption
                st.download_button(
                    label="📥 Download Caption (TXT)",
                    data=caption,
                    file_name=f"caption_{int(time.time())}.txt",
                    mime="text/plain"
                )
        else:
            st.info("ℹ️ Enable AI Captioning in the sidebar to use this feature.")
    
    # Tab 3: Translation
    with tab3:
        st.subheader("🌍 Translate Text")
        
        # Choose source text
        source_choice = st.radio(
            "Select text to translate:",
            ["Extracted Text (OCR)", "AI Caption"],
            horizontal=True
        )
        
        if source_choice == "Extracted Text (OCR)":
            source_text = st.session_state.get('extracted_text', '')
        else:
            source_text = st.session_state.get('caption_text', '')
        
        if source_text.strip():
            target_langs = translation_engine.get_supported_languages()
            target_lang = st.selectbox("🌐 Select Target Language", target_langs, index=1)
            
            if st.button("🔄 Translate", key="translate_btn"):
                with st.spinner(f'Translating to {target_lang}...'):
                    try:
                        translated_text = translation_engine.translate(source_text, target_lang)
                        st.session_state.translated_text = translated_text
                        st.session_state.target_lang = target_lang
                    except Exception as e:
                        st.error(f"❌ Translation Error: {e}")
            
            if 'translated_text' in st.session_state:
                st.markdown(f"""
                <div class="success-box">
                    <h4>Translation ({st.session_state.target_lang}):</h4>
                    <p style="font-size: 1.1rem;">{st.session_state.translated_text}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download translation
                st.download_button(
                    label="📥 Download Translation (TXT)",
                    data=st.session_state.translated_text,
                    file_name=f"translation_{st.session_state.target_lang}_{int(time.time())}.txt",
                    mime="text/plain"
                )
        else:
            st.warning("⚠️ No text available to translate. Please extract text or generate a caption first.")
    
    # Tab 4: Text-to-Speech
    with tab4:
        st.subheader("🎧 Text-to-Speech with Auto-Translation")
        
        # Choose source text
        tts_source = st.radio(
            "Select text for audio:",
            ["Extracted Text (OCR)", "AI Caption", "Translated Text"],
            horizontal=True,
            key="tts_source"
        )
        
        if tts_source == "Extracted Text (OCR)":
            source_text = st.session_state.get('extracted_text', '')
        elif tts_source == "AI Caption":
            source_text = st.session_state.get('caption_text', '')
        else:
            source_text = st.session_state.get('translated_text', '')
        
        if source_text.strip():
            # Get voices
            voices = tts_engine.get_voices()
            
            # Helper to map language codes to names
            def get_language_name(lang_code):
                code = str(lang_code).split('_')[0].lower()
                lang_map = {
                    'en': 'English', 'hi': 'Hindi', 'kn': 'Kannada',
                    'ta': 'Tamil', 'te': 'Telugu', 'mr': 'Marathi',
                    'bn': 'Bengali', 'gu': 'Gujarati', 'ml': 'Malayalam',
                    'de': 'German', 'fr': 'French', 'es': 'Spanish',
                    'it': 'Italian', 'pt': 'Portuguese', 'ja': 'Japanese',
                    'ko': 'Korean', 'zh': 'Chinese', 'ru': 'Russian', 'ar': 'Arabic'
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
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_lang = st.selectbox("🎙️ Select Output Language", available_languages)
            
            with col2:
                rate = st.slider("⚡ Speech Rate", 100, 300, 200)
            
            selected_voice_id = None
            selected_voice_name = None
            
            if selected_lang:
                lang_voices = voices_by_lang[selected_lang]
                selected_voice = lang_voices[0]
                
                if selected_lang == 'English':
                    for v in lang_voices:
                        if 'IN' in str(v.languages[0]) or 'India' in v.name:
                            selected_voice = v
                            break
                        elif 'US' in str(v.languages[0]) and 'IN' not in str(selected_voice.languages[0]):
                             selected_voice = v
                
                selected_voice_id = selected_voice.id
                selected_voice_name = selected_voice.name
            
            st.info(f"🎤 Selected Voice: **{selected_voice_name}** ({selected_lang})")
            
            # Show what will happen
            if selected_lang != 'English':
                st.warning(f"💡 **Smart Translation**: Your text will be automatically translated to **{selected_lang}** before generating audio!")
            
            if st.button("🎵 Generate Audio", key="generate_audio"):
                with st.spinner('🎵 Generating audio...'):
                    try:
                        # Translate text to selected language if not English
                        final_text = source_text
                        
                        if selected_lang != 'English':
                            with st.spinner(f'Translating to {selected_lang}...'):
                                try:
                                    final_text = translation_engine.translate(source_text, selected_lang)
                                    st.success(f"✅ Translated to {selected_lang}")
                                    
                                    # Show translated text
                                    with st.expander(f"📝 Translated Text ({selected_lang})"):
                                        st.write(final_text)
                                except Exception as e:
                                    st.error(f"Translation failed: {e}. Using original text.")
                                    final_text = source_text
                        
                        # Generate audio with the (possibly translated) text
                        tts_engine.set_voice(selected_voice_id)
                        tts_engine.set_rate(rate)
                        
                        timestamp = int(time.time())
                        output_file = f"output_audio_{timestamp}.wav"
                        
                        tts_engine.save_to_file(final_text, output_file)
                        
                        st.success(f"✅ Audio generated successfully in {selected_lang}!")
                        st.audio(output_file, format='audio/wav')
                        
                        # Download audio
                        with open(output_file, 'rb') as f:
                            audio_bytes = f.read()
                        
                        st.download_button(
                            label=f"📥 Download Audio ({selected_lang})",
                            data=audio_bytes,
                            file_name=output_file,
                            mime="audio/wav"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Audio Error: {e}")
        else:
            st.warning("⚠️ No text available for audio generation.")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Statistics")
    if 'extracted_text' in st.session_state:
        word_count = len(st.session_state.extracted_text.split())
        char_count = len(st.session_state.extracted_text)
        st.metric("Words", word_count)
        st.metric("Characters", char_count)

with col2:
    st.markdown("### 🛠️ Technologies")
    st.markdown("""
    - EasyOCR
    - BLIP Model
    - Deep Translator
    - pyttsx3 / macOS say
    """)

with col3:
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Use image enhancement for better OCR
    - Cloud API is faster for captions
    - Try different voices and rates
    """)

st.markdown("""
---
<div style="text-align: center; padding: 2rem;">
    <h3>🚀 Image AI Platform - Next Level Edition</h3>
    <p>Built with ❤️ using Streamlit, EasyOCR, BLIP, Deep Translator & Advanced TTS</p>
    <p><strong>Final Year Project - Enhanced Version</strong></p>
</div>
""", unsafe_allow_html=True)
