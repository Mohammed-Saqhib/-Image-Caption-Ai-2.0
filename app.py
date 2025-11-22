import streamlit as st

st.set_page_config(page_title="AI Image Analysis", page_icon="🚀", layout="wide")

st.title("🚀 AI Image Analysis Platform")
st.success("✅ App is running! Upload functionality coming soon...")

# Simple file uploader
uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.image(uploaded_file, caption="Your Image", use_container_width=True)
    st.info("�� Image uploaded successfully!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Extract Text", use_container_width=True):
            with st.spinner("Installing OCR..."):
                import subprocess, sys
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "easyocr", "opencv-python-headless"])
                import easyocr
                reader = easyocr.Reader(['en'], gpu=False)
                results = reader.readtext(uploaded_file.getvalue())
                if results:
                    text = "\n".join([r[1] for r in results])
                    st.text_area("Extracted Text:", text, height=200)
                else:
                    st.warning("No text found")
    
    with col2:
        if st.button("💬 Generate Caption", use_container_width=True):
            st.info("Caption feature will install AI model on first use (2-3 min)")
            with st.spinner("Installing AI model..."):
                import subprocess, sys
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "transformers", "torch", "pillow"])
                from transformers import BlipProcessor, BlipForConditionalGeneration
                from PIL import Image
                import torch
                
                processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
                model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
                
                image = Image.open(uploaded_file)
                inputs = processor(image, return_tensors="pt")
                with torch.no_grad():
                    out = model.generate(**inputs)
                caption = processor.decode(out[0], skip_special_tokens=True)
                st.success(f"📝 {caption}")
else:
    st.info("👆 Upload an image to get started")

st.markdown("---")
st.markdown("**Developer:** Mohammed Saqhib | [Email](mailto:msaqhib76@gmail.com) | [LinkedIn](http://www.linkedin.com/in/mohammed-saqhib-87b8b325a) | [GitHub](https://github.com/Mohammed-Saqhib)")
