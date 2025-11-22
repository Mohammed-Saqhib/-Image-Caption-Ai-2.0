import streamlit as st

st.title("🚀 AI Image Analysis Platform")
st.write("Testing Hugging Face Space deployment...")

# Test imports
st.subheader("Testing imports...")
try:
    import torch
    st.success(f"✅ PyTorch {torch.__version__}")
except Exception as e:
    st.error(f"❌ PyTorch: {e}")

try:
    import easyocr
    st.success("✅ EasyOCR")
except Exception as e:
    st.error(f"❌ EasyOCR: {e}")

try:
    import transformers
    st.success("✅ Transformers")
except Exception as e:
    st.error(f"❌ Transformers: {e}")

try:
    from PIL import Image
    st.success("✅ Pillow")
except Exception as e:
    st.error(f"❌ Pillow: {e}")

st.write("If all imports show ✅, the Space is working!")
