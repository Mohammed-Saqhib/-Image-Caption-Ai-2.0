import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

st.set_page_config(
    page_title="AI Image Analysis Platform",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Image Analysis Platform - Professional Edition")
st.write("Loading application...")

# Try to import dependencies
import_status = {}

try:
    import torch
    import_status['PyTorch'] = f"✅ {torch.__version__}"
except Exception as e:
    import_status['PyTorch'] = f"❌ {str(e)}"

try:
    import transformers
    import_status['Transformers'] = f"✅ {transformers.__version__}"
except Exception as e:
    import_status['Transformers'] = f"❌ {str(e)}"

try:
    import easyocr
    import_status['EasyOCR'] = "✅ Loaded"
except Exception as e:
    import_status['EasyOCR'] = f"❌ {str(e)}"

try:
    import cv2
    import_status['OpenCV'] = f"✅ {cv2.__version__}"
except Exception as e:
    import_status['OpenCV'] = f"❌ {str(e)}"

st.subheader("📦 Dependency Check")
for lib, status in import_status.items():
    st.write(f"{lib}: {status}")

# If all dependencies loaded, try to load the actual app
all_loaded = all("✅" in status for status in import_status.values())

if all_loaded:
    st.success("All dependencies loaded successfully!")
    st.write("---")
    
    try:
        # Now try to load the actual application
        import app_pro
        st.success("✅ App loaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to load app_pro: {str(e)}")
        st.code(str(e))
        
        # Show traceback
        import traceback
        st.code(traceback.format_exc())
else:
    st.error("❌ Some dependencies failed to load. Check the status above.")
