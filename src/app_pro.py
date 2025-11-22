"""
🚀 AI Image Analysis Platform - Professional Edition
Advanced OCR, Captioning, Translation & TTS with Enhanced Features
"""

import streamlit as st
import time
from pathlib import Path
import os
from PIL import Image
import io
import json
from datetime import datetime
import zipfile

# Import existing engines
from ocr_engine import OCREngine
from caption_engine import CaptionEngine
from translation_engine import TranslationEngine
from tts_engine import TTSEngine

# Import new advanced modules
try:
    from image_processor import ImageProcessor
    IMAGE_PROCESSOR_AVAILABLE = True
except ImportError:
    IMAGE_PROCESSOR_AVAILABLE = False

try:
    from export_engine import ExportEngine
    EXPORT_ENGINE_AVAILABLE = True
except ImportError:
    EXPORT_ENGINE_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="AI Image Analysis Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern dark theme support
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #4A90E2;
        --secondary-color: #50C878;
        --accent-color: #FF6B6B;
        --bg-dark: #1E1E1E;
        --bg-light: #2D2D2D;
        --text-light: #E0E0E0;
    }
    
    /* Enhanced header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
    }
    
    .stat-label {
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }
    
    /* Enhanced buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }
    
    /* Progress indicators */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Image quality badge */
    .quality-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .quality-excellent {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    
    .quality-good {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .quality-fair {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
    }
    
    .quality-poor {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Download section */
    .download-section {
        background: linear-gradient(135deg, #f093fb20 0%, #f5576c20 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Animations */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .processing {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 2rem;
        background: rgba(102, 126, 234, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processing_history' not in st.session_state:
    st.session_state.processing_history = []
if 'total_processed' not in st.session_state:
    st.session_state.total_processed = 0
if 'batch_mode' not in st.session_state:
    st.session_state.batch_mode = False

# Initialize engines
@st.cache_resource
def load_engines():
    """Load all processing engines"""
    engines = {
        'ocr': OCREngine(),
        'caption': CaptionEngine(),
        'translation': TranslationEngine(),
        'tts': TTSEngine()
    }
    
    if IMAGE_PROCESSOR_AVAILABLE:
        engines['image_processor'] = ImageProcessor()
    
    if EXPORT_ENGINE_AVAILABLE:
        engines['export'] = ExportEngine()
    
    return engines

try:
    engines = load_engines()
    ocr_engine = engines['ocr']
    caption_engine = engines['caption']
    translation_engine = engines['translation']
    tts_engine = engines['tts']
    image_processor = engines.get('image_processor')
    export_engine = engines.get('export')
except Exception as e:
    st.error(f"⚠️ Error loading engines: {e}")
    st.stop()

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 AI Image Analysis Platform</h1>
    <p>Professional Edition with Advanced Features</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings & Tools")
    
    # Theme selector
    theme_mode = st.selectbox("🎨 Theme", ["Professional", "Classic", "Dark Mode"])
    
    # Processing mode
    st.markdown("### 🔧 Processing Mode")
    processing_mode = st.radio(
        "Select mode:",
        ["Single Image", "Batch Processing"],
        help="Process one or multiple images"
    )
    
    st.session_state.batch_mode = (processing_mode == "Batch Processing")
    
    # Advanced options
    with st.expander("🎛️ Advanced Options"):
        enable_preprocessing = st.checkbox("Enable Image Preprocessing", value=True)
        enable_quality_check = st.checkbox("Quality Assessment", value=True)
        enable_auto_enhance = st.checkbox("Auto-Enhancement", value=False)
        aggressive_mode = st.checkbox("Aggressive Processing", value=False)
    
    # Statistics
    st.markdown("### 📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Processed", st.session_state.total_processed)
    with col2:
        st.metric("Session", len(st.session_state.processing_history))
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🗑️ Clear History"):
        st.session_state.processing_history = []
        st.rerun()
    
    if st.button("📥 Export History"):
        if st.session_state.processing_history and export_engine:
            history_json = export_engine.export_to_json({
                "history": st.session_state.processing_history,
                "stats": {
                    "total": st.session_state.total_processed,
                    "session": len(st.session_state.processing_history)
                }
            })
            st.download_button(
                "Download History (JSON)",
                history_json,
                file_name=f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# Main content
if st.session_state.batch_mode:
    st.markdown("## 📦 Batch Processing Mode")
    st.info("Upload multiple images to process them all at once!")
    
    uploaded_files = st.file_uploader(
        "Upload Images",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
        accept_multiple_files=True
    )
    
    if uploaded_files and len(uploaded_files) > 0:
        st.success(f"✅ Loaded {len(uploaded_files)} images")
        
        # Show thumbnails
        cols = st.columns(min(5, len(uploaded_files)))
        for idx, (col, file) in enumerate(zip(cols, uploaded_files[:5])):
            with col:
                img = Image.open(file)
                st.image(img, caption=f"Image {idx+1}", use_container_width=True)
        
        if len(uploaded_files) > 5:
            st.info(f"...and {len(uploaded_files) - 5} more images")
        
        # Batch processing options
        col1, col2, col3 = st.columns(3)
        with col1:
            batch_ocr = st.checkbox("Extract Text (OCR)", value=True)
        with col2:
            batch_caption = st.checkbox("Generate Captions", value=True)
        with col3:
            batch_translate = st.checkbox("Translate", value=False)
        
        if batch_translate:
            target_lang = st.selectbox("Target Language", translation_engine.supported_languages)
        
        if st.button("🚀 Process All Images", type="primary"):
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, file in enumerate(uploaded_files):
                status_text.text(f"Processing {file.name}... ({idx+1}/{len(uploaded_files)})")
                
                try:
                    img = Image.open(file)
                    result = {"filename": file.name, "success": True}
                    
                    # OCR
                    if batch_ocr:
                        extracted = ocr_engine.extract_text(img)
                        result['extracted_text'] = extracted
                    
                    # Caption
                    if batch_caption:
                        caption = caption_engine.generate_caption(img)
                        result['caption'] = caption
                    
                    # Translation
                    if batch_translate and batch_ocr:
                        translated = translation_engine.translate(result.get('extracted_text', ''), target_lang)
                        result['translated_text'] = translated
                        result['target_language'] = target_lang
                    
                    results.append(result)
                    st.session_state.total_processed += 1
                    
                except Exception as e:
                    results.append({"filename": file.name, "success": False, "error": str(e)})
                
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.success(f"✅ Processed {len(uploaded_files)} images!")
            
            # Show results summary
            st.markdown("### 📊 Batch Results")
            successful = sum(1 for r in results if r.get('success'))
            failed = len(results) - successful
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{len(results)}</div>
                    <div class="stat-label">Total Processed</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="stat-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
                    <div class="stat-value">{successful}</div>
                    <div class="stat-label">Successful</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="stat-card" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);">
                    <div class="stat-value">{failed}</div>
                    <div class="stat-label">Failed</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Export batch results
            if export_engine:
                st.markdown("### 📥 Export Batch Results")
                
                batch_report = export_engine.create_batch_report(results)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        "📄 Download JSON Report",
                        batch_report['json'],
                        file_name=f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                with col2:
                    st.download_button(
                        "📝 Download Text Report",
                        batch_report['txt'],
                        file_name=f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
                with col3:
                    # Create ZIP with all results
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        # Add JSON report
                        zip_file.writestr("report.json", batch_report['json'])
                        zip_file.writestr("report.txt", batch_report['txt'])
                        
                        # Add individual results
                        for result in results:
                            if result.get('success'):
                                filename = result['filename'].rsplit('.', 1)[0]
                                content = export_engine.export_to_txt(result, include_metadata=False)
                                zip_file.writestr(f"{filename}_result.txt", content)
                    
                    zip_buffer.seek(0)
                    st.download_button(
                        "📦 Download Complete Package (ZIP)",
                        zip_buffer,
                        file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip"
                    )
            
            # Show detailed results
            with st.expander("📋 View Detailed Results"):
                for idx, result in enumerate(results, 1):
                    st.markdown(f"**{idx}. {result['filename']}**")
                    if result.get('success'):
                        if result.get('extracted_text'):
                            st.text(f"Text: {result['extracted_text'][:100]}...")
                        if result.get('caption'):
                            st.text(f"Caption: {result['caption']}")
                        st.success("✅ Success")
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown')}")
                    st.divider()

else:
    # Single image mode
    st.markdown("## 🖼️ Single Image Processing")
    
    # Image upload with sample selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Supported formats: PNG, JPG, JPEG, BMP, TIFF"
        )
    
    with col2:
        # Sample images
        sample_dir = Path("sample_images")
        if sample_dir.exists():
            sample_files = [f.name for f in sample_dir.glob("*.png")]
            if sample_files:
                selected_sample = st.selectbox(
                    "Or select a sample:",
                    ["None"] + sample_files
                )
                
                if selected_sample != "None":
                    sample_path = sample_dir / selected_sample
                    uploaded_file = str(sample_path)
    
    if uploaded_file:
        # Load image
        if isinstance(uploaded_file, str):
            image = Image.open(uploaded_file)
            original_image = image.copy()
        else:
            image = Image.open(uploaded_file)
            original_image = image.copy()
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎨 Image & Preprocessing",
            "📝 OCR & Text",
            "🖼️ AI Caption",
            "🌐 Translation",
            "🎧 Text-to-Speech"
        ])
        
        # Tab 1: Image preprocessing
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📸 Original Image")
                st.image(original_image, use_container_width=True)
                
                # Quality assessment
                if enable_quality_check and image_processor:
                    with st.spinner("Analyzing image quality..."):
                        quality = image_processor.quality_assessment(original_image)
                        
                        # Quality badge
                        score = quality['overall_score']
                        if score >= 80:
                            badge_class = "quality-excellent"
                        elif score >= 60:
                            badge_class = "quality-good"
                        elif score >= 40:
                            badge_class = "quality-fair"
                        else:
                            badge_class = "quality-poor"
                        
                        st.markdown(f"""
                        <div class="quality-badge {badge_class}">
                            Quality Score: {score}% - {quality['recommendation']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Detailed metrics
                        with st.expander("📊 Detailed Metrics"):
                            met_col1, met_col2, met_col3 = st.columns(3)
                            with met_col1:
                                st.metric("Sharpness", f"{quality['sharpness']}%")
                            with met_col2:
                                st.metric("Brightness", f"{quality['brightness']}%")
                            with met_col3:
                                st.metric("Contrast", f"{quality['contrast']}%")
            
            with col2:
                st.markdown("### ⚡ Enhanced Image")
                
                if image_processor and enable_preprocessing:
                    # Preprocessing controls
                    with st.expander("🎛️ Preprocessing Controls", expanded=True):
                        preset = st.radio(
                            "Choose preset:",
                            ["None", "Auto Enhance", "Custom"],
                            horizontal=True
                        )
                        
                        if preset == "Auto Enhance":
                            if st.button("🚀 Apply Auto Enhancement"):
                                with st.spinner("Enhancing image..."):
                                    processed_image = image_processor.auto_enhance(
                                        original_image,
                                        aggressive=aggressive_mode
                                    )
                                    st.session_state['processed_image'] = processed_image
                                    st.session_state['preprocessing_applied'] = True
                        
                        elif preset == "Custom":
                            denoise_strength = st.slider("Noise Reduction", 0, 30, 10)
                            sharpen_factor = st.slider("Sharpness", 1.0, 5.0, 2.0, 0.1)
                            apply_threshold = st.checkbox("Adaptive Threshold")
                            apply_deskew = st.checkbox("Auto Deskew")
                            
                            if st.button("✨ Apply Custom Processing"):
                                with st.spinner("Processing..."):
                                    processed = original_image.copy()
                                    
                                    if denoise_strength > 0:
                                        processed = image_processor.denoise(processed, denoise_strength)
                                    
                                    if apply_deskew:
                                        processed = image_processor.deskew(processed)
                                    
                                    if sharpen_factor > 1.0:
                                        processed = image_processor.sharpen(processed, sharpen_factor)
                                    
                                    if apply_threshold:
                                        processed = image_processor.adaptive_threshold(processed)
                                    
                                    st.session_state['processed_image'] = processed
                                    st.session_state['preprocessing_applied'] = True
                    
                    # Show processed image
                    if st.session_state.get('preprocessing_applied'):
                        processed_img = st.session_state['processed_image']
                        st.image(processed_img, use_container_width=True)
                        
                        if image_processor.processing_history:
                            st.info(f"Applied: {image_processor.get_processing_summary()}")
                        
                        # Use processed image for OCR
                        image = processed_img
                    else:
                        st.image(original_image, use_container_width=True)
                        st.info("Original image - no preprocessing applied")
                else:
                    st.image(original_image, use_container_width=True)
        
        # Tab 2: OCR
        with tab2:
            st.markdown("### 📝 Extract Text from Image")
            
            ocr_langs = st.multiselect(
                "Select OCR languages",
                ['en', 'hi', 'kn', 'ta', 'te', 'mr', 'bn'],
                default=['en']
            )
            
            if st.button("🔍 Extract Text", key="extract_btn"):
                with st.spinner("Extracting text..."):
                    extracted_text = ocr_engine.extract_text(image, languages=ocr_langs)
                    st.session_state['extracted_text'] = extracted_text
                    
                    # Add to history
                    st.session_state.processing_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "type": "OCR",
                        "languages": ocr_langs,
                        "text_length": len(extracted_text)
                    })
            
            if st.session_state.get('extracted_text'):
                st.success("✅ Text extracted successfully!")
                
                st.text_area(
                    "Extracted Text",
                    st.session_state['extracted_text'],
                    height=200,
                    key="ocr_text_display"
                )
                
                # Export options
                if export_engine:
                    st.markdown("### 📥 Export Options")
                    
                    export_cols = st.columns(4)
                    
                    with export_cols[0]:
                        txt_export = export_engine.export_to_txt(
                            {"extracted_text": st.session_state['extracted_text']}
                        )
                        st.download_button(
                            "📄 TXT",
                            txt_export,
                            file_name="extracted_text.txt",
                            mime="text/plain"
                        )
                    
                    with export_cols[1]:
                        json_export = export_engine.export_to_json(
                            {"extracted_text": st.session_state['extracted_text']},
                            {"languages": ocr_langs, "timestamp": datetime.now().isoformat()}
                        )
                        st.download_button(
                            "📋 JSON",
                            json_export,
                            file_name="extracted_text.json",
                            mime="application/json"
                        )
                    
                    with export_cols[2]:
                        try:
                            # Save image temporarily
                            temp_img_path = "temp_image.png"
                            original_image.save(temp_img_path)
                            
                            pdf_buffer = export_engine.export_to_pdf(
                                {"extracted_text": st.session_state['extracted_text']},
                                image_path=temp_img_path
                            )
                            st.download_button(
                                "📕 PDF",
                                pdf_buffer,
                                file_name="extracted_text.pdf",
                                mime="application/pdf"
                            )
                        except Exception as e:
                            st.error(f"PDF export unavailable: {e}")
                    
                    with export_cols[3]:
                        try:
                            temp_img_path = "temp_image.png"
                            original_image.save(temp_img_path)
                            
                            docx_buffer = export_engine.export_to_docx(
                                {"extracted_text": st.session_state['extracted_text']},
                                image_path=temp_img_path
                            )
                            st.download_button(
                                "📘 DOCX",
                                docx_buffer,
                                file_name="extracted_text.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        except Exception as e:
                            st.error(f"DOCX export unavailable: {e}")
        
        # Tab 3: Caption (similar structure)
        with tab3:
            st.markdown("### 🖼️ AI Image Captioning")
            
            col1, col2 = st.columns(2)
            with col1:
                caption_mode = st.radio("Processing mode:", ["Local Model", "Cloud API"], horizontal=True)
            with col2:
                max_length = st.slider("Caption length", 20, 100, 50)
            
            if st.button("🎨 Generate Caption", key="caption_btn"):
                with st.spinner("Generating caption..."):
                    use_api = (caption_mode == "Cloud API")
                    caption = caption_engine.generate_caption(image, max_length=max_length, use_api=use_api)
                    st.session_state['caption_text'] = caption
                    
                    st.session_state.processing_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "type": "Caption",
                        "mode": caption_mode
                    })
            
            if st.session_state.get('caption_text'):
                st.success("✅ Caption generated!")
                
                st.markdown(f"""
                <div class="info-box">
                    <h4>📝 Generated Caption:</h4>
                    <p style="font-size: 1.1rem;">{st.session_state['caption_text']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Export caption
                if export_engine:
                    st.markdown("### 📥 Export Caption")
                    export_cols = st.columns(4)
                    
                    with export_cols[0]:
                        st.download_button(
                            "📄 TXT",
                            st.session_state['caption_text'],
                            file_name="caption.txt",
                            mime="text/plain"
                        )
                    
                    with export_cols[1]:
                        json_export = export_engine.export_to_json(
                            {"caption": st.session_state['caption_text']}
                        )
                        st.download_button(
                            "📋 JSON",
                            json_export,
                            file_name="caption.json",
                            mime="application/json"
                        )
        
        # Tab 4: Translation (existing logic)
        with tab4:
            st.markdown("### 🌐 Translation")
            
            trans_source = st.radio(
                "Select text to translate:",
                ["Extracted Text (OCR)", "AI Caption"],
                horizontal=True
            )
            
            source_text = st.session_state.get('extracted_text' if trans_source.startswith('Extracted') else 'caption_text', '')
            
            if source_text:
                target_lang = st.selectbox("Target language:", translation_engine.supported_languages)
                
                if st.button("🌍 Translate", key="translate_btn"):
                    with st.spinner(f"Translating to {target_lang}..."):
                        translated = translation_engine.translate(source_text, target_lang)
                        st.session_state['translated_text'] = translated
                        st.session_state['target_language'] = target_lang
                
                if st.session_state.get('translated_text'):
                    st.success(f"✅ Translated to {st.session_state.get('target_language')}!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original:**")
                        st.text_area("", source_text, height=150, key="orig_trans")
                    with col2:
                        st.markdown(f"**{st.session_state.get('target_language')}:**")
                        st.text_area("", st.session_state['translated_text'], height=150, key="trans_result")
                    
                    # Export
                    if export_engine:
                        srt_content = export_engine.export_to_srt(
                            st.session_state['translated_text'],
                            language=st.session_state.get('target_language', 'en')
                        )
                        st.download_button(
                            "📥 Download SRT Subtitles",
                            srt_content,
                            file_name=f"subtitles_{st.session_state.get('target_language', 'en')}.srt",
                            mime="text/plain"
                        )
        
        # Tab 5: TTS (existing logic with enhancements)
        with tab5:
            st.markdown("### 🎧 Text-to-Speech with Auto-Translation")
            
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
                voices = tts_engine.get_voices()
                
                def get_language_name(lang_code):
                    code = str(lang_code).split('_')[0].lower()
                    lang_map = {
                        'en': 'English', 'hi': 'Hindi', 'kn': 'Kannada',
                        'ta': 'Tamil', 'te': 'Telugu', 'mr': 'Marathi',
                        'bn': 'Bengali', 'gu': 'Gujarati', 'ml': 'Malayalam'
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
                
                if selected_lang:
                    lang_voices = voices_by_lang[selected_lang]
                    selected_voice = lang_voices[0]
                    
                    if selected_lang == 'English':
                        for v in lang_voices:
                            if 'IN' in str(v.languages[0]) or 'India' in v.name:
                                selected_voice = v
                                break
                    
                    selected_voice_id = selected_voice.id
                    selected_voice_name = selected_voice.name
                    
                    st.info(f"🎤 Selected Voice: **{selected_voice_name}** ({selected_lang})")
                    
                    if selected_lang != 'English':
                        st.warning(f"💡 **Smart Translation**: Your text will be automatically translated to **{selected_lang}** before generating audio!")
                    
                    if st.button("🎵 Generate Audio", key="generate_audio"):
                        with st.spinner('🎵 Generating audio...'):
                            try:
                                final_text = source_text
                                
                                if selected_lang != 'English':
                                    with st.spinner(f'Translating to {selected_lang}...'):
                                        try:
                                            final_text = translation_engine.translate(source_text, selected_lang)
                                            st.success(f"✅ Translated to {selected_lang}")
                                            
                                            with st.expander(f"📝 Translated Text ({selected_lang})"):
                                                st.write(final_text)
                                        except Exception as e:
                                            st.error(f"Translation failed: {e}. Using original text.")
                                
                                tts_engine.set_voice(selected_voice_id)
                                tts_engine.set_rate(rate)
                                
                                timestamp = int(time.time())
                                output_file = f"output_audio_{timestamp}.wav"
                                
                                tts_engine.save_to_file(final_text, output_file)
                                
                                st.success(f"✅ Audio generated successfully in {selected_lang}!")
                                st.audio(output_file, format='audio/wav')
                                
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

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🚀 AI Image Analysis Pro**")
with col2:
    st.markdown("Made with ❤️ using Streamlit")
with col3:
    st.markdown(f"Version 2.0 | © {datetime.now().year}")
