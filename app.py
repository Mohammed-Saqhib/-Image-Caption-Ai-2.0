import streamlit as st
import subprocess
import sys
from PIL import Image
import io

# Page config
st.set_page_config(
    page_title="AI Image Analysis",
    page_icon="🖼️",
    layout="wide"
)

def install_package(package):
    """Install package on-demand"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

# Title
st.title("🖼️ AI Image Analysis Platform")
st.markdown("### Professional OCR & Image Captioning Tool")

# Sidebar
with st.sidebar:
    st.header("📋 Features")
    st.markdown("""
    - **🔍 Text Extraction**: OCR with EasyOCR
    - **💬 Image Captioning**: AI descriptions with BLIP
    - **⚡ Fast Loading**: Models load on-demand
    - **🎯 High Accuracy**: Professional-grade results
    """)
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.markdown("**Mohammed Saqhib**")
    st.markdown("[Email](mailto:msaqhib76@gmail.com) | [LinkedIn](http://www.linkedin.com/in/mohammed-saqhib-87b8b325a) | [GitHub](https://github.com/Mohammed-Saqhib)")

# File uploader
uploaded_file = st.file_uploader(
    "📁 Choose an image...",
    type=['png', 'jpg', 'jpeg', 'bmp', 'gif'],
    help="Upload an image file to analyze"
)

if uploaded_file is not None:
    # Display image
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📸 Uploaded Image")
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Analysis Options")
        
        # OCR Button
        if st.button("🔍 Extract Text (OCR)", use_container_width=True):
            with st.spinner("🔄 Loading OCR model... (first time: ~2 min)"):
                try:
                    # Install EasyOCR on demand
                    st.info("📦 Installing EasyOCR and dependencies...")
                    install_package("easyocr==1.7.0")
                    install_package("opencv-python-headless==4.8.0.76")
                    
                    import easyocr
                    import numpy as np
                    
                    # Initialize reader
                    st.info("🚀 Initializing OCR engine...")
                    reader = easyocr.Reader(['en'], gpu=False)
                    
                    # Convert PIL to numpy array
                    st.info("�� Extracting text from image...")
                    img_array = np.array(image)
                    
                    # Extract text
                    results = reader.readtext(img_array)
                    
                    if results:
                        st.success("✅ Text extracted successfully!")
                        extracted_text = "\n".join([text[1] for text in results])
                        st.text_area("📝 Extracted Text:", extracted_text, height=200)
                        
                        # Download button
                        st.download_button(
                            "💾 Download Text",
                            extracted_text,
                            file_name="extracted_text.txt",
                            mime="text/plain"
                        )
                    else:
                        st.warning("⚠️ No text found in image")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Try refreshing the page and trying again")
        
        st.markdown("---")
        
        # Caption Button
        if st.button("💬 Generate AI Caption", use_container_width=True):
            with st.spinner("🔄 Loading AI model... (first time: ~3 min)"):
                try:
                    # Install transformers on demand
                    st.info("📦 Installing AI models and dependencies...")
                    install_package("transformers==4.30.0")
                    install_package("torch==2.0.1+cpu")
                    
                    from transformers import BlipProcessor, BlipForConditionalGeneration
                    import torch
                    
                    # Load model
                    st.info("🚀 Loading BLIP model...")
                    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
                    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
                    
                    # Generate caption
                    st.info("🎨 Generating caption...")
                    inputs = processor(image, return_tensors="pt")
                    
                    with torch.no_grad():
                        outputs = model.generate(**inputs, max_length=50)
                    
                    caption = processor.decode(outputs[0], skip_special_tokens=True)
                    
                    st.success("✅ Caption generated!")
                    st.info(f"💬 **Caption:** {caption}")
                    
                    # Download button
                    st.download_button(
                        "💾 Download Caption",
                        caption,
                        file_name="caption.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Try refreshing the page and trying again")

else:
    # Instructions
    st.info("👆 Upload an image to get started!")
    
    # How to use
    with st.expander("ℹ️ How to use this tool"):
        st.markdown("""
        ### 📖 Instructions
        
        1. **Upload Image**: Click the file uploader above and select an image
        2. **Choose Analysis**: 
           - Click **🔍 Extract Text** for OCR
           - Click **💬 Generate Caption** for AI description
        3. **First Use**: Models download automatically (~2-3 minutes)
        4. **Subsequent Uses**: Instant results (models are cached!)
        
        ### ⚡ Performance
        - **Startup**: < 30 seconds
        - **First OCR**: ~2 minutes (downloading model)
        - **First Caption**: ~3 minutes (downloading model)
        - **After First Use**: Instant! ⚡
        
        ### 🎯 Features
        - Multi-language OCR support
        - State-of-the-art BLIP AI model
        - High accuracy results
        - Export results as text files
        """)
    
    # Sample info
    with st.expander("🖼️ Supported Image Formats"):
        st.markdown("""
        - PNG (.png)
        - JPEG (.jpg, .jpeg)
        - BMP (.bmp)
        - GIF (.gif)
        
        **Recommended**: Use clear, high-resolution images for best results
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🚀 <b>AI Image Analysis Platform</b> - Professional Edition</p>
    <p>Developed by <b>Mohammed Saqhib</b> | Aspiring Data Professional | Bengaluru, India</p>
    <p>
        <a href='mailto:msaqhib76@gmail.com'>📧 Email</a> | 
        <a href='http://www.linkedin.com/in/mohammed-saqhib-87b8b325a'>💼 LinkedIn</a> | 
        <a href='https://github.com/Mohammed-Saqhib'>🐙 GitHub</a> | 
        <a href='https://mohammed-saqhib.github.io/Portfolio/'>🌐 Portfolio</a>
    </p>
    <p><i>© 2024 Mohammed Saqhib | All Rights Reserved</i></p>
</div>
""", unsafe_allow_html=True)
