"""
Hugging Face Space Entry Point
AI Image Analysis Platform - Professional Edition
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
os.environ['IS_HUGGINGFACE_SPACE'] = 'true'

# Import streamlit first
import streamlit as st

# Now run the actual app
try:
    # Import and execute the app_pro module
    import app_pro
    print("✅ Successfully loaded AI Image Analysis Platform - Professional Edition")
except ImportError as e:
    print(f"⚠️ Error loading app_pro: {e}")
    print("Trying standard edition...")
    try:
        import app_enhanced
        print("✅ Successfully loaded AI Image Analysis Platform - Standard Edition")
    except Exception as e2:
        st.error(f"❌ Failed to load application: {e2}")
        st.info("Please check the deployment logs for more information.")
